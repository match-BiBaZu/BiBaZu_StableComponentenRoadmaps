"""Frequency-independent geometric tipping resistance of observed poses.

This measures sampled, seated shortest-rotation paths to other recorded poses.
It is neither a minimum-energy-path proof nor a dynamic transport assessment.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
import os
from pathlib import Path
import tempfile

import numpy as np
from scipy.spatial.transform import Rotation

from ._engine.geometry import load_solid_mesh
from ._engine.symmetry import detect_rotational_symmetry
from .inputs import PoseSource, load_source, read_json, sha256

METHOD = "sampled_seated_escape_lift"
METHOD_VERSION = 1
ANGULAR_STEP_DEG = 0.1
THRESHOLDS_MM = {"fragile": 0.1, "resistant": 0.5}
_EQUIVALENT_ANGLE_RAD = 1e-6


class QualityCancelled(Exception):
    """The caller requested cancellation at a safe calculation boundary."""


def quality_label(lift_mm: float | None) -> str:
    if lift_mm is None:
        return "unknown"
    if not math.isfinite(lift_mm) or lift_mm < 0:
        raise ValueError("Escape lift must be finite and nonnegative.")
    # Avoid classifying an analytically exact threshold on its floating-point
    # rounding side. This tolerance is much smaller than mesh/sampling accuracy.
    if lift_mm < THRESHOLDS_MM["fragile"] - 1e-9:
        return "fragile"
    if lift_mm < THRESHOLDS_MM["resistant"] - 1e-9:
        return "marginal"
    return "resistant"


def _angle(config, key, default):
    value = config.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"Invalid {key} in source config.json.")
    return float(value)


def _symmetry(descriptor, mesh_path):
    symmetry_source = "saved_recognition"
    symbol = descriptor.get("symmetry_symbol")
    axis = descriptor.get("continuous_axis_part")
    raw_symmetry = descriptor.get("symmetry_quaternions_xyzw")
    if raw_symmetry is None:
        group = detect_rotational_symmetry(mesh_path, tolerance_mm=.05)
        raw_symmetry = Rotation.from_matrix(np.asarray([item.rotation_part_from_part for item in group.elements])).as_quat()
        axis, symbol = group.continuous_axis_part, group.symbol
        symmetry_source = "mesh_geometry"
    raw = np.asarray(raw_symmetry, dtype=float)
    if raw.ndim != 2 or raw.shape[1] != 4 or not len(raw) or not np.isfinite(raw).all():
        raise ValueError("Invalid symmetry quaternions for pose quality.")
    norms = np.linalg.norm(raw, axis=1)
    if np.any(norms < 1e-12):
        raise ValueError("Invalid symmetry quaternion length for pose quality.")
    # Identity is always available, including descriptors that omit it.
    symmetries = Rotation.from_quat(np.vstack(([0, 0, 0, 1], raw / norms[:, None]))).as_matrix()
    if axis is not None:
        axis = np.asarray(axis, dtype=float)
        if axis.shape != (3,) or not np.isfinite(axis).all() or np.linalg.norm(axis) < 1e-12:
            raise ValueError("Invalid continuous symmetry axis for pose quality.")
        axis = axis / np.linalg.norm(axis)
    return symmetries, axis, symmetry_source, symbol


def _relative_path(first, second, symmetries, continuous_axis):
    if continuous_axis is not None:
        u, v = first @ continuous_axis, second @ continuous_axis
        cross = np.cross(u, v)
        sine = float(np.linalg.norm(cross))
        cosine = float(np.clip(u @ v, -1, 1))
        angle = math.atan2(sine, cosine)
        if angle < _EQUIVALENT_ANGLE_RAD:
            return np.zeros(3)
        if sine < 1e-10:
            cross = np.cross(u, np.eye(3)[np.argmin(np.abs(u))])
        return cross / np.linalg.norm(cross) * angle
    candidates = Rotation.from_matrix((second @ symmetries) @ first.T).as_rotvec()
    return min(candidates, key=lambda rv: (float(np.linalg.norm(rv)), tuple(rv)))


def _sample_path(vertices, first, rotvec, gravity, check_cancel):
    """Return both directed barriers and peak fractions using bounded memory."""
    angle = float(np.degrees(np.linalg.norm(rotvec)))
    count = max(2, math.ceil(angle / ANGULAR_STEP_DEG) + 1)
    fractions = np.linspace(0.0, 1.0, count)
    # Two support-function arrays, each capped at about 4 MiB. Computing only
    # the wall/floor coordinates avoids materializing samples x vertices x 3.
    chunk = max(1, min(128, 524288 // max(1, len(vertices))))
    heights = np.empty(count)
    for start in range(0, count, chunk):
        check_cancel()
        rotation = Rotation.from_rotvec(fractions[start:start + chunk, None] * rotvec).as_matrix() @ first
        min_y = np.einsum("sj,vj->sv", rotation[:, 1, :], vertices, optimize=False).min(axis=1)
        min_z = np.einsum("sj,vj->sv", rotation[:, 2, :], vertices, optimize=False).min(axis=1)
        heights[start:start + chunk] = gravity[1] * min_y + gravity[2] * min_z
    if not np.isfinite(heights).all():
        raise ValueError("Non-finite seated height encountered during pose-quality analysis.")
    peak = int(np.argmax(heights))
    return (max(0.0, float(heights[peak] - heights[0])),
            max(0.0, float(heights[peak] - heights[-1])),
            angle * float(fractions[peak]), angle * (1.0 - float(fractions[peak])))


def _observations(source):
    data = read_json(source.path)
    if "poses" not in data:
        data = read_json(source.path.with_name("poses.json"))
    return data


def _groups(observations):
    groups = {str(row["id"]): str(row["group_id"]) for row in observations.get("poses", [])
              if row.get("group_id") is not None}
    for group in observations.get("groups", []):
        if isinstance(group, dict) and group.get("id") is not None:
            for member in group.get("members", []):
                groups.setdefault(str(member), str(group["id"]))
    return groups


def _saved_paths(source, observations, mesh_hash, config_hash, alpha, beta):
    """Reuse only checksum-verified ordinary paths with identical inputs.

    Scoped rolling/support-family models use different evidence semantics, so
    their paths are recalculated instead of assigning them invented meanings.
    """
    try:
        folder = source.path.parent
        catalogue_path = folder / "catalogue.json"
        provenance = observations.get("source_provenance", {})
        if not catalogue_path.is_file() or sha256(catalogue_path) != provenance.get("catalogue_sha256"):
            return {}, "No checksum-verified published catalogue beside the source."
        catalogue = read_json(catalogue_path)
        saved_source = catalogue["source"]
        settings = catalogue["settings"]
        if (saved_source["mesh_sha256"] != mesh_hash or saved_source["config_sha256"] != config_hash
                or settings["recognition"] != source.recognition
                or settings["transverse_angle_deg"] != alpha or settings["longitudinal_angle_deg"] != beta):
            return {}, "Saved path mesh, configuration or symmetry differs from the selected source."
        anchors = {str(row["id"]): np.asarray(row["quaternion_xyzw"], dtype=float) for row in catalogue["poses"]}
        for pose in source.poses:
            saved = anchors.get(pose.source_id)
            if saved is None or abs(float(saved @ np.asarray(pose.quaternion_xyzw)) / np.linalg.norm(saved)) < 1 - 1e-12:
                return {}, "Saved paths use different pose representatives."
        evidence_name = catalogue["grouping_evidence"]
        if Path(evidence_name).name != evidence_name:
            return {}, "Unsafe saved evidence filename."
        evidence_path = folder / evidence_name
        if not evidence_path.is_file() or sha256(evidence_path) != catalogue["grouping_evidence_sha256"]:
            return {}, "Saved grouping evidence checksum does not match."
        evidence = read_json(evidence_path)
        if evidence.get("model") != "observed-seated-geodesic-basins-v1":
            return {}, "Saved evidence uses a scoped model; ordinary paths are recalculated."
        if not 0 < evidence["sampling_step_deg"] <= ANGULAR_STEP_DEG:
            return {}, "Saved evidence angular sampling is coarser than the quality method."
        paths = {}
        for path in evidence["paths"]:
            values = [path.get(key) for key in ("angle_deg", "forward_barrier_mm", "reverse_barrier_mm")]
            if any(isinstance(v, bool) or not isinstance(v, (float, int)) or not math.isfinite(v) or v < 0 for v in values):
                continue
            key = (str(path["source"]), str(path["target"]))
            if key in paths or key[::-1] in paths:
                return {}, "Duplicate saved path evidence; paths are recalculated."
            paths[key] = path
        return paths, "Checksum-verified ordinary seated paths; missing paths are calculated."
    except (OSError, ValueError, TypeError, KeyError, ZeroDivisionError):
        return {}, "Saved evidence is unavailable or incompatible; paths are recalculated."


def analyze_pose_quality(source: PoseSource, *, mesh=None, progress=lambda message: None,
                         check_cancel=lambda: None) -> dict:
    """Classify every input pose independently of its frequency or export cutoff."""
    check_cancel()
    source_hash = sha256(source.path)
    observations_path = source.path if "poses" in read_json(source.path) else source.path.with_name("poses.json")
    observations_hash = sha256(observations_path)
    mesh_hash = sha256(source.mesh)
    config_path = source.path.with_name("config.json")
    config_hash = sha256(config_path) if config_path.is_file() else None
    alpha, beta = _angle(source.config, "alpha_deg", 45), _angle(source.config, "beta_deg", 0)
    symmetry, continuous_axis, symmetry_source, symmetry_symbol = _symmetry(source.recognition, source.mesh)
    mesh = load_solid_mesh(source.mesh) if mesh is None else mesh
    vertices = np.asarray(mesh.convex_hull.vertices, dtype=float) - np.asarray(mesh.center_mass, dtype=float)
    if vertices.ndim != 2 or vertices.shape[1] != 3 or not len(vertices) or not np.isfinite(vertices).all():
        raise ValueError("A finite solid convex hull is required for pose quality.")
    chute = Rotation.from_euler("y", beta, degrees=True) * Rotation.from_euler("x", alpha, degrees=True)
    gravity = chute.inv().apply([0.0, 0.0, -1.0])
    observations = _observations(source)
    groups = _groups(observations)
    saved, reuse_note = _saved_paths(source, observations, mesh_hash, config_hash, alpha, beta)
    ordered = sorted(source.poses, key=lambda pose: pose.source_id)
    rotations = {pose.source_id: Rotation.from_quat(pose.quaternion_xyzw).as_matrix() for pose in ordered}
    poses = {pose.source_id: {
        "label": "unknown", "escape_lift_mm": None, "escape_target_source_id": None,
        "escape_within_group": None, "source_group_id": groups.get(pose.source_id),
        "path_angle_deg": None, "peak_angle_deg": None, "path_origin": None,
        "observed_count": pose.count, "observed_frequency_percent": pose.frequency_percent,
        "reason": "No symmetry-distinct recorded target pose is available.",
    } for pose in ordered}
    reused = calculated = equivalent = 0
    pair_total = len(ordered) * (len(ordered) - 1) // 2
    pair_done = 0
    progress(f"Assessing geometric quality for all {len(ordered)} observed poses ({pair_total} candidate paths)")

    def consider(first, second, lift, angle, peak_angle, origin):
        entry = poses[first]
        previous = entry["escape_lift_mm"]
        if previous is not None and (lift, second) >= (previous, entry["escape_target_source_id"]):
            return
        within = groups[first] == groups[second] if first in groups and second in groups else None
        entry.update(label=quality_label(lift), escape_lift_mm=float(lift),
                     escape_target_source_id=second, escape_within_group=within,
                     path_angle_deg=float(angle), peak_angle_deg=peak_angle, path_origin=origin,
                     reason="Movement stays within the existing pose group (rocking); this does not classify the whole group."
                     if within else "Sampled geometric escape to another recorded pose; not a dynamic stability guarantee.")

    for index, first in enumerate(ordered):
        first_id = first.source_id
        rotation = rotations[first_id]
        for second in ordered[index + 1:]:
            check_cancel()
            second_id = second.source_id
            rv = _relative_path(rotation, rotations[second_id], symmetry, continuous_axis)
            angle_rad = float(np.linalg.norm(rv))
            pair_done += 1
            if angle_rad <= _EQUIVALENT_ANGLE_RAD:
                equivalent += 1
                continue
            angle = math.degrees(angle_rad)
            evidence = saved.get((first_id, second_id))
            reverse_evidence = False
            if evidence is None:
                evidence = saved.get((second_id, first_id))
                reverse_evidence = evidence is not None
            if evidence is not None and abs(evidence["angle_deg"] - angle) <= 1e-6:
                forward, backward = evidence["forward_barrier_mm"], evidence["reverse_barrier_mm"]
                if reverse_evidence:
                    forward, backward = backward, forward
                peak_forward = peak_backward = None
                origin = "verified_saved_path"
                reused += 1
            else:
                forward, backward, peak_forward, peak_backward = _sample_path(vertices, rotation, rv, gravity, check_cancel)
                origin = "calculated_path"
                calculated += 1
            consider(first_id, second_id, forward, angle, peak_forward, origin)
            consider(second_id, first_id, backward, angle, peak_backward, origin)
        progress(f"Pose quality checked {index + 1}/{len(ordered)} ({pair_done}/{pair_total} paths)")
    check_cancel()
    if (sha256(source.path) != source_hash or sha256(observations_path) != observations_hash
            or sha256(source.mesh) != mesh_hash
            or (sha256(config_path) if config_path.is_file() else None) != config_hash):
        raise ValueError("Source inputs changed during pose-quality analysis; refresh the source and retry.")
    counts = Counter(entry["label"] for entry in poses.values())
    return {
        "schema_version": 1, "method": METHOD, "method_version": METHOD_VERSION,
        "workpiece": source.workpiece, "source_sha256": source_hash, "observations_sha256": observations_hash,
        "mesh_sha256": mesh_hash,
        "config_sha256": config_hash, "angular_step_deg": ANGULAR_STEP_DEG,
        "thresholds_mm": dict(THRESHOLDS_MM), "alpha_deg": alpha, "beta_deg": beta,
        "symmetry_source": symmetry_source, "symmetry_symbol": symmetry_symbol,
        "frequency_independent": True, "automatic_filtering": False, "uniform_density_assumed": True,
        "interpretation": "Smallest sampled COM lift along symmetry-aware, two-plane-seated shortest rotations to recorded poses. "
                          "This is an evaluated-path estimate, not a proven minimum escape energy or dynamic transport assessment. "
                          "Frequency and pose-group incidence are unchanged; within-group rocking does not classify the whole group.",
        "path_counts": {"reused": reused, "calculated": calculated, "symmetry_equivalent": equivalent},
        "saved_path_reuse": reuse_note,
        "label_counts": {label: counts[label] for label in ("fragile", "marginal", "resistant", "unknown")},
        "poses": poses,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cancel-file", type=Path)
    args = parser.parse_args()

    def emit(**event):
        print(json.dumps(event, ensure_ascii=False, allow_nan=False), flush=True)

    def check_cancel():
        if args.cancel_file is not None and args.cancel_file.exists():
            raise QualityCancelled()

    temporary = None
    try:
        check_cancel()
        destination = args.output.expanduser().resolve()
        source_file = args.source.expanduser().resolve()
        if destination.is_relative_to(source_file.parent):
            raise ValueError("Save the quality report outside the input catalogue folder; source inputs are read-only.")
        if destination.is_file() and destination.name in {
                "poses.json", "pose_registry.json", "catalogue.json", "config.json", "grouping-evidence.json",
                "files.sha256.json", "manifest.json"}:
            raise ValueError("The quality report cannot overwrite an existing catalogue or inventory file.")
        source = load_source(source_file)
        report = analyze_pose_quality(source, progress=lambda message: emit(message=message), check_cancel=check_cancel)
        destination.parent.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(prefix=".pose-quality-", suffix=".tmp", dir=destination.parent)
        temporary = Path(name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
        check_cancel()
        os.replace(temporary, destination)
        emit(status="completed", report_path=str(destination))
        return 0
    except QualityCancelled:
        emit(status="cancelled", message="Pose-quality analysis cancelled.")
        return 0
    except Exception as error:
        emit(status="failed", message=str(error))
        return 1
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
