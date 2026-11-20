from dataclasses import replace
import json
import math
import subprocess
import sys

import numpy as np
import pytest
from scipy.spatial.transform import Rotation
import trimesh

from bibazu_stable_roadmaps.inputs import load_source, sha256
from bibazu_stable_roadmaps.quality import analyze_pose_quality, quality_label, _sample_path


def source_for(tmp_path, *, quaternions, extents=(40, 30, 2), alpha=0, beta=0, symmetry=None, axis=None):
    folder = tmp_path / "poses"
    folder.mkdir()
    mesh = folder / "Test.stl"
    trimesh.creation.box(extents=extents).export(mesh)
    data = {"schema_version": 1, "workpiece": "Test", "completed_trials": 100,
            "geometry": {"stl": mesh.name, "stl_sha256": sha256(mesh)},
            "recognition": {"quaternion_order": "xyzw", "rotation": "part_to_chute",
                            "symmetry_quaternions_xyzw": symmetry or [[0, 0, 0, 1]],
                            "continuous_axis_part": axis},
            "poses": [{"id": f"Test_{index:04}", "count": 99 if index == 0 else 1,
                       "frequency_percent": 99 if index == 0 else 1,
                       "quaternion_xyzw": list(quat), "group_id": "G0"}
                      for index, quat in enumerate(quaternions)]}
    path = folder / "poses.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    (folder / "config.json").write_text(json.dumps({"alpha_deg": alpha, "beta_deg": beta}), encoding="utf-8")
    return load_source(path)


def test_thin_upright_pose_is_fragile_and_flat_pose_resistant_without_frequency_bias(tmp_path):
    source = source_for(tmp_path, quaternions=Rotation.from_euler("y", [[90], [0]], degrees=True).as_quat())
    original = source.path.read_bytes()
    report = analyze_pose_quality(source)
    upright, flat = report["poses"].values()
    diagonal = math.hypot(20, 1)
    assert upright["escape_lift_mm"] == pytest.approx(diagonal - 20, abs=2e-5)
    assert flat["escape_lift_mm"] == pytest.approx(diagonal - 1, abs=2e-5)
    assert upright["label"] == "fragile" and flat["label"] == "resistant"
    assert upright["escape_target_source_id"] == "Test_0001"
    assert upright["escape_within_group"] is True
    assert source.path.read_bytes() == original
    modified = replace(source, poses=tuple(replace(p, count=1, frequency_percent=0.01) for p in source.poses))
    second = analyze_pose_quality(modified)
    assert [(p["label"], p["escape_lift_mm"]) for p in second["poses"].values()] == [
        (p["label"], p["escape_lift_mm"]) for p in report["poses"].values()]


def test_paths_beyond_the_old_sixty_degree_guard_are_evaluated(tmp_path):
    source = source_for(tmp_path, quaternions=Rotation.from_euler("y", [[0], [120]], degrees=True).as_quat())
    report = analyze_pose_quality(source)
    assert report["path_counts"]["calculated"] == 1
    assert report["poses"]["Test_0000"]["path_angle_deg"] == pytest.approx(120)
    assert report["poses"]["Test_0000"]["label"] != "unknown"


@pytest.mark.parametrize("value,label", [(0, "fragile"), (.099, "fragile"), (.1, "marginal"),
                                       (.499, "marginal"), (.5, "resistant"), (None, "unknown")])
def test_threshold_boundaries(value, label):
    assert quality_label(value) == label


@pytest.mark.parametrize("value", [-1, float("nan"), float("inf")])
def test_invalid_barriers_are_rejected(value):
    with pytest.raises(ValueError):
        quality_label(value)


def test_single_or_symmetry_equivalent_pose_has_unknown_quality(tmp_path):
    quats = Rotation.from_euler("z", [[0], [180]], degrees=True).as_quat()
    source = source_for(tmp_path, quaternions=quats, symmetry=quats.tolist())
    report = analyze_pose_quality(source)
    assert report["path_counts"]["symmetry_equivalent"] == 1
    assert all(row["label"] == "unknown" and row["escape_lift_mm"] is None for row in report["poses"].values())
    one = analyze_pose_quality(replace(source, poses=source.poses[:1]))
    assert one["poses"]["Test_0000"]["label"] == "unknown"


def test_directed_continuous_symmetry_ignores_spin_but_not_axis_reversal(tmp_path):
    quats = Rotation.from_euler("xyz", [[0, 0, 0], [0, 0, 90], [180, 0, 0]], degrees=True).as_quat()
    source = source_for(tmp_path, quaternions=quats, extents=(20, 20, 40), axis=[0, 0, 1])
    report = analyze_pose_quality(source)
    assert report["path_counts"]["symmetry_equivalent"] == 1
    assert report["path_counts"]["calculated"] == 2
    assert report["poses"]["Test_0000"]["escape_target_source_id"] == "Test_0002"
    assert report["poses"]["Test_0000"]["path_angle_deg"] == pytest.approx(180)


def test_missing_recognition_uses_mesh_symmetry_instead_of_inventing_an_escape(tmp_path):
    quats = Rotation.from_euler("x", [[0], [180]], degrees=True).as_quat()
    source = source_for(tmp_path, quaternions=quats)
    report = analyze_pose_quality(replace(source, recognition={}))
    assert report["symmetry_source"] == "mesh_geometry"
    assert report["path_counts"]["symmetry_equivalent"] == 1
    assert all(row["label"] == "unknown" for row in report["poses"].values())


def test_inclined_belt_and_wall_height_matches_explicit_seating():
    vertices = np.asarray(trimesh.creation.box(extents=(10, 20, 30)).vertices) + [2, -3, 1]
    first = Rotation.from_euler("xyz", [10, 20, 30], degrees=True).as_matrix()
    rv = Rotation.from_euler("x", 90, degrees=True).as_rotvec()
    gravity = (Rotation.from_euler("y", 13, degrees=True) * Rotation.from_euler("x", 45, degrees=True)).inv().apply([0, 0, -1])
    forward, reverse, _, _ = _sample_path(vertices, first, rv, gravity, lambda: None)
    angles = np.linspace(0, 1, 901)
    rotations = Rotation.from_rotvec(angles[:, None] * rv).as_matrix() @ first
    heights = []
    for rotation in rotations:
        points = vertices @ rotation.T
        translation = np.array([0, -points[:, 1].min(), -points[:, 2].min()])
        heights.append(-float(gravity @ translation))
    assert forward == pytest.approx(max(heights) - heights[0])
    assert reverse == pytest.approx(max(heights) - heights[-1])


def test_discrete_symmetric_representatives_and_quaternion_sign_do_not_change_score(tmp_path):
    symmetry = Rotation.from_euler("z", [[0], [180]], degrees=True)
    quats = Rotation.from_euler("y", [[0], [90]], degrees=True).as_quat()
    source = source_for(tmp_path, quaternions=quats, symmetry=symmetry.as_quat().tolist())
    first = analyze_pose_quality(source)
    varied = tuple(replace(p, quaternion_xyzw=tuple(-(Rotation.from_quat(p.quaternion_xyzw) * symmetry[1]).as_quat())) for p in source.poses)
    second = analyze_pose_quality(replace(source, poses=varied))
    for key, entry in first["poses"].items():
        assert second["poses"][key]["escape_lift_mm"] == pytest.approx(entry["escape_lift_mm"])
        assert second["poses"][key]["label"] == entry["label"]


def test_cancellation_is_checked_inside_long_paths(tmp_path):
    source = source_for(tmp_path, quaternions=Rotation.from_euler("y", [[0], [180]], degrees=True).as_quat())
    calls = 0
    def cancel():
        nonlocal calls
        calls += 1
        if calls == 4:
            raise RuntimeError("cancelled")
    with pytest.raises(RuntimeError, match="cancelled"):
        analyze_pose_quality(source, check_cancel=cancel)
    assert calls == 4


def test_verified_evidence_reuse_and_checksum_mismatch_recalculation(tmp_path):
    source = source_for(tmp_path, quaternions=Rotation.from_euler("y", [[90], [0]], degrees=True).as_quat())
    initial = analyze_pose_quality(source)
    a, b = initial["poses"]["Test_0000"], initial["poses"]["Test_0001"]
    evidence = {"model": "observed-seated-geodesic-basins-v1", "sampling_step_deg": .1,
                "paths": [{"source": "Test_0000", "target": "Test_0001", "angle_deg": 90,
                           "forward_barrier_mm": a["escape_lift_mm"], "reverse_barrier_mm": b["escape_lift_mm"]}]}
    folder = source.path.parent
    evidence_path = folder / "grouping-evidence.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    data = json.loads(source.path.read_text())
    catalogue = {"source": {"mesh_sha256": sha256(source.mesh), "config_sha256": sha256(folder / "config.json")},
                 "settings": {"recognition": source.recognition, "transverse_angle_deg": 0, "longitudinal_angle_deg": 0},
                 "poses": data["poses"], "grouping_evidence": evidence_path.name,
                 "grouping_evidence_sha256": sha256(evidence_path)}
    catalogue_path = folder / "catalogue.json"
    catalogue_path.write_text(json.dumps(catalogue), encoding="utf-8")
    data["source_provenance"] = {"catalogue_sha256": sha256(catalogue_path)}
    source.path.write_text(json.dumps(data), encoding="utf-8")
    report = analyze_pose_quality(load_source(source.path))
    assert report["path_counts"]["reused"] == 1
    assert report["path_counts"]["calculated"] == 0
    evidence["paths"][0]["forward_barrier_mm"] = 999
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    recalculated = analyze_pose_quality(load_source(source.path))
    assert recalculated["path_counts"]["reused"] == 0
    assert recalculated["poses"]["Test_0000"]["escape_lift_mm"] == pytest.approx(a["escape_lift_mm"])


@pytest.mark.parametrize("filename", ["poses.json", "catalogue.json", "grouping-evidence.json"])
def test_cli_rejects_outputs_inside_source_catalogue_before_analysis(tmp_path, filename):
    source = source_for(tmp_path, quaternions=[[0, 0, 0, 1]])
    target = source.path.with_name(filename)
    if target != source.path:
        target.write_bytes(b"preserve me")
    previous = target.read_bytes()
    result = subprocess.run([sys.executable, "-m", "bibazu_stable_roadmaps.quality",
                             "--source", str(source.path), "--output", str(target)], capture_output=True, text=True)
    events = [json.loads(line) for line in result.stdout.splitlines()]
    assert result.returncode == 1
    assert events == [{"status": "failed", "message": "Save the quality report outside the input catalogue folder; source inputs are read-only."}]
    assert target.read_bytes() == previous


def test_cli_writes_a_report_and_cancel_preserves_existing_destination(tmp_path):
    source = source_for(tmp_path, quaternions=[[0, 0, 0, 1]])
    destination = tmp_path / "report.json"
    command = [sys.executable, "-m", "bibazu_stable_roadmaps.quality", "--source", str(source.path), "--output", str(destination)]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout.splitlines()[-1])["status"] == "completed"
    report = json.loads(destination.read_text())
    assert report["source_sha256"] == sha256(source.path)
    assert report["poses"]["Test_0000"]["label"] == "unknown"
    previous = destination.read_bytes()
    cancel = tmp_path / "cancel"
    cancel.touch()
    cancelled = subprocess.run(command + ["--cancel-file", str(cancel)], capture_output=True, text=True)
    assert cancelled.returncode == 0
    assert json.loads(cancelled.stdout)["status"] == "cancelled"
    assert destination.read_bytes() == previous
