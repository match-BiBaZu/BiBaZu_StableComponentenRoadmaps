import json

import pytest

from bibazu_stable_roadmaps.inputs import EmptyPoseList, discover_sources, load_source, select_poses


@pytest.mark.parametrize("filename", ["poses.json", "pose_registry.json"])
def test_threshold_numbering_and_orientation_identity(source_folder, filename):
    source = load_source(source_folder / filename)
    retained, removed = select_poses(source, 5, True)
    assert [(pose.source_id, number) for pose, number in retained] == [("Test1_0007", 0), ("Test1_0009", 1), ("Test1_0003", 2)]
    assert [pose.frequency_percent for pose, _ in retained] == [27, 20, 5]
    assert removed[0].source_id == "Test1_0010"
    assert len(select_poses(source, 0, True)[0]) == 4
    assert [number for _, number in select_poses(source, 5, False)[0]] == [7, 9, 3]


def test_discover_components_once_prefers_observations(source_folder):
    assert discover_sources(source_folder.parent) == [source_folder / "poses.json"]
    assert discover_sources(source_folder / "pose_registry.json") == [source_folder / "pose_registry.json"]


def test_registry_anchor_is_not_replaced_by_observation(source_folder):
    path = source_folder / "pose_registry.json"
    data = json.loads(path.read_text())
    data["entries"][0]["anchor_quaternion_xyzw"] = [0, 0, 1, 0]
    data["entries"].append({"id": "Test1_0011", "anchor_quaternion_xyzw": [0, 0, 0, 1]})
    path.write_text(json.dumps(data))
    source = load_source(path)
    assert source.poses[0].quaternion_xyzw == (0, 0, 1, 0)
    assert source.poses[-1].frequency_percent == 0


def test_counts_use_all_trials_without_rescaling(source_folder):
    path = source_folder / "poses.json"
    data = json.loads(path.read_text())
    for row in data["poses"]:
        del row["frequency_percent"]
    path.write_text(json.dumps(data))
    retained, removed = select_poses(load_source(path), 5, True)
    assert [pose.frequency_percent for pose, _ in retained] == [27, 20, 5]
    assert sum(pose.frequency_percent for pose, _ in retained) == 52


@pytest.mark.parametrize("field,value", [("frequency_percent", -1), ("frequency_percent", float("nan")),
                                         ("count", -1), ("count", True), ("quaternion_xyzw", [0, 0, 0, 0]),
                                         ("quaternion_xyzw", [0, 1, 0])])
def test_invalid_pose_data_rejected(source_folder, field, value):
    path = source_folder / "poses.json"
    data = json.loads(path.read_text())
    data["poses"][0][field] = value
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        load_source(path)


def test_missing_mismatched_mesh_and_registry_frequencies(source_folder):
    mesh = source_folder / "Test1.stl"
    original = mesh.read_bytes()
    mesh.write_bytes(b"different")
    with pytest.raises(ValueError, match="hash"):
        load_source(source_folder / "poses.json")
    mesh.write_bytes(original)
    mesh.unlink()
    with pytest.raises(ValueError, match="Missing matching"):
        load_source(source_folder / "poses.json")
    (source_folder / "poses.json").unlink()
    with pytest.raises(ValueError, match="neighboring poses.json"):
        load_source(source_folder / "pose_registry.json")


def test_empty_duplicate_and_wrong_convention(source_folder):
    path = source_folder / "poses.json"
    data = json.loads(path.read_text())
    original = json.loads(path.read_text())
    data["poses"].append(data["poses"][0])
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="duplicate"):
        load_source(path)
    data = original
    data["recognition"]["rotation"] = "chute_to_part"
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="part-to-chute"):
        load_source(path)
    data["poses"] = []
    path.write_text(json.dumps(data))
    with pytest.raises(EmptyPoseList):
        load_source(path)


def test_frequency_ties_are_deterministic(source_folder):
    path = source_folder / "poses.json"
    data = json.loads(path.read_text())
    for row in data["poses"]:
        row["frequency_percent"] = 10
    path.write_text(json.dumps(data))
    retained, _ = select_poses(load_source(path), 5, True)
    assert [pose.source_id for pose, _ in retained] == sorted(row["id"] for row in data["poses"])
