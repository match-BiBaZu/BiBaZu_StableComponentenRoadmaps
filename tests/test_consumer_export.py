from copy import deepcopy
import json

import pytest

from bibazu_stable_roadmaps.consumer_export import attach_consumer_export, build_consumer_export
from bibazu_stable_roadmaps.transfer_validation import rotate, validate_members, validate_transfer
from bibazu_stable_roadmaps.roadmap import handover_dict


def chain(length=6):
    return dict(schema_version=1, source="part.stl", geometry_status="verified", generation={},
        nodes=[dict(node_id=i, pose_ids=[i], kind="robust", source_pose_ids=[f"m{i}"],
                    representative_quaternion_xyzw=list(rotate([0, 0, 0, 1], "y", i * 10)))
               for i in range(length + 1)],
        edges=[dict(edge_id=f"a{i}", source=i, target=i+1, directed=True,
                    transition_kind="actuated", actuation="free_y", signed_angle_deg=10)
               for i in range(length)])


def test_long_route_is_finished_upstream_and_direct_data_is_unchanged():
    document = chain()
    original = deepcopy(document)
    attach_consumer_export(document)
    assert {k: v for k, v in document.items() if k != "consumer_export"} == original
    choices = {c["edge_id"]: c for c in document["consumer_export"]["calibration_choices"]}
    macro = choices["multi6:0->1->2->3->4->5->6"]
    assert macro["component_edge_ids"] == [f"a{i}" for i in range(6)]
    assert len(macro["commands"]) == len(macro["preview_segments"]) == 6
    assert any(r["source"] == 0 and r["target"] == 6 and len(r["steps"]) == 6
               for r in document["consumer_export"]["execution_routes"])
    assert not any(c["source"] == 6 and c["target"] == 0 for c in choices.values())
    assert build_consumer_export(document) == document["consumer_export"]


def test_legacy_parallel_option_ids_are_preserved():
    document = chain(2)
    document["edges"].append(dict(document["edges"][0], edge_id="parallel"))
    section = build_consumer_export(document)
    options = {c["edge_id"]: c for c in section["calibration_choices"]}
    assert options["multi2:0->1->2"]["component_edge_ids"] == ["a0", "a1"]
    assert options["multi2:0->1->2:option2"]["component_edge_ids"] == ["parallel", "a1"]


def test_unknown_arrivals_require_full_next_group_coverage():
    document = chain(2)
    document["member_states"] = [
        dict(member_id=key, group_id=g, retained=True, quaternion_xyzw=[0, 0, 0, 1])
        for g, key in [(0, "m0"), (0, "extra0"), (1, "m1"), (1, "extra1"), (2, "m2")]]
    section = build_consumer_export(document)
    route = next(r for r in section["execution_routes"] if r["profile_edge_ids"] == ["a0", "a1"])
    assert route["steps"][0]["required_source_member_ids"] == ["extra0", "m0"]
    assert route["steps"][1]["required_source_member_ids"] == ["extra1", "m1"]
    document["member_states"] = [s for s in document["member_states"] if s["member_id"] != "extra0"]
    section = build_consumer_export(document)
    route = next(r for r in section["execution_routes"] if r["profile_edge_ids"] == ["a0", "a1"])
    assert route["steps"][1]["required_source_member_ids"] == ["m1"]


def test_geometry_verification_is_owned_by_producer():
    start = [0, 0, 0, 1]
    terminal = list(rotate(start, "y", 90))
    transfer = dict(edge_id="composite:0->1:test", source=0, target=1, directed=True,
        transition_kind="composite_candidate", evidence_status="geometry_only", actuation_count=1,
        terminal_quaternion_xyzw=terminal, terminal_symmetry_quaternion_xyzw=start,
        commands=[dict(axis="y", signed_angle_deg=89, start_quaternion_xyzw=start,
                       end_quaternion_xyzw=terminal)])
    with pytest.raises(ValueError, match="endpoint mismatch"):
        validate_transfer(transfer, {0: start, 1: terminal})


def test_disconnected_and_json_roundtrip():
    document = chain(2)
    document["edges"] = document["edges"][:1]
    attach_consumer_export(document)
    assert not any(r["target"] == 2 for r in document["consumer_export"]["execution_routes"])
    assert json.loads(json.dumps(document))["consumer_export"] == document["consumer_export"]
