"""Import a pinned, published pose catalogue without reclassifying observations."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

from .generate import write_json


def normalize_catalogue(catalogue: dict, revision: str, source_path: str, digest: str) -> dict:
    """Keep source pose identities, representatives, groups and trial denominator."""
    data = deepcopy(catalogue)
    if data.get("schema_version") != 1 or data.get("condition") not in {"moving", "stationary"}:
        raise ValueError("Expected a current moving or stationary version 1 catalogue.")
    total = data["total_trials"]
    if isinstance(total, bool) or not isinstance(total, int) or total <= 0:
        raise ValueError("Invalid source trial total.")
    if sum(pose["count"] for pose in data["poses"]) != data["settled_trials"]:
        raise ValueError("Pose counts disagree with settled trials.")
    for pose in data["poses"]:
        frequency = 100 * pose["count"] / total
        if abs(pose["incidence_percent"] - frequency) > 1e-9:
            raise ValueError("Source incidence disagrees with the all-trial denominator.")
        pose["frequency_percent"] = pose["incidence_percent"]
    source = data["source"]
    data.update(completed_trials=total,
                geometry={"stl": PurePosixPath(source["mesh_path"]).name,
                          "stl_sha256": source["mesh_sha256"]},
                recognition=data["settings"]["recognition"],
                evaluation_phase="transport" if data["condition"] == "moving" else "stationary",
                frequency_denominator="all completed drop trials, including unsettled outcomes",
                source_provenance={"pose_repository": "https://github.com/match-BiBaZu/BiBaZu_Stable_ComponentPoses",
                                   "pose_revision": revision, "catalogue_path": source_path,
                                   "catalogue_sha256": digest, "condition": data["condition"],
                                   "classification_method": data["model"],
                                   "representative_policy": "unchanged published catalogue quaternion",
                                   **source})
    return data


def import_catalogues(repo: Path, output: Path, revision: str, condition: str) -> list[Path]:
    repo, output = repo.resolve(), output.resolve()
    if output.is_relative_to(repo) or repo.is_relative_to(output):
        raise ValueError("Import destination must be separate from the source repository.")
    command = ["git", "-c", f"safe.directory={repo.as_posix()}", "-C", str(repo)]
    commit = subprocess.check_output(command + ["rev-parse", "--verify", f"{revision}^{{commit}}"], text=True).strip()

    def blob(path):
        if PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts or "\\" in path:
            raise ValueError("Unsafe source path.")
        return subprocess.check_output(command + ["show", f"{commit}:{path}"])

    def verified(path, digest):
        content = blob(path)
        if hashlib.sha256(content).hexdigest() != digest:
            raise ValueError(f"Source checksum mismatch: {path}")
        return content

    index = json.loads(blob("index.json"))
    sources = []
    for entry in index["workpieces"]:
        part = entry["workpiece"]
        if PurePosixPath(part).name != part or part in {".", ".."} or "\\" in part:
            raise ValueError("Unsafe workpiece name.")
        path = entry["grouped_10000_catalogues"][condition]["path"]
        folder = str(PurePosixPath(path).parent)
        inventory = json.loads(blob(f"{folder}/files.sha256.json"))
        raw = verified(path, inventory["catalogue.json"])
        catalogue = json.loads(raw)
        if catalogue["workpiece"] != part or catalogue["condition"] != condition:
            raise ValueError("Catalogue identity disagrees with the source index.")
        normalized = normalize_catalogue(catalogue, commit, path, hashlib.sha256(raw).hexdigest())
        source = catalogue["source"]
        mesh = verified(source["mesh_path"], source["mesh_sha256"])
        config = verified(f'{source["run_dir"]}/config.json', source["config_sha256"])
        evidence_name = catalogue["grouping_evidence"]
        evidence = verified(f"{folder}/{evidence_name}", catalogue["grouping_evidence_sha256"])
        destination = output / part
        if destination.exists():
            raise ValueError(f"Choose a fresh import folder: {destination}")
        destination.mkdir(parents=True)
        (destination / "catalogue.json").write_bytes(raw)
        (destination / normalized["geometry"]["stl"]).write_bytes(mesh)
        (destination / "config.json").write_bytes(config)
        (destination / "grouping-evidence.json").write_bytes(evidence)
        write_json(destination / "poses.json", normalized)
        (destination / "README.md").write_text(
            f"# {part}: {condition}\n\nImported from pose revision `{commit}`.\n\n"
            f"Source: `{path}`. Original IDs, counts, groups and orientations are preserved.\n"
            "`catalogue.json` is the original published file; `poses.json` adapts field names for the roadmap generator.\n",
            encoding="utf-8")
        write_json(destination / "files.sha256.json", {
            item.name: hashlib.sha256(item.read_bytes()).hexdigest()
            for item in sorted(destination.iterdir()) if item.is_file()})
        sources.append(destination / "poses.json")
        print(json.dumps({"workpiece": part, "condition": condition, "poses": len(catalogue["poses"])}), flush=True)
    return sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--poses-repo", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--revision", default="origin/main")
    parser.add_argument("--condition", choices=("moving", "stationary"), required=True)
    args = parser.parse_args()
    import_catalogues(args.poses_repo, args.output_root, args.revision, args.condition)


if __name__ == "__main__":
    main()
