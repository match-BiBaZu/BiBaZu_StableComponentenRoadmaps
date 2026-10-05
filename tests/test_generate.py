from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import sys

import networkx as nx
import numpy as np
import pytest
import yaml

from bibazu_stable_roadmaps.generate import GenerationConfig, GenerationCancelled, generate_one
from bibazu_stable_roadmaps.inputs import load_source, select_poses, sha256
from bibazu_stable_roadmaps.roadmap import build_roadmap


@pytest.mark.parametrize("filename", ["poses.json", "pose_registry.json"])
def test_exports_preserve_observed_poses_without_enumeration(source_folder, tmp_path, monkeypatch, filename):
    def forbidden(*args, **kwargs):
        raise AssertionError("Theoretical pose enumeration must never run")
    for module in ("contacts", "symmetry", "visualization"):
        monkeypatch.setattr(f"bibazu_stable_roadmaps._engine.{module}.build_pose_catalog", forbidden)
    config = GenerationConfig(str(tmp_path / "outputs"), outputs=("yaml", "json", "graphml"))
    status, result = generate_one(source_folder / filename, config)
    assert status == "completed" and result["pose_count"] == 3
    folder = Path(result["folder"])
    document = json.loads((folder / "Test1_roadmap.json").read_text())
    source = load_source(source_folder / filename)
    for node, (pose, number) in zip(document["nodes"], select_poses(source, 5, True)[0]):
        assert node["node_id"] == number
        assert node["source_pose_ids"] == [pose.source_id]
        assert node["observed_frequency_percent"] == pose.frequency_percent
        assert np.allclose(node["representative_quaternion_xyzw"], pose.quaternion_xyzw)
        assert node["rocking_barrier_mm"] is None
    assert not document["analytical_stability_evaluated"]
    assert all(edge["source"] in range(3) and edge["target"] in range(3) for edge in document["edges"])
    assert all(edge["geometric_score"] is None and edge["settling_pose_ids"] == [] for edge in document["edges"])
    sheet = yaml.safe_load((folder / "Test1_roadmap.yaml").read_text())
    assert [pose["id"] for pose in sheet["poses"]] == [0, 1, 2]
    assert [edge["from_pose"] for edge in sheet["transitions"]] == [edge["source"] for edge in document["edges"]]
    assert sheet["classification"]["basis"] == "observed_simulation"
    graph = nx.read_graphml(folder / "Test1_roadmap.graphml")
    assert set(graph.nodes) == {"0", "1", "2"}
    assert all("rocking_barrier_mm" not in attributes for _, attributes in graph.nodes(data=True))
    for edge in document["edges"]:
        assert f":{edge['source']}->{edge['target']}:" in edge["edge_id"]
    assert (folder / document["source"]).is_file()
    assert {p.name for p in (folder / "source").iterdir()} == {"poses.json", "pose_registry.json", "Test1.stl", "config.json"}
    inventory = json.loads((folder / "files.sha256.json").read_text())
    assert all(sha256(folder / path) == digest for path, digest in inventory.items())


def test_source_numbering_and_no_connections_is_valid(source_folder, tmp_path):
    config = GenerationConfig(str(tmp_path / "outputs"), renumber_by_frequency=False, minimum_frequency_percent=25, outputs=("yaml",))
    status, result = generate_one(source_folder / "poses.json", config)
    sheet = yaml.safe_load((Path(result["folder"]) / "Test1_roadmap.yaml").read_text())
    assert sheet["poses"][0]["id"] == 7
    assert sheet["transitions"] == []
    assert sheet["classification"]["pose_ranking_method"] == "source_id"


def test_one_current_set_replacement_removes_stale_formats(source_folder, tmp_path):
    config = GenerationConfig(str(tmp_path / "outputs"), outputs=("yaml", "graphml"))
    _, result = generate_one(source_folder / "poses.json", config)
    folder = Path(result["folder"])
    generate_one(source_folder / "poses.json", replace(config, minimum_frequency_percent=25, outputs=("yaml",)))
    assert not (folder / "Test1_roadmap.graphml").exists()
    assert len(yaml.safe_load((folder / "Test1_roadmap.yaml").read_text())["poses"]) == 1
    index = json.loads((tmp_path / "outputs/index.json").read_text())
    assert index["workpieces"][0]["pose_count"] == 1
    assert index["workpieces"][0]["minimum_frequency_percent"] == 25
    assert not list((tmp_path / "outputs").glob(".roadmap-*"))


def test_failure_before_publication_keeps_previous_result(source_folder, tmp_path, monkeypatch):
    config = GenerationConfig(str(tmp_path / "outputs"), outputs=("yaml",))
    _, result = generate_one(source_folder / "poses.json", config)
    folder = Path(result["folder"])
    before = {p.relative_to(folder): p.read_bytes() for p in folder.rglob("*") if p.is_file()}
    def fail(*args, **kwargs):
        raise RuntimeError("render failed")
    monkeypatch.setattr("bibazu_stable_roadmaps.generate.build_roadmap", fail)
    with pytest.raises(RuntimeError, match="render failed"):
        generate_one(source_folder / "poses.json", config)
    assert before == {p.relative_to(folder): p.read_bytes() for p in folder.rglob("*") if p.is_file()}


def test_index_failure_rolls_back_component_and_indexes(source_folder, tmp_path, monkeypatch):
    config = GenerationConfig(str(tmp_path / "outputs"), outputs=("yaml",))
    _, result = generate_one(source_folder / "poses.json", config)
    root = tmp_path / "outputs"
    before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    def fail(*args, **kwargs):
        raise RuntimeError("index failed")
    monkeypatch.setattr("bibazu_stable_roadmaps.generate.update_index", fail)
    with pytest.raises(RuntimeError, match="index failed"):
        generate_one(source_folder / "poses.json", replace(config, minimum_frequency_percent=25))
    assert before == {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def test_manual_files_are_preserved(source_folder, tmp_path):
    config = GenerationConfig(str(tmp_path / "outputs"), outputs=("yaml",))
    _, result = generate_one(source_folder / "poses.json", config)
    manual = Path(result["folder"]) / "manual.txt"
    manual.write_text("my work")
    with pytest.raises(ValueError, match="manually changed"):
        generate_one(source_folder / "poses.json", config)
    assert manual.read_text() == "my work"


def test_empty_or_all_removed_preserves_existing_and_does_not_calculate(source_folder, tmp_path, monkeypatch):
    config = GenerationConfig(str(tmp_path / "outputs"), outputs=("yaml",))
    def forbidden(*args, **kwargs):
        raise AssertionError("No geometry needed for empty selection")
    monkeypatch.setattr("bibazu_stable_roadmaps.generate.build_roadmap", forbidden)
    assert generate_one(source_folder / "poses.json", replace(config, minimum_frequency_percent=100))[0] == "skipped"
    path = source_folder / "poses.json"
    data = json.loads(path.read_text())
    data["poses"] = []
    path.write_text(json.dumps(data))
    assert generate_one(path, config)[0] == "skipped"
    assert not (tmp_path / "outputs").exists()


def test_uncertain_contact_does_not_remove_pose(source_folder):
    path = source_folder / "poses.json"
    data = json.loads(path.read_text())
    from scipy.spatial.transform import Rotation
    data["poses"][0]["quaternion_xyzw"] = Rotation.from_euler("xyz", [12, 23, 34], degrees=True).as_quat().tolist()
    path.write_text(json.dumps(data))
    source = load_source(path)
    built = build_roadmap(source, select_poses(source, 25, True)[0])
    assert len(built.document["nodes"]) == 1
    assert built.warnings


def test_cancelled_staging_keeps_previous_result(source_folder, tmp_path):
    config = GenerationConfig(str(tmp_path / "outputs"), outputs=("yaml",))
    _, result = generate_one(source_folder / "poses.json", config)
    old = (Path(result["folder"]) / "Test1_roadmap.yaml").read_bytes()
    counter = 0
    def cancel():
        nonlocal counter
        counter += 1
        if counter > 2:
            raise GenerationCancelled()
    with pytest.raises(GenerationCancelled):
        generate_one(source_folder / "poses.json", config, check_cancel=cancel)
    assert (Path(result["folder"]) / "Test1_roadmap.yaml").read_bytes() == old
    assert not (tmp_path / "outputs/.roadmaps.lock").exists()


def test_refuse_output_in_source_catalogue(source_folder):
    config = GenerationConfig(str(source_folder.parent), outputs=("yaml",))
    with pytest.raises(ValueError, match="separate from the source"):
        generate_one(source_folder / "poses.json", config)


def test_existing_reorientation_consumer_loads_both_formats(source_folder, tmp_path):
    consumer_path = Path(__file__).resolve().parents[2] / "BiBaZu_Big_Boi/ReorientationControlGUI/src/bibazu_reorientation/roadmap.py"
    if not consumer_path.is_file():
        pytest.skip("Optional workspace integration: existing reorientation consumer is not installed")
    spec = importlib.util.spec_from_file_location("_existing_roadmap_consumer", consumer_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    _, result = generate_one(source_folder / "poses.json", GenerationConfig(str(tmp_path / "outputs"), outputs=("yaml", "json")))
    for extension in ("yaml", "json"):
        loaded = module.load_pose_roadmap(Path(result["folder"]) / f"Test1_roadmap.{extension}")
        assert [pose.pose_id for pose in loaded.poses] == [0, 1, 2]
        assert loaded.mesh_path.is_file()
        assert all(pose.rocking_barrier_mm is None for pose in loaded.poses)


@pytest.mark.parametrize("cutoff", [-1, 101, float("nan")])
def test_config_rejects_bad_cutoffs(cutoff):
    with pytest.raises(ValueError):
        GenerationConfig(minimum_frequency_percent=cutoff).validate()
