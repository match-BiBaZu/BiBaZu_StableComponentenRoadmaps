import copy
import itertools
import json
from pathlib import Path

import numpy as np
import pytest
from scipy.spatial.transform import Rotation as R

from bibazu_stable_roadmaps.inputs import load_source
from bibazu_stable_roadmaps.roadmap import build_roadmap
from bibazu_stable_roadmaps.member_transfers import (
    augment_members,
    member_routes,
    SeatedEnergy,
    capture_samples,
    load_members,
)


def state(key, group):
    return dict(member_id=key, group_id=group, retained=True, quaternion_xyzw=[0, 0, 0, 1])


def transfer(key, source, targets, cost=1):
    return dict(
        edge_id=key,
        source_member_ids=source,
        possible_target_member_ids=targets,
        transfer_model="known_member_endpoint",
        actuation_count=cost,
        total_absolute_angle_deg=cost * 10,
    )


def test_member_continuity_and_explicit_repositioning():
    states = [state("A", 0), state("B1", 1), state("B2", 1), state("C", 2)]
    edges = [transfer("ab", ["A"], ["B1"]), transfer("bc", ["B2"], ["C"])]
    assert not any(
        r["source_member_id"] == "A" and r["target"] == 2 for r in member_routes(states, edges)
    )
    edges.append(transfer("reposition", ["B1"], ["B2"]))
    route = next(
        r for r in member_routes(states, edges) if r["source_member_id"] == "A" and r["target"] == 2
    )
    assert route["component_edge_ids"] == ["ab", "reposition", "bc"]


def test_branching_arrivals_require_universal_next_action():
    states = [state("A", 0), state("B1", 1), state("B2", 1), state("C", 2)]
    edges = [transfer("branch", ["A"], ["B1", "B2"]), transfer("partial", ["B1"], ["C"])]
    assert not any(
        r["source_member_id"] == "A" and r["target"] == 2 for r in member_routes(states, edges)
    )
    edges.append(transfer("universal", ["B1", "B2"], ["C"]))
    route = next(
        r for r in member_routes(states, edges) if r["source_member_id"] == "A" and r["target"] == 2
    )
    assert route["component_edge_ids"] == ["branch", "universal"]


def test_downhill_is_directed_and_rejects_barriers_and_plateaus():
    vertices = np.array(list(itertools.product((-2, 2), (-1, 1), (-0.5, 0.5))))
    energy = SeatedEnergy(vertices, 0, 0)
    sym = R.from_quat([[0, 0, 0, 1]])
    tilted = R.from_euler("y", 30, degrees=True)
    assert energy.downhill(tilted.as_matrix()[None], R.identity(), sym)[0][0]
    assert not energy.downhill(R.identity().as_matrix()[None], tilted, sym)[0][0]
    # A high stable face must first climb a barrier before falling onto the low face.
    assert not energy.downhill(
        R.from_euler("y", 90, degrees=True).as_matrix()[None], R.identity(), sym
    )[0][0]
    assert not energy.downhill(
        R.from_euler("y", 60.1, degrees=True).as_matrix()[None], R.identity(), sym
    )[0][0]
    assert not energy.downhill(
        R.from_euler("z", 20, degrees=True).as_matrix()[None], R.identity(), sym
    )[0][0]
    assert energy.downhill(R.identity().as_matrix()[None], R.identity(), sym)[0][0]


def test_capture_boundary_refinement_and_unknown_gaps():
    class Evidence:
        def downhill(self, endpoints, target, symmetries, continuous_axis):
            angles = R.from_matrix(endpoints).as_euler("xyz", degrees=True)[:, 1]
            return (angles >= 0.35) & (angles < 1.5), None, None

    states = [dict(member_id="target", quaternion_xyzw=[0, 0, 0, 1])]
    runs = capture_samples(
        [0, 0, 0, 1], "y", (-2, 2), states, Evidence(), R.from_quat([[0, 0, 0, 1]])
    )
    found = next(r for r in runs if r["outcomes"] == ("target",))
    assert min(found["angles"]) == pytest.approx(0.4)
    assert max(found["angles"]) == pytest.approx(1.4)
    assert any(not r["outcomes"] for r in runs)
    assert all(0 not in r["angles"] for r in runs)


@pytest.mark.parametrize("part,known,member_count", [("Qk1a", 20, 13), ("Dl1a", 34, 14)])
def test_known_member_actions_and_fallback_preserve_existing_data(part, known, member_count):
    folder = Path(__file__).resolve().parents[1] / part
    if not folder.is_dir():
        pytest.skip("Published workspace fixture unavailable")
    doc = json.loads((folder / f"{part}_roadmap.json").read_text())
    source = load_source(folder / "source/poses.json")
    by_id = {p.source_id: p for p in source.poses}
    built = build_roadmap(
        source, [(by_id[n["source_pose_ids"][0]], n["node_id"]) for n in doc["nodes"]]
    )
    built.document = copy.deepcopy(doc)
    augment_members(source, built, sample_capture=False)
    assert built.document["nodes"] == doc["nodes"] and built.document["edges"] == doc["edges"]
    assert sum(s["retained"] for s in built.document["member_states"]) == member_count
    assert (
        built.document["connectivity"]["members"]["known_member_inter_group_action_count"] == known
    )
    assert built.document["connectivity"]["members"]["every_source_member_reaches_every_group"]
    assert all(
        s["retained"]
        for s in built.document["member_states"]
        if s["member_id"]
        in {m for t in built.document["member_transfers"] for m in t["source_member_ids"]}
    )


def test_missing_declared_member_is_not_silently_dropped(source_folder):
    source = load_source(source_folder / "poses.json")
    doc = dict(
        nodes=[
            dict(node_id=0, source_pose_ids=[source.poses[0].source_id], group_members=["missing"])
        ]
    )
    with pytest.raises(ValueError, match="Missing"):
        load_members(source, doc)
