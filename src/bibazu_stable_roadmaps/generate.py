"""Transactional component export and JSON-lines GUI worker."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import shutil
import sys
import tempfile
import traceback
from uuid import uuid4

import networkx as nx
import yaml

from .inputs import EmptyPoseList, load_source, select_poses, sha256, read_json
from .roadmap import build_roadmap, handover_dict
from .render import thumbnails, embed_thumbnails, render_roadmap, render_pose_sheets

ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = {"yaml": "YAML", "json": "JSON", "graphml": "GraphML", "roadmap_svg": "Roadmap SVG",
           "roadmap_png": "Roadmap PNG", "poses_svg": "Pose sheets SVG", "poses_png": "Pose sheets PNG"}


class GenerationCancelled(Exception):
    pass


@dataclass(frozen=True)
class GenerationConfig:
    output_root: str = str(ROOT)
    minimum_frequency_percent: float = 5.0
    renumber_by_frequency: bool = True
    outputs: tuple[str, ...] = ("yaml", "json", "graphml", "roadmap_svg", "roadmap_png")

    def validate(self):
        if not self.output_root.strip():
            raise ValueError("Choose the output repository folder.")
        if not math.isfinite(self.minimum_frequency_percent) or not 0 <= self.minimum_frequency_percent <= 100:
            raise ValueError("Minimum observed frequency must be between 0 and 100%.")
        if not isinstance(self.renumber_by_frequency, bool):
            raise ValueError("Frequency numbering must be on or off.")
        if not self.outputs or set(self.outputs) - OUTPUTS.keys():
            raise ValueError("Select at least one valid output format.")


def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def _atomic_text(path: Path, text: str):
    temporary = path.with_name("." + path.name + "." + uuid4().hex + ".tmp")
    try:
        temporary.write_text(text, encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def repository_lock(root: Path):
    """Serialize component/index publication across application instances."""
    lock = root / ".roadmaps.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            pid = int(lock.read_text(encoding="ascii"))
            # On Windows os.kill(pid, 0) can terminate a process. Use the native
            # query API rather than a POSIX process-existence idiom.
            if sys.platform == "win32":
                import ctypes
                handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
                if handle:
                    ctypes.windll.kernel32.CloseHandle(handle)
                    alive = True
                else:
                    alive = False
            else:
                try:
                    os.kill(pid, 0)
                    alive = True
                except ProcessLookupError:
                    alive = False
            if alive:
                raise ValueError("Another roadmap generation is using this output repository.")
        except (OSError, ValueError) as error:
            if isinstance(error, ValueError) and str(error).startswith("Another"):
                raise
            raise ValueError("An unreadable output lock exists; close other generators and remove .roadmaps.lock.") from error
        lock.unlink()
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        with os.fdopen(descriptor, "w", encoding="ascii") as handle:
            handle.write(str(os.getpid()))
        yield
    finally:
        lock.unlink(missing_ok=True)


INDEX_START = "<!-- GENERATED ROADMAP INDEX START -->"
INDEX_END = "<!-- GENERATED ROADMAP INDEX END -->"


def update_index(root: Path):
    entries = []
    for manifest_path in sorted(root.glob("*/manifest.json")):
        if manifest_path.parent.name.startswith("."):
            continue
        manifest = read_json(manifest_path)
        if manifest.get("format") != "bibazu_observed_roadmap_generation":
            continue
        entries.append({key: manifest[key] for key in ("workpiece", "pose_count", "transition_count", "minimum_frequency_percent", "renumber_by_frequency", "generated_utc")})
    _atomic_text(root / "index.json", json.dumps({"schema_version": 1, "workpieces": entries}, indent=2) + "\n")
    lines = ["| Component | Poses | Connections | Minimum frequency | Numbering |", "| --- | ---: | ---: | ---: | --- |"]
    for entry in entries:
        name = entry["workpiece"]
        mode = "Frequency" if entry["renumber_by_frequency"] else "Source ID"
        lines.append(f"| [{name}]({name}/README.md) | {entry['pose_count']} | {entry['transition_count']} | {entry['minimum_frequency_percent']:g}% | {mode} |")
    if not entries:
        lines = ["No component roadmaps generated yet."]
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.exists() else "# BiBaZu observed component roadmaps\n\n"
    replacement = INDEX_START + "\n" + "\n".join(lines) + "\n" + INDEX_END
    if INDEX_START in text and INDEX_END in text:
        start, end = text.index(INDEX_START), text.index(INDEX_END) + len(INDEX_END)
        text = text[:start] + replacement + text[end:]
    else:
        text += "\n" + replacement + "\n"
    _atomic_text(readme, text)


def _write_graphml(document: dict, destination: Path):
    graph = nx.MultiDiGraph()
    graph.graph["generation"] = json.dumps(document["generation"])
    graph.graph["classification_basis"] = "observed_simulation"
    for node in document["nodes"]:
        graph.add_node(node["node_id"], **{key: json.dumps(value) if isinstance(value, (list, dict)) else value
                                          for key, value in node.items() if value is not None and key not in {"node_id", "thumbnail_png_base64"}})
    for edge in document["edges"]:
        graph.add_edge(edge["source"], edge["target"], key=edge["edge_id"],
                       **{key: json.dumps(value) if isinstance(value, (list, dict)) else value
                          for key, value in edge.items() if value is not None and key not in {"source", "target"}})
    nx.write_graphml(graph, destination)


def _publish(root: Path, staging: Path, destination: Path):
    if destination.resolve().parent != root.resolve() or not staging.resolve().is_relative_to(root.resolve()):
        raise ValueError("Publication paths must stay inside the output repository.")
    if destination.exists():
        manifest = destination / "manifest.json"
        if not manifest.is_file() or read_json(manifest).get("format") != "bibazu_observed_roadmap_generation":
            raise ValueError(f"Refusing to replace an unmanaged folder: {destination.name}")
        # Preserve manual files rather than silently deleting them during a
        # complete replacement of the generated formats.
        inventory = read_json(destination / "files.sha256.json")
        actual = {p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file()}
        expected = set(inventory) | {"files.sha256.json"}
        if actual != expected or any(sha256(destination / path) != digest for path, digest in inventory.items()):
            raise ValueError(f"{destination.name} contains manually changed or added files. Save those changes elsewhere before regenerating.")
    backup = root / (".roadmap-backup-" + uuid4().hex)
    old_index = (root / "index.json").read_bytes() if (root / "index.json").exists() else None
    old_readme = (root / "README.md").read_bytes() if (root / "README.md").exists() else None
    moved_old = False
    moved_new = False
    try:
        if destination.exists():
            os.replace(destination, backup)
            moved_old = True
        os.replace(staging, destination)
        moved_new = True
        update_index(root)
    except BaseException:
        if moved_new:
            shutil.rmtree(destination)
        if moved_old:
            os.replace(backup, destination)
        for name, content in (("index.json", old_index), ("README.md", old_readme)):
            if content is None:
                (root / name).unlink(missing_ok=True)
            else:
                (root / name).write_bytes(content)
        raise
    if moved_old:
        shutil.rmtree(backup)


def generate_one(source_path: str | Path, config: GenerationConfig, progress=lambda message: None, check_cancel=lambda: None):
    config.validate()
    try:
        source = load_source(source_path)
    except EmptyPoseList as error:
        return "skipped", {"reason": str(error)}
    numbered, removed = select_poses(source, config.minimum_frequency_percent, config.renumber_by_frequency)
    if not numbered:
        return "skipped", {"reason": f"No poses remain at {config.minimum_frequency_percent:g}% minimum frequency."}
    root = Path(config.output_root).expanduser().resolve()
    destination = root / source.workpiece
    # Never replace the input catalogue itself or its component folders.
    if destination == source.path.parent or root == source.path.parent or root == source.path.parent.parent:
        raise ValueError("Choose the roadmaps repository as output, separate from the source poses repository.")
    root.mkdir(parents=True, exist_ok=True)
    with repository_lock(root):
        def report(message):
            check_cancel()
            progress(message)
        check_cancel()
        built = build_roadmap(source, numbered, report)
        for warning in built.warnings:
            progress(warning)
        generated_utc = datetime.now(timezone.utc).isoformat()
        metadata = {"minimum_frequency_percent": config.minimum_frequency_percent,
                    "renumber_by_frequency": config.renumber_by_frequency, "frequency_denominator": source.frequency_denominator,
                    "numbering_tie_break": "original source ID", "source_file": source.path.name,
                    "source_sha256": sha256(source.path), "generated_utc": generated_utc,
                    "pose_id_mapping": {pose.source_id: number for pose, number in numbered},
                    "removed_poses": [{"source_pose_id": pose.source_id, "frequency_percent": pose.frequency_percent} for pose in removed]}
        built.document.update(part_name=source.workpiece, generation=metadata,
                              pose_ranking_method="observed_frequency" if config.renumber_by_frequency else "source_id",
                              classical_metadata={"observed_pose_generation": metadata})
        progress(f"Exporting {len(numbered)} poses and {len(built.document['edges'])} direct connections")
        with tempfile.TemporaryDirectory(prefix=".roadmap-stage-", dir=root) as temporary:
            staging = Path(temporary) / source.workpiece
            staging.mkdir()
            snapshots = staging / "source"
            snapshots.mkdir()
            for path in source.snapshot_files:
                shutil.copyfile(path, snapshots / path.name)
            stem = staging / f"{source.workpiece}_roadmap"
            need_images = "json" in config.outputs or any(fmt.startswith("roadmap_") for fmt in config.outputs)
            images = thumbnails(built, check_cancel) if need_images else {}
            if "json" in config.outputs:
                embed_thumbnails(built.document, images)
                write_json(stem.with_suffix(".json"), built.document)
            if "yaml" in config.outputs:
                stem.with_suffix(".yaml").write_text(yaml.safe_dump(handover_dict(built.document), sort_keys=False, allow_unicode=True), encoding="utf-8")
            if "graphml" in config.outputs:
                _write_graphml(built.document, stem.with_suffix(".graphml"))
            formats = tuple(fmt for fmt in ("svg", "png") if f"roadmap_{fmt}" in config.outputs)
            if formats:
                render_roadmap(built, stem, formats, images)
            sheet_formats = tuple(fmt for fmt in ("svg", "png") if f"poses_{fmt}" in config.outputs)
            if sheet_formats:
                render_pose_sheets(built, staging / "pose_sheets", sheet_formats, check_cancel)
            manifest = {"format": "bibazu_observed_roadmap_generation", "schema_version": 1,
                        "workpiece": source.workpiece, "generated_utc": generated_utc,
                        "pose_count": len(numbered), "transition_count": len(built.document["edges"]),
                        "minimum_frequency_percent": config.minimum_frequency_percent,
                        "renumber_by_frequency": config.renumber_by_frequency,
                        "settings": {**asdict(config), "output_root": "."}, "input": metadata,
                        "analytical_stability_evaluated": False,
                        "engine_provenance": read_json(ROOT / "ENGINE_PROVENANCE.json"), "warnings": built.warnings}
            write_json(staging / "manifest.json", manifest)
            lines = [f"# {source.workpiece}\n", "Observed simulation poses; geometry supplies untested direct connection candidates.",
                     f"\nMinimum frequency: **{config.minimum_frequency_percent:g}%**. Percentages retain the source denominator.",
                     "\n| Roadmap pose | Source pose | Frequency | Count |", "| ---: | --- | ---: | ---: |"]
            lines.extend(f"| {number} | {pose.source_id} | {pose.frequency_percent:g}% | {pose.count if pose.count is not None else 'unknown'} |" for pose, number in numbered)
            lines.append("\nThe legacy `robust` tag is used for stable-target compatibility. It does not assert analytical robustness; rocking and reliability scores are unknown.")
            lines.append("\nOriginal inputs are in `source/`; generation settings and exclusions are in `manifest.json`.")
            lines.append("\nFiles: " + ", ".join(f"[{p.name}]({p.name})" for p in sorted(staging.glob(f"{source.workpiece}_roadmap.*"))))
            (staging / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
            write_json(staging / "files.sha256.json", {p.relative_to(staging).as_posix(): sha256(p) for p in sorted(staging.rglob("*")) if p.is_file()})
            # Validate references and JSON/YAML before replacing any previous set.
            ids = {node["node_id"] for node in built.document["nodes"]}
            if len(ids) != len(numbered) or any(edge["source"] not in ids or edge["target"] not in ids for edge in built.document["edges"]):
                raise ValueError("Generated roadmap references are inconsistent.")
            if "json" in config.outputs:
                read_json(stem.with_suffix(".json"))
            if "yaml" in config.outputs:
                yaml.safe_load(stem.with_suffix(".yaml").read_text(encoding="utf-8"))
            check_cancel()
            _publish(root, staging, destination)
    return "completed", {"folder": str(destination), "pose_count": len(numbered), "transition_count": len(built.document["edges"])}


def emit(**event):
    print(json.dumps(event, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="JSON request; otherwise read stdin")
    args = parser.parse_args()
    try:
        request = read_json(args.config) if args.config else json.loads(sys.stdin.read())
        config = GenerationConfig(**request.get("settings", {}))
        config.validate()
        sources = [Path(path) for path in request["sources"]]
        if not sources:
            raise ValueError("Select at least one component.")
        names = []
        for path in sources:
            try:
                names.append(load_source(path).workpiece)
            except EmptyPoseList:
                names.append(path.parent.name)
        if len({name.casefold() for name in names}) != len(names):
            raise ValueError("Selected inputs contain duplicate component names.")
        cancel_file = Path(request["cancel_file"]) if request.get("cancel_file") else None
    except Exception as error:
        emit(status="failed", message=str(error))
        return 1
    failures = 0
    def check_cancel():
        if cancel_file and cancel_file.exists():
            raise GenerationCancelled()
    for index, path in enumerate(sources):
        part = names[index]
        emit(source=str(path), part=part, status="running", index=index)
        try:
            status, result = generate_one(path, config, lambda message: emit(source=str(path), part=part, message=message), check_cancel)
            emit(source=str(path), part=part, status=status, index=index + 1, **result)
        except GenerationCancelled:
            emit(source=str(path), status="cancelled", message="Generation cancelled; existing results retained.")
            return 0
        except Exception as error:
            failures += 1
            emit(source=str(path), part=part, status="failed", index=index + 1, message=str(error), detail=traceback.format_exc())
    emit(status="finished", failures=failures)
    return int(failures > 0)


if __name__ == "__main__":
    raise SystemExit(main())
