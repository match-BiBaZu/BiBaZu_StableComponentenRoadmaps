from copy import deepcopy
import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from bibazu_stable_roadmaps.derive import build_catalogue, cluster_orientations


def descriptor(symmetry=None, axis=None):
    return {"symmetry_quaternions_xyzw": symmetry or [[0, 0, 0, 1]], "continuous_axis_part": axis,
            "quaternion_order": "xyzw", "rotation": "part_to_chute"}


def test_complete_link_prevents_chained_modes_and_is_permutation_invariant():
    quats = Rotation.from_euler("x", [[0], [4], [8], [90]], degrees=True).as_quat()
    labels = cluster_orientations(quats, descriptor())
    assert labels[0] != labels[2]
    assert len(set(labels)) == 3
    order = [2, 0, 3, 1]
    permuted = cluster_orientations(quats[order], descriptor())
    assert [permuted[order.index(index)] for index in range(4)] == labels


def test_quaternion_sign_and_discrete_part_symmetry():
    identity = [0, 0, 0, 1]
    half_turn = Rotation.from_euler("z", 180, degrees=True).as_quat().tolist()
    assert cluster_orientations([identity, [0, 0, 0, -1], half_turn], descriptor([identity, half_turn])) == [0, 0, 0]


def test_continuous_axis_is_directed():
    quats = Rotation.from_euler("x", [[0], [90], [180]], degrees=True).as_quat()
    assert len(set(cluster_orientations(quats, descriptor(axis=[0, 0, 1])))) == 3


def test_counts_keep_unsettled_denominator_and_observed_representatives():
    rows = [{"trial": i, "status": "settled" if i < 2 else "unsettled",
             "final_quat_xyzw": Rotation.from_euler("x", i, degrees=True).as_quat().tolist()} for i in range(5)]
    data = build_catalogue(rows, "Test1", "study", "transport", {}, descriptor(), {})
    assert data["completed_trials"] == 5 and data["settled_trials"] == 2
    assert len(data["poses"]) == 1
    pose = data["poses"][0]
    assert pose["count"] == 2 and pose["frequency_percent"] == 40
    assert pose["member_trial_ids"] == [0, 1]
    assert pose["quaternion_xyzw"] == rows[0]["final_quat_xyzw"]


def test_post_braking_is_not_mixed_with_transport():
    rows = [{"trial": i, "status": "unsettled", "final_quat_xyzw": [0, 0, 0, 1],
             "stop_observation": {"status": "settled", "final_quat_xyzw": [0, 0, 1, 0]}} for i in range(3)]
    original = deepcopy(rows)
    moving = build_catalogue(rows, "Test1", "study", "transport", {}, descriptor(), {})
    stopped = build_catalogue(rows, "Test1", "study", "after_belt_stop", {}, descriptor(), {})
    assert moving["settled_trials"] == 0 and moving["poses"] == []
    assert stopped["settled_trials"] == 3 and stopped["poses"][0]["frequency_percent"] == 100
    assert rows == original


def test_classes_match_simulator_reference():
    path = Path(__file__).resolve().parents[2] / "Dashas_drop_sim/src/dashas_drop_sim/pose_matching.py"
    if not path.exists():
        pytest.skip("Optional simulator comparison requires its workspace source")
    spec = importlib.util.spec_from_file_location("_classification_reference", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    reference = module.PoseResolver.__new__(module.PoseResolver)
    reference._continuous_axis = None
    reference._symmetry_quats = np.array([[0, 0, 0, 1], [0, 0, 1, 0]])
    reference.cluster_tolerance_deg = 5.0
    quats = Rotation.from_euler("xyz", [[0, 0, 0], [3, 0, 0], [8, 0, 0], [0, 0, 180], [0, 90, 0]], degrees=True).as_quat()
    assert cluster_orientations(quats, descriptor(reference._symmetry_quats.tolist())) == reference.cluster_unmatched(quats)
