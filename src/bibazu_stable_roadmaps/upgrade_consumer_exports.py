"""Stage finished consumer records without recalculating poses or direct geometry.

Run with --repository SOURCE --staging-root NEW_DIRECTORY. Publication is separate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

import yaml

from .consumer_export import attach_consumer_export
from .generate import _write_graphml, write_json
from .inputs import sha256


def upgrade_folder(folder):
    folder = Path(folder)
    path = folder / f"{folder.name}_roadmap.json"
    if not path.is_file():
        paths = list(folder.glob("*_roadmap.json"))
        if len(paths) != 1:
            raise ValueError(f"Expected one roadmap JSON in {folder}")
        path = paths[0]
    document = json.loads(path.read_text(encoding="utf-8"))
    old = json.dumps({k: v for k, v in document.items() if k != "consumer_export"}, sort_keys=True)
    attach_consumer_export(document)
    if old != json.dumps({k: v for k, v in document.items() if k != "consumer_export"}, sort_keys=True):
        raise ValueError("Consumer upgrade changed existing roadmap data")
    path.write_text(json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    yaml_path = path.with_suffix(".yaml")
    if yaml_path.is_file():
        handover = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        handover["consumer_export"] = document["consumer_export"]
        yaml_path.write_text(yaml.dump(handover, Dumper=getattr(yaml, "CSafeDumper", yaml.SafeDumper),
                                      sort_keys=False, allow_unicode=True), encoding="utf-8")
    graphml_path = path.with_suffix(".graphml")
    if graphml_path.is_file() and "generation" in document:
        _write_graphml(document, graphml_path)
    manifest_path = folder / "manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["consumer_export"] = dict(version=1, route_policy="exported_only",
            calibration_choice_count=len(document["consumer_export"]["calibration_choices"]),
            execution_route_count=len(document["consumer_export"]["execution_routes"]),
            implementation_sha256=sha256(Path(__file__).with_name("consumer_export.py")))
        write_json(manifest_path, manifest)
    readme = folder / "README.md"
    if readme.is_file():
        marker = "\n<!-- CONSUMER EXPORT -->\n"
        text = readme.read_text(encoding="utf-8").split(marker)[0]
        readme.write_text(text + marker + "\nControl applications read finished calibration choices, ordered commands, "
            "preview segments and execution routes from `consumer_export` in JSON/YAML. "
            "They do not construct routes. Execution requires assigned pressure profiles and explicit "
            "source-member coverage; geometry-only evidence does not grant either.\n", encoding="utf-8")
    inventory = folder / "files.sha256.json"
    write_json(inventory, {p.relative_to(folder).as_posix(): sha256(p)
                          for p in sorted(folder.rglob("*")) if p.is_file() and p != inventory})
    return dict(part=folder.name, calibration_choices=len(document["consumer_export"]["calibration_choices"]),
                execution_routes=len(document["consumer_export"]["execution_routes"]))


def stage_catalogue(repository, staging_root):
    source, destination = Path(repository).resolve(), Path(staging_root).resolve()
    if destination.exists():
        raise ValueError("Use a new staging directory")
    report = []
    for folder in sorted(source.iterdir()):
        if folder.name.startswith(".") or not folder.is_dir():
            continue
        if not (folder / f"{folder.name}_roadmap.json").is_file():
            continue
        staged = destination / folder.name
        shutil.copytree(folder, staged)
        report.append(upgrade_folder(staged))
        print(json.dumps(report[-1]), flush=True)
    destination.mkdir(parents=True, exist_ok=True)
    write_json(destination / "consumer_export_audit.json", dict(version=1, components=report))
    return report


def prepare_legacy_sidecars(root):
    """Preserve historical file hashes while adding offline-produced route records."""
    report = []
    for path in sorted(Path(root).glob("*/*_roadmap.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        attach_consumer_export(document)
        for source in (path, path.with_suffix(".yaml")):
            if source.is_file():
                write_json(source.with_name(source.name + ".consumer.json"),
                           dict(version=1, roadmap_sha256=sha256(source),
                                consumer_export=document["consumer_export"]))
        report.append(dict(component=path.parent.name,
                           calibration_choices=len(document["consumer_export"]["calibration_choices"])))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path)
    parser.add_argument("--staging-root", type=Path)
    parser.add_argument("--legacy-root", type=Path,
                        help="Write hash-bound sidecars beside byte-preserved historical exports")
    args = parser.parse_args()
    if args.legacy_root is not None:
        if args.repository is not None or args.staging_root is not None:
            parser.error("Use --legacy-root separately from staging arguments")
        for result in prepare_legacy_sidecars(args.legacy_root):
            print(json.dumps(result), flush=True)
    else:
        if args.repository is None or args.staging_root is None:
            parser.error("Specify both --repository and --staging-root")
        stage_catalogue(args.repository, args.staging_root)


if __name__ == "__main__":
    main()
