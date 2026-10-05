"""Read simulator exports, keeping every source orientation and pose ID."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import re

import numpy as np


class EmptyPoseList(ValueError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path.name}.")
    return data


@dataclass(frozen=True)
class ObservedPose:
    source_id: str
    quaternion_xyzw: tuple[float, float, float, float]
    count: int | None
    frequency_percent: float
    source_index: int

    def original_number(self) -> int:
        match = re.search(r"(?:^|_)(\d+)$", self.source_id)
        if not match:
            raise ValueError(f"Pose {self.source_id!r} has no numeric suffix. Enable frequency numbering.")
        return int(match[1])


@dataclass(frozen=True)
class PoseSource:
    path: Path
    workpiece: str
    mesh: Path
    poses: tuple[ObservedPose, ...]
    recognition: dict
    config: dict
    snapshot_files: tuple[Path, ...]
    frequency_denominator: str


def discover_sources(path: str | Path) -> list[Path]:
    path = Path(path).expanduser().resolve()
    if path.is_file():
        if path.suffix.lower() != ".json":
            raise ValueError("Choose a poses.json or pose_registry.json file.")
        return [path]
    if not path.is_dir():
        raise ValueError("Choose an existing pose JSON file or poses repository folder.")
    candidates = {}
    for name in ("pose_registry.json", "poses.json"):
        for candidate in path.rglob(name):
            if any(p.startswith(".") for p in candidate.relative_to(path).parts):
                continue
            # Prefer observations when both files exist; do not process twice.
            candidates[candidate.parent] = candidate
    return sorted(candidates.values(), key=lambda p: p.as_posix().casefold())


def _rows(data: dict, key: str, quaternion_key: str) -> list[dict]:
    rows = data.get(key)
    if not isinstance(rows, list):
        raise ValueError(f"Expected a '{key}' list in the JSON file.")
    if not rows:
        raise EmptyPoseList("The simulator export contains no observed poses.")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or isinstance(row.get("id"), bool) or not isinstance(row.get("id"), (str, int)):
            raise ValueError("Every pose must have a string or integer ID.")
        pose_id = str(row["id"])
        if not pose_id.strip() or pose_id in seen:
            raise ValueError(f"Empty or duplicate pose ID: {pose_id!r}.")
        seen.add(pose_id)
        try:
            quat = np.asarray(row.get(quaternion_key), dtype=float)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid xyzw quaternion for pose {pose_id}.") from error
        if quat.shape != (4,) or not np.isfinite(quat).all():
            raise ValueError(f"Expected four finite xyzw quaternion components for pose {pose_id}.")
        norm = float(np.linalg.norm(quat))
        if not math.isfinite(norm) or norm < 1e-12:
            raise ValueError(f"Invalid quaternion length for pose {pose_id}.")
    return rows


def load_source(path: str | Path) -> PoseSource:
    path = Path(path).expanduser().resolve()
    data = read_json(path)
    if data.get("schema_version", 1) != 1:
        raise ValueError("Only version 1 simulator pose exports are supported.")
    registry = "entries" in data and "poses" not in data
    rows = _rows(data, "entries" if registry else "poses",
                 "anchor_quaternion_xyzw" if registry else "quaternion_xyzw")
    observed_path = path.with_name("poses.json") if registry else path
    if not observed_path.is_file():
        raise ValueError("A registry needs the neighboring poses.json for observed frequencies.")
    observations = read_json(observed_path) if registry else data
    observed_rows = _rows(observations, "poses", "quaternion_xyzw")
    by_id = {str(row["id"]): row for row in observed_rows}
    if registry and not set(by_id).intersection(str(row["id"]) for row in rows):
        raise ValueError("The registry and poses.json have no pose IDs in common.")
    geometry = observations.get("geometry", {})
    if not isinstance(geometry, dict):
        raise ValueError("Pose geometry must be a JSON object.")
    workpiece = observations.get("workpiece")
    mesh_name = geometry.get("stl")
    if workpiece is None:
        prefixes = {str(row["id"]).rsplit("_", 1)[0] for row in rows if "_" in str(row["id"])}
        workpiece = Path(mesh_name).stem if isinstance(mesh_name, str) else (prefixes.pop() if len(prefixes) == 1 else path.parent.name)
    if not isinstance(workpiece, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", workpiece):
        raise ValueError("Invalid component name in the pose file.")
    if workpiece.upper() in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}:
        raise ValueError("The component name is reserved by Windows.")
    if mesh_name is not None and (not isinstance(mesh_name, str) or Path(mesh_name).name != mesh_name):
        raise ValueError("The source STL must be beside the pose files.")
    meshes = [p for p in path.parent.iterdir() if p.is_file() and p.suffix.lower() == ".stl"
              and p.stem.casefold() == workpiece.casefold()]
    mesh = path.parent / mesh_name if mesh_name else (meshes[0] if len(meshes) == 1 else None)
    if mesh is None or not mesh.is_file() or mesh.suffix.lower() != ".stl":
        raise ValueError(f"Missing matching {workpiece}.stl beside the pose JSON.")
    expected = geometry.get("stl_sha256")
    registry_hash = data.get("mesh_sha256") if registry else None
    actual = sha256(mesh)
    for stored in (expected, registry_hash):
        if stored is not None and (not isinstance(stored, str) or stored.lower() != actual):
            raise ValueError("The STL hash does not match the pose export/registry.")
    recognition = observations.get("recognition", {})
    if not isinstance(recognition, dict) or recognition.get("quaternion_order", "xyzw") != "xyzw" or recognition.get("rotation", "part_to_chute") != "part_to_chute":
        raise ValueError("Expected part-to-chute xyzw quaternions.")
    counts = []
    for row in observed_rows:
        count = row.get("count")
        if count is not None and (isinstance(count, bool) or not isinstance(count, int) or count < 0):
            raise ValueError(f"Invalid observation count for pose {row['id']}.")
        counts.append(count)
    trials = observations.get("completed_trials")
    if trials is not None and (isinstance(trials, bool) or not isinstance(trials, int) or trials <= 0):
        raise ValueError("completed_trials must be a positive integer.")
    denominator = trials or (sum(counts) if all(c is not None for c in counts) else 0)
    denominator_name = "all completed trials" if trials else "all listed observation counts"
    poses = []
    for index, row in enumerate(rows):
        source_id = str(row["id"])
        observed = by_id.get(source_id)
        count = observed.get("count") if observed else 0
        frequency = observed.get("frequency_percent") if observed else 0.0
        if frequency is None:
            if count is None or not denominator:
                raise ValueError(f"Missing usable frequencies for pose {source_id}.")
            frequency = 100.0 * count / denominator
        if isinstance(frequency, bool) or not isinstance(frequency, (int, float)) or not math.isfinite(frequency) or not 0 <= frequency <= 100:
            raise ValueError(f"Invalid percentage for pose {source_id}.")
        quat = np.asarray(row["anchor_quaternion_xyzw" if registry else "quaternion_xyzw"], dtype=float)
        quat /= np.linalg.norm(quat)
        poses.append(ObservedPose(source_id, tuple(float(q) for q in quat), count, float(frequency), index))
    config_path = path.with_name("config.json")
    config = read_json(config_path) if config_path.is_file() else {}
    files = {path, observed_path, mesh}
    other_registry = path.with_name("pose_registry.json")
    if other_registry.is_file():
        files.add(other_registry)
    if config_path.is_file():
        files.add(config_path)
    return PoseSource(path, workpiece, mesh.resolve(), tuple(poses), recognition, config,
                      tuple(sorted(files)), observations.get("frequency_denominator", denominator_name))


def select_poses(source: PoseSource, minimum_percent: float, renumber: bool) -> tuple[list[tuple[ObservedPose, int]], list[ObservedPose]]:
    if not math.isfinite(minimum_percent) or not 0 <= minimum_percent <= 100:
        raise ValueError("Minimum frequency must be between 0 and 100 percent.")
    retained = [pose for pose in source.poses if pose.frequency_percent >= minimum_percent]
    removed = [pose for pose in source.poses if pose.frequency_percent < minimum_percent]
    if not retained:
        return [], removed
    if renumber:
        retained.sort(key=lambda pose: (-pose.frequency_percent, pose.source_id))
        numbered = list(zip(retained, range(len(retained))))
    else:
        numbered = [(pose, pose.original_number()) for pose in retained]
        if len({number for _, number in numbered}) != len(numbered):
            raise ValueError("Source numeric pose suffixes overlap. Enable frequency numbering.")
    return numbered, removed
