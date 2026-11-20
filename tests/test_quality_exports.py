"""Quality annotations must describe source geometry without changing the roadmap."""
from dataclasses import replace
import json
import math
from pathlib import Path

import networkx as nx
import numpy as np
import pytest
from scipy.spatial.transform import Rotation
import trimesh
import yaml

from bibazu_stable_roadmaps.generate import GenerationConfig, generate_one
from bibazu_stable_roadmaps.inputs import sha256


def thin_box_catalogue(folder, *, one_pose=False):
    """A common precarious pose can escape into a rare broad resting pose."""
    mesh = folder / "Test1.stl"
    trimesh.creation.box(extents=(40, 30, 2)).export(mesh)
    path = folder / "poses.json"
    data = json.loads(path.read_text())
    data["geometry"]["stl_sha256"] = sha256(mesh)
    data["poses"] = [
        {"id": "Test1_0007", "count": 96, "frequency_percent": 96., "group_id": "G0",
         "quaternion_xyzw": Rotation.from_euler("y", 90, degrees=True).as_quat().tolist()},
    ]
    if not one_pose:
        data["poses"].append({"id": "Test1_0009", "count": 4, "frequency_percent": 4.,
                              "group_id": "G0", "quaternion_xyzw": [0., 0., 0., 1.]})
    data["groups"] = [{"id": "G0", "members": [pose["id"] for pose in data["poses"]]}]
    path.write_text(json.dumps(data), encoding="utf-8")
    (folder / "pose_registry.json").write_text(json.dumps({
        "schema_version": 1, "mesh_sha256": sha256(mesh),
        "entries": [{"id": pose["id"], "anchor_quaternion_xyzw": pose["quaternion_xyzw"]}
                    for pose in data["poses"]],
    }), encoding="utf-8")
    (folder / "config.json").write_text(json.dumps({"alpha_deg": 0., "beta_deg": 0.}), encoding="utf-8")
    # Fixture models a published DropSim report; consumers must not recompute it.
    entries={}
    for row in data["poses"]:
        upright=row["id"]=="Test1_0007"
        lift=None if one_pose else math.hypot(20,1)-(20 if upright else 1)
        entries[row["id"]]={"label":"unknown" if one_pose else "fragile" if upright else "resistant",
            "stability":"unknown" if one_pose else "low" if upright else "high",
            "escape_lift_mm":lift,"escape_target_source_id":None if one_pose else "Test1_0009" if upright else "Test1_0007",
            "escape_within_group":None if one_pose else True}
    report={"schema_version":1,"producer":"dashas_drop_sim","method":"sampled_seated_escape_lift","method_version":1,
        "source_sha256":sha256(path),"observations_sha256":sha256(path),"mesh_sha256":sha256(mesh),
        "config_sha256":sha256(folder/"config.json"),"thresholds_mm":{"fragile":.1,"resistant":.5},"poses":entries}
    (folder/"pose_quality.json").write_text(json.dumps(report),encoding="utf-8")
    return path, data


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_quality_exports_include_filtered_destination_without_changing_observations(source_folder, tmp_path):
    source_path, source_data = thin_box_catalogue(source_folder)
    original_files = {path.name: path.read_bytes() for path in source_folder.iterdir() if path.is_file()}
    config = GenerationConfig(str(tmp_path / "outputs"), minimum_frequency_percent=5,
                              outputs=("json", "yaml", "graphml"))
    status, result = generate_one(source_path, config)
    assert status == "completed" and result["pose_count"] == 1
    folder = Path(result["folder"])
    report = load_json(folder / "pose_quality.json")
    assert report["source_sha256"] == sha256(source_path)
    assert report["mesh_sha256"] == sha256(source_folder / "Test1.stl")
    assert report["thresholds_mm"] == {"fragile": .1, "resistant": .5}
    assert set(report["poses"]) == {"Test1_0007", "Test1_0009"}
    quality = report["poses"]["Test1_0007"]
    assert quality["label"] == "fragile"
    assert quality["escape_lift_mm"] == pytest.approx(math.hypot(20, 1) - 20, abs=1e-4)
    assert quality["escape_target_source_id"] == "Test1_0009"
    assert quality["escape_within_group"] is True
    assert report["poses"]["Test1_0009"]["label"] == "resistant"

    document = load_json(folder / "Test1_roadmap.json")
    sheet = yaml.safe_load((folder / "Test1_roadmap.yaml").read_text(encoding="utf-8"))
    assert len(document["nodes"]) == len(sheet["poses"]) == 1
    node, pose = document["nodes"][0], sheet["poses"][0]
    assert node["node_id"] == pose["id"] == 0
    assert node["source_pose_ids"] == pose["source_pose_ids"] == ["Test1_0007"]
    assert node["observed_count"] == pose["observed_count"] == 96
    assert node["observed_frequency_percent"] == pose["observed_frequency_percent"] == 96
    assert np.allclose(node["representative_quaternion_xyzw"], source_data["poses"][0]["quaternion_xyzw"])
    assert node["pose_quality"] == pose["pose_quality"] == quality
    # The easiest destination is below the frequency cutoff: it remains a source ID,
    # rather than acquiring a nonexistent numeric roadmap node or actuated edge.
    assert document["edges"] == sheet["transitions"] == []
    assert node["kind"] == pose["stability"] == "robust"
    assert node["rocking_barrier_mm"] is None
    for exported in (document, sheet):
        metadata = exported["pose_quality_assessment"]
        assert metadata["method"] == report["method"]
        assert metadata["thresholds_mm"] == report["thresholds_mm"]
        assert "poses" not in metadata

    graph = nx.read_graphml(folder / "Test1_roadmap.graphml")
    attributes = graph.nodes["0"]
    assert attributes["pose_quality_label"] == quality["label"]
    assert attributes["pose_quality_escape_lift_mm"] == quality["escape_lift_mm"]
    assert attributes["pose_quality_escape_target_source_id"] == "Test1_0009"
    assert attributes["pose_quality_escape_within_group"] is True
    assert graph.number_of_edges() == 0
    manifest = load_json(folder / "manifest.json")
    assert manifest["geometric_pose_quality_evaluated"] is True
    assert manifest["analytical_stability_evaluated"] is False
    assert document["analytical_stability_evaluated"] is False
    assert original_files == {path.name: path.read_bytes() for path in source_folder.iterdir() if path.is_file()}
    assert original_files == {path.name: path.read_bytes() for path in (folder / "source").iterdir() if path.is_file()}
    inventory = load_json(folder / "files.sha256.json")
    assert inventory["pose_quality.json"] == sha256(folder / "pose_quality.json")
    assert all(sha256(folder / name) == digest for name, digest in inventory.items())


def test_quality_is_independent_of_frequency_filter_and_roadmap_numbering(source_folder, tmp_path):
    source_path, _ = thin_box_catalogue(source_folder)
    config = GenerationConfig(str(tmp_path / "outputs"), minimum_frequency_percent=5,
                              outputs=("yaml",))
    _, result = generate_one(source_path, config)
    folder = Path(result["folder"])
    filtered = load_json(folder / "pose_quality.json")
    assert len(yaml.safe_load((folder / "Test1_roadmap.yaml").read_text())["poses"]) == 1
    generate_one(source_path, replace(config, minimum_frequency_percent=0, renumber_by_frequency=False))
    unfiltered = load_json(folder / "pose_quality.json")
    assert filtered["poses"] == unfiltered["poses"]
    sheet = yaml.safe_load((folder / "Test1_roadmap.yaml").read_text())
    assert [pose["id"] for pose in sheet["poses"]] == [7, 9]
    assert [pose["pose_quality"]["label"] for pose in sheet["poses"]] == ["fragile", "resistant"]
    assert [pose["observed_count"] for pose in sheet["poses"]] == [96, 4]


def test_single_pose_stays_unknown_and_graphml_does_not_invent_values(source_folder, tmp_path):
    source_path, _ = thin_box_catalogue(source_folder, one_pose=True)
    _, result = generate_one(source_path, GenerationConfig(str(tmp_path / "outputs"),
                                                         outputs=("json", "yaml", "graphml")))
    folder = Path(result["folder"])
    report = load_json(folder / "pose_quality.json")
    quality = report["poses"]["Test1_0007"]
    assert quality["label"] == "unknown"
    assert quality["escape_lift_mm"] is None
    assert quality["escape_target_source_id"] is None
    assert quality["escape_within_group"] is None
    graph = nx.read_graphml(folder / "Test1_roadmap.graphml")
    assert graph.nodes["0"]["pose_quality_label"] == "unknown"
    assert all(name not in graph.nodes["0"] for name in (
        "pose_quality_escape_lift_mm", "pose_quality_escape_target_source_id", "pose_quality_escape_within_group"))
    document = load_json(folder / "Test1_roadmap.json")
    assert document["nodes"][0]["pose_quality"] == quality
    assert document["nodes"][0]["rocking_barrier_mm"] is None
