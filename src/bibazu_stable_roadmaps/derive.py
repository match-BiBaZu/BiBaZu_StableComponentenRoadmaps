"""Derive observed pose frequencies from checksum-verified simulation trials.

Complete-link classification follows Dashas Drop Sim's PoseResolver at
72b1ba08aa9b317804cd60e1e2ae6e636910f3fd (MIT, copyright 2026 match-BiBaZu).
Classification is post-processing; the original ungrouped runs remain intact.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from scipy.spatial.transform import Rotation

from .inputs import read_json, sha256

METHOD = "symmetry_aware_complete_link"
TOLERANCE_DEG = 5.0


def _canonical(quaternion):
    signed = quaternion.copy()
    for value in signed[::-1]:
        if abs(float(value)) > 1e-12:
            if value < 0:
                signed *= -1
            break
    return tuple(float(value) for value in np.round(signed, 12))


def cluster_orientations(quaternions, recognition, tolerance_deg=TOLERANCE_DEG):
    """Deterministic complete-link classes, with the simulator's symmetry metric."""
    quats = np.asarray(quaternions, dtype=float)
    if quats.size == 0:
        return []
    if quats.ndim != 2 or quats.shape[1] != 4 or not np.isfinite(quats).all():
        raise ValueError("Expected finite xyzw quaternions with shape (n, 4).")
    norms = np.linalg.norm(quats, axis=1)
    if np.any(norms < 1e-12) or not 0 < tolerance_deg <= 180:
        raise ValueError("Invalid quaternion or angular tolerance.")
    quats = quats / norms[:, None]
    count = len(quats)
    if count == 1:
        return [0]
    axis = recognition.get("continuous_axis_part")
    if axis is None:
        symmetry = Rotation.from_quat(recognition["symmetry_quaternions_xyzw"])
        variants = [(Rotation.from_quat(quat) * symmetry).as_quat() for quat in quats]
        keys = [min(_canonical(variant) for variant in item) for item in variants]
    else:
        axis = np.asarray(axis, dtype=float)
        if axis.shape != (3,) or not np.isfinite(axis).all() or np.linalg.norm(axis) < 1e-12:
            raise ValueError("Invalid directed continuous symmetry axis.")
        axes = Rotation.from_quat(quats).apply(axis / np.linalg.norm(axis))
        keys = [tuple(float(value) for value in np.round(item, 12)) for item in axes]
    order = sorted(range(count), key=lambda index: keys[index])
    sorted_quats = quats[order]
    if axis is None:
        distances = np.zeros((count, count), dtype=float)
        for row, original_index in enumerate(order):
            dots = np.abs(variants[original_index] @ sorted_quats.T)
            distances[row] = np.degrees(2 * np.arccos(np.clip(np.max(dots, axis=0), 0, 1)))
    else:
        sorted_axes = axes[order]
        distances = np.degrees(np.arccos(np.clip(sorted_axes @ sorted_axes.T, -1, 1)))
    distances = np.maximum(distances, distances.T)
    np.fill_diagonal(distances, 0)
    tree = linkage(squareform(distances, checks=False), method="complete")
    raw = fcluster(tree, t=tolerance_deg, criterion="distance")
    first_key = {label: min(keys[order[index]] for index in np.flatnonzero(raw == label)) for label in np.unique(raw)}
    renumber = {label: index for index, label in enumerate(sorted(first_key, key=first_key.get))}
    labels = [0] * count
    for sorted_index, original_index in enumerate(order):
        labels[original_index] = renumber[int(raw[sorted_index])]
    return labels


def build_catalogue(rows, workpiece, study, phase, geometry, recognition, provenance):
    """Count settled observations; representatives are actual recorded trials."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", workpiece):
        raise ValueError("Invalid workpiece name.")
    if phase not in {"transport", "after_belt_stop"}:
        raise ValueError("Choose transport or after_belt_stop observations.")
    trials = len(rows)
    if trials == 0 or {row["trial"] for row in rows} != set(range(trials)):
        raise ValueError("Missing or duplicate trial IDs.")
    if phase == "transport":
        observations = rows
    else:
        observations = [{**(row.get("stop_observation") or {"status": "not_observed"}),
                         "trial": row["trial"]} for row in rows]
    settled = sorted((row for row in observations if row["status"] == "settled"), key=lambda row: row["trial"])
    labels = cluster_orientations([row["final_quat_xyzw"] for row in settled], recognition)
    groups = {}
    for row, label in zip(settled, labels):
        groups.setdefault(label, []).append(row)
    poses = []
    for label, members in sorted(groups.items()):
        first = members[0]
        poses.append({"id": f"{workpiece}_{study}_{phase}_{label + 1:04d}",
                      "count": len(members), "frequency_percent": 100 * len(members) / trials,
                      "frequency_settled_percent": 100 * len(members) / len(settled),
                      "quaternion_xyzw": first["final_quat_xyzw"], "representative_trial": first["trial"],
                      "member_trial_ids": [row["trial"] for row in members],
                      "reference_quaternions_xyzw": [row["final_quat_xyzw"] for row in members]})
    poses.sort(key=lambda pose: (-pose["count"], pose["id"]))
    return {"schema_version": 1, "workpiece": workpiece, "completed_trials": trials,
            "settled_trials": len(settled), "status_counts": dict(Counter(row["status"] for row in observations)),
            "evaluation_phase": phase, "geometry": geometry, "recognition": recognition,
            "frequency_denominator": "all completed drop trials, including unsettled outcomes",
            "source_provenance": {**provenance, "evaluation_phase": phase,
                "classification_method": METHOD, "classification_tolerance_deg": TOLERANCE_DEG,
                "representative_policy": "first recorded trial in each complete-link class",
                "simulation_grouping_enabled": False, "derivation_version": 1}, "poses": poses}


def read_trials(folder):
    """Verify every archived member before using the recorded orientations."""
    archive_path = folder / "simulation_results.tar.xz"
    if sha256(archive_path) != read_json(folder / "files.sha256.json")[archive_path.name]:
        raise ValueError(f"Archive checksum mismatch: {archive_path}")
    expected = read_json(folder / "archive_contents.sha256.json")
    actual, captured = {}, {}
    with tarfile.open(archive_path, "r|xz") as archive:
        for member in archive:
            if not member.isfile() or Path(member.name).name != member.name or member.name in actual:
                raise ValueError("Unexpected archive member.")
            with archive.extractfile(member) as stream:
                if member.name in {"trials.jsonl", "config.json", "manifest.json"}:
                    content = stream.read()
                    actual[member.name] = hashlib.sha256(content).hexdigest()
                    captured[member.name] = content
                else:
                    actual[member.name] = hashlib.file_digest(stream, "sha256").hexdigest()
    if actual != expected:
        raise ValueError(f"Archived member checksums differ: {folder}")
    return ([json.loads(line) for line in captured["trials.jsonl"].splitlines() if line.strip()],
            json.loads(captured["config.json"]), json.loads(captured["manifest.json"]))


def _write_json(path, value):
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode())


def derive_one(repo, output_root, entry, revision):
    part = entry["workpiece"]
    indexed = entry["ungrouped_10000_simulations"]["100mm_s"]
    folder = (repo / indexed["path"]).resolve()
    if not folder.is_relative_to(repo / part):
        raise ValueError("Run directory escapes the selected workpiece.")
    phase = "after_belt_stop" if part == "Kf1i" else "transport"
    recognition_path = repo / part / ("poses_after_stop.json" if phase == "after_belt_stop" else "poses.json")
    historical = read_json(recognition_path)
    provenance = {"pose_repository": "https://github.com/match-BiBaZu/BiBaZu_Stable_ComponentPoses",
                  "pose_revision": revision, "run_directory": indexed["path"], "condition": "100mm_s",
                  "source_archive_sha256": sha256(folder / "simulation_results.tar.xz"),
                  "source_signature": indexed["signature"], "simulator_commit": indexed["simulator_commit"],
                  "symmetry_source": recognition_path.relative_to(repo).as_posix(),
                  "symmetry_source_sha256": sha256(recognition_path)}
    destination = output_root / part
    if destination.exists():
        previous = read_json(destination / "poses.json")
        inventory = read_json(destination / "files.sha256.json")
        if {p.name for p in destination.iterdir()} != set(inventory) | {"files.sha256.json"} or any(sha256(destination / name) != digest for name, digest in inventory.items()):
            raise ValueError(f"Derived catalogue has manual changes: {part}")
        recorded = previous.get("source_provenance", {})
        if all(recorded.get(key) == value for key, value in provenance.items()) and recorded.get("derivation_version") == 1:
            return {"part": part, "status": "reused", "pose_count": len(previous["poses"])}
        raise ValueError(f"Choose a new catalogue output folder for changed inputs: {part}")
    rows, config, manifest = read_trials(folder)
    summary = read_json(folder / "summary.json")
    if len(rows) != 10000 or config["group_poses"] is not False or config["belt_mode"] != "running":
        raise ValueError("Expected a completed ungrouped 10,000-drop moving-belt run.")
    if dict(Counter(row["status"] for row in rows)) != summary["status_counts"]:
        raise ValueError("Trial statuses disagree with the published summary.")
    mesh = repo / part / f"{part}.stl"
    if sha256(mesh) != manifest["mesh_source_sha256"] or sha256(mesh) != historical["geometry"]["stl_sha256"]:
        raise ValueError("Saved symmetry and trial mesh hashes differ.")
    geometry = {"stl": mesh.name, "stl_sha256": sha256(mesh),
                "center_mass_source_mm": manifest["center_mass_source_mm"]}
    data = build_catalogue(rows, part, folder.parent.name, phase, geometry, historical["recognition"], provenance)
    expected_settled = summary["settled_trials"] if phase == "transport" else summary["belt_stop_observation"]["status_counts"].get("settled", 0)
    if data["settled_trials"] != expected_settled:
        raise ValueError("Derived settlement counts differ from the recorded phase.")
    with tempfile.TemporaryDirectory(prefix=".catalogue-stage-", dir=output_root) as temporary:
        staging = Path(temporary) / part
        staging.mkdir()
        shutil.copyfile(mesh, staging / mesh.name)
        portable = deepcopy(config)
        portable.update(mesh_path=mesh.name, output_dir="./local_results")
        _write_json(staging / "config.json", portable)
        _write_json(staging / "poses.json", data)
        _write_json(staging / "pose_registry.json", {"schema_version": 1, "mesh_sha256": sha256(mesh),
            "entries": [{"id": pose["id"], "anchor_quaternion_xyzw": pose["quaternion_xyzw"]} for pose in data["poses"]]})
        (staging / "README.md").write_text(
            f"# {part}: derived {phase} pose catalogue\n\n"
            f"{data['settled_trials']:,} settled observations out of 10,000 drops; {len(data['poses'])} complete-link classes. "
            "Classification uses the recorded part symmetry and a 5° maximum within-class angular distance. "
            "The representative is an actual observed trial. Frequencies use all 10,000 completed drops.\n\n"
            f"Source: `{indexed['path']}`, pose repository revision `{revision}`. "
            "Source archive hashes, trial memberships, and reference orientations are recorded in poses.json.\n",
            encoding="utf-8")
        _write_json(staging / "files.sha256.json", {p.name: sha256(p) for p in sorted(staging.iterdir()) if p.is_file()})
        staging.replace(destination)
    return {"part": part, "status": "completed", "evaluation_phase": phase,
            "settled_trials": data["settled_trials"], "pose_count": len(data["poses"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--poses-repo", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    repo, output = args.poses_repo.resolve(), args.output_root.resolve()
    if output == repo or output.is_relative_to(repo):
        raise ValueError("Derived output must be outside the source poses repository.")
    revision = subprocess.check_output(["git", "-c", f"safe.directory={repo.as_posix()}", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    output.mkdir(parents=True, exist_ok=True)
    entries = read_json(repo / "index.json")["workpieces"]
    if len(entries) != 39:
        raise ValueError("Expected all 39 workpieces in the completed study index.")
    for index, entry in enumerate(entries, start=1):
        print(json.dumps({"part": entry["workpiece"], "status": "classifying", "index": index, "total": len(entries)}), flush=True)
        result = derive_one(repo, output, entry, revision)
        print(json.dumps({**result, "index": index, "total": len(entries)}), flush=True)
    print(json.dumps({"status": "finished", "parts": len(entries), "pose_revision": revision}), flush=True)


if __name__ == "__main__":
    main()
