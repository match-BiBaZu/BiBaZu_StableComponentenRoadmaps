"""Finish calibration choices and execution routes before handing files to controls.

Controls never need this package: every route, identity, applicability requirement,
and preview segment is materialized in the exported document.
"""
from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
import hashlib

from .transfer_validation import (
    member_route_record, preferred_path, rotate, validate_members, validate_transfer,
)


def _commands(edge, poses):
    if edge.get("commands"):
        return deepcopy(edge["commands"])
    if edge.get("signed_angle_deg") is None:
        return []
    action = edge.get("actuation", "")
    axis = "x" if "main_" in action else action[-1:]
    if axis not in "xyz" or not axis:
        return []
    start = poses[edge["source"]]
    return [dict(axis=axis, actuation=action, signed_angle_deg=edge["signed_angle_deg"],
                 start_quaternion_xyzw=list(start),
                 end_quaternion_xyzw=list(rotate(start, axis, edge["signed_angle_deg"])))]


def _legacy_paths(edges):
    """Preserve the original GUI's two/three-transfer IDs, including parallel options."""
    adjacency = defaultdict(list)
    for edge in edges:
        adjacency[edge["source"]].append(edge)
    for values in adjacency.values():
        values.sort(key=lambda e: (e["target"], e["edge_id"]))
    candidates = []

    def walk(poses, legs):
        if len(legs) in (2, 3):
            candidates.append((poses, legs))
        if len(legs) == 3:
            return
        for edge in adjacency[poses[-1]]:
            if edge["target"] not in poses:
                walk(poses + (edge["target"],), legs + (edge,))

    for start in sorted(tuple(adjacency)):
        walk((start,), ())
    counts = defaultdict(int)
    for poses, legs in sorted(candidates, key=lambda x: (len(x[1]), x[0], tuple(e["edge_id"] for e in x[1]))):
        base = f"multi{len(legs)}:" + "->".join(map(str, poses))
        counts[base] += 1
        yield base if counts[base] == 1 else f"{base}:option{counts[base]}", legs


def _macro(identity, legs):
    count = sum(e["actuation_count"] for e in legs)
    evidence = "geometry_only" if any(e.get("evidence_status") == "geometry_only" for e in legs) else ""
    return dict(edge_id=identity, source=legs[0]["source"], target=legs[-1]["target"],
                directed=True, transition_kind="multi_reorientation",
                actuation=f"multiple_reorientation_{count}", actuation_count=count,
                signed_angle_deg=None, geometric_score=None,
                experimental_status="untested" if evidence else "experimental_non_preferred",
                component_edge_ids=[e["edge_id"] for e in legs],
                via_pose_ids=[e["target"] for e in legs[:-1]],
                commands=[c for e in legs for c in e["commands"]],
                total_absolute_angle_deg=sum(e["total_absolute_angle_deg"] for e in legs),
                evidence_status=evidence, legs=list(legs))


def _preview(record):
    return [dict(segment, segment_kind=kind)
            for leg in record.get("legs", [record])
            for kind, segments in (("command", leg.get("commands", [])),
                                   ("settling", leg.get("settling_segments", [])))
            for segment in segments]


def build_consumer_export(document):
    """Return an additive, deterministic, standalone consumer contract (version 1)."""
    poses = {n["node_id"]: n["representative_quaternion_xyzw"] for n in document["nodes"]}
    robust = {n["node_id"] for n in document["nodes"] if n.get("kind") == "robust"}
    states, transfers = validate_members(document)
    groups = defaultdict(list)
    for state in states:
        if state["retained"]:
            groups[state["group_id"]].append(state["member_id"])
    representatives = {n["node_id"]: n.get("source_pose_ids", [None])[0] for n in document["nodes"]}
    choices = {}

    def add(raw):
        record = deepcopy(raw)
        record.setdefault("directed", True)
        record.setdefault("transition_kind", "actuated")
        record.setdefault("commands", _commands(record, poses))
        record.setdefault("actuation_count", len(record["commands"]) or 1)
        record.setdefault("signed_angle_deg", None)
        record.setdefault("component_edge_ids", [])
        record.setdefault("via_pose_ids", [])
        record.setdefault("evidence_status", "")
        record.setdefault("total_absolute_angle_deg", sum(abs(c["signed_angle_deg"]) for c in record["commands"]))
        if groups:
            record.setdefault("source_member_ids", [representatives[record["source"]]])
            record.setdefault("possible_target_member_ids", [representatives[record["target"]]])
            record["source_group_member_ids"] = sorted(groups[record["source"]])
            record["target_group_member_ids"] = sorted(groups[record["target"]])
        record["preview_segments"] = _preview(record)
        # Component IDs and flattened preview segments are sufficient for consumers.
        # Embedding complete legs here duplicates the graph for every macro.
        record.pop("legs", None)
        old = choices.get(record["edge_id"])
        if old is not None and old != record:
            raise ValueError(f"Conflicting calibration identity: {record['edge_id']}")
        choices[record["edge_id"]] = record
        return record

    direct = [add(e) for e in document["edges"] if e.get("transition_kind") == "actuated"
              and e["source"] in robust and e["target"] in robust]
    composites = []
    for raw in document.get("composite_transfers", []):
        validate_transfer(raw, poses)
        composites.append(add(dict(raw, transition_kind="multi_reorientation",
                                   actuation=f"multiple_reorientation_{raw['actuation_count']}")))
    for raw in transfers:
        add(dict(raw, transition_kind="member_transfer"))
    for identity, legs in _legacy_paths(direct):
        add(_macro(identity, legs))
    for start in sorted(robust):
        for target in sorted(robust - {start}):
            legs = preferred_path(direct + composites, start, target)
            if len(legs) > 1:
                ids = [e["edge_id"] for e in legs]
                digest = hashlib.sha256("|".join(ids).encode()).hexdigest()[:16]
                evidence = any(e.get("evidence_status") == "geometry_only" for e in legs)
                identity = (f"route:{start}->{target}:{digest}" if evidence else
                            f"multi{len(legs)}:" + "->".join(map(str, (start,) + tuple(e["target"] for e in legs))))
                if identity not in choices:
                    add(_macro(identity, legs))
    for route in document.get("member_routes", []):
        record = member_route_record(route, transfers)
        if record and record.get("legs"):
            add(dict(record, transition_kind="multi_reorientation"))

    execution = []
    for record in sorted(choices.values(), key=lambda e: e["edge_id"]):
        alternatives = [[record]]
        if record["component_edge_ids"]:
            alternatives.append([choices[key] for key in record["component_edge_ids"]])
        for legs in alternatives:
            possible = set(groups[record["source"]])
            steps = []
            for leg in legs:
                required = sorted(possible)
                supported = set(leg.get("source_member_ids", []))
                # Calibration may explicitly cover additional starts. Its arrival
                # member is then unknown: conservatively retain the whole group.
                possible = (set(leg.get("possible_target_member_ids", []))
                            if possible and possible.issubset(supported)
                            else set(groups[leg["target"]]))
                steps.append(dict(edge_id=leg["edge_id"], source=leg["source"], target=leg["target"],
                                  required_source_member_ids=required,
                                  possible_target_member_ids=sorted(possible)))
            execution.append(dict(route_id=record["edge_id"] + (":profiles" if len(legs) > 1 else ":profile"),
                                  source=record["source"], target=record["target"],
                                  profile_edge_ids=[e["edge_id"] for e in legs], steps=steps,
                                  priority=[0 if len(legs) == 1 and record["transition_kind"] == "actuated"
                                            else 1 if len(legs) == 1 else 2, len(legs)],
                                  evidence_status=record["evidence_status"]))
    return dict(version=1, calibration_choices=sorted(choices.values(), key=lambda e: e["edge_id"]),
                execution_routes=execution,
                route_policy="exported_only; explicit calibration and source coverage required")


def attach_consumer_export(document):
    document["consumer_export"] = build_consumer_export(document)
    return document
