"""Whole-group candidate actions. Member witnesses do not constrain composition."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import heapq
import json

import numpy as np
from scipy.spatial.transform import Rotation as R

from .connectivity import composite_transfer, connectivity
from .member_transfers import SeatedEnergy, augment_members, command, load_members
from .roadmap import _symmetry

PLANNING_ASSUMPTION = (
    "group_union: arrival and departure may use different group members"
)
ENDPOINT_TOLERANCE_DEG = 1.0


def identity(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:20]


def cartesian(commands):
    return len(commands) == 1 and any(
        abs(abs(commands[0]["signed_angle_deg"]) - angle) < 1e-8 for angle in (90, 180)
    )


def command_name(commands):
    return (
        " → ".join(
            f"{c['axis'].upper()} {c['signed_angle_deg']:+.8g}°" for c in commands
        )
        or "No rotation"
    )


def preference(transfer):
    return (
        int(not transfer["cartesian_preferred"]),
        int(transfer["is_composite"]),
        transfer["actuation_count"],
        transfer["total_absolute_angle_deg"],
        int(bool(transfer.get("settling_required"))),
    )


def endpoint_errors(endpoints, target, symmetries, continuous_axis=None):
    variants = target * symmetries
    if continuous_axis is not None:
        directions = variants.apply(continuous_axis)
        cosines = endpoints.apply(continuous_axis) @ directions.T
        return np.degrees(np.arccos(np.clip(cosines.max(axis=1), -1, 1)))
    return np.array(
        [np.degrees((end.inv() * variants).magnitude()).min() for end in endpoints]
    )


def landing_paths(energy, endpoints, target, symmetries, continuous_axis=None):
    if continuous_axis is None:
        return energy.downhill(endpoints.as_matrix(), target, symmetries)
    # Finite symmetries may also reverse a continuously symmetric part's axis.
    variants, directions = [], []
    for variant in target * symmetries:
        direction = variant.apply(continuous_axis)
        if not any(np.linalg.norm(direction - old) < 1e-8 for old in directions):
            variants.append(variant)
            directions.append(direction)
    accepted = np.zeros(len(endpoints), dtype=bool)
    vectors = np.zeros((len(endpoints), 3))
    terminals = endpoints.as_matrix().copy()
    best = np.full(len(endpoints), np.inf)
    for variant in variants:
        allowed, rv, terminal = energy.downhill(
            endpoints.as_matrix(), variant, symmetries, continuous_axis
        )
        length = np.linalg.norm(rv, axis=1)
        replace = allowed & (length < best)
        accepted |= allowed
        vectors[replace], terminals[replace], best[replace] = (
            rv[replace],
            terminal[replace],
            length[replace],
        )
    return accepted, vectors, terminals


def preferred_group_routes(groups, transfers):
    adjacency = defaultdict(list)
    for transfer in transfers:
        adjacency[transfer["source"]].append(transfer)
    routes = []
    for source in sorted(groups):
        queue = [((0, 0, 0, 0.0, 0, ()), source)]
        visited = set()
        while queue:
            cost, target = heapq.heappop(queue)
            if target in visited:
                continue
            visited.add(target)
            if source != target:
                routes.append(
                    dict(
                        edge_id=f"group-route:{source}->{target}:{identity(cost[-1])}",
                        source=source,
                        target=target,
                        component_edge_ids=list(cost[-1]),
                        preference_cost=list(cost[:-1]),
                        planning_assumption=PLANNING_ASSUMPTION,
                        evidence_status="geometry_only",
                    )
                )
            for transfer in adjacency[target]:
                if transfer["target"] in visited:
                    continue
                step = preference(transfer)
                new = tuple(cost[i] + step[i] for i in range(5)) + (
                    cost[-1] + (transfer["edge_id"],),
                )
                heapq.heappush(queue, (new, transfer["target"]))
    return sorted(routes, key=lambda r: (r["source"], r["target"]))


def augment_groups(
    source, built, *, include_fallback=True, progress=lambda message: None, group_key_overrides=None
):
    document = built.document
    if not document.get("member_states"):
        augment_members(
            source,
            built,
            sample_capture=False,
            include_fallback=False,
            progress=progress,
        )
    states = document["member_states"]
    retained = [s for s in states if s["retained"]]
    by_id = {s["member_id"]: s for s in states}
    groups = defaultdict(list)
    for state in retained:
        groups[state["group_id"]].append(state)
    part = source.workpiece
    keys = {
        group: f"{part}:group:{group}:"
        + identity(
            [
                (
                    s["member_id"],
                    [
                        round(float(v), 12) + 0.0
                        for v in R.from_quat(s["quaternion_xyzw"]).as_quat(
                            canonical=True
                        )
                    ],
                )
                for s in sorted(members, key=lambda s: s["member_id"])
            ]
        )
        for group, members in groups.items()
    }
    if group_key_overrides:
        keys.update({g: group_key_overrides[str(g)] for g in groups})
    symmetries, continuous_axis, _ = _symmetry(source)
    energy = SeatedEnergy(
        np.asarray(built.mesh.convex_hull.vertices)
        - np.asarray(built.mesh.center_mass),
        document["alpha_deg"],
        document["beta_deg"],
    )
    aggregate = {}
    witness_keys = defaultdict(set)

    def add(a, b, commands, witness, *, composite=False):
        if not by_id[a]['retained'] or not by_id[b]['retained']:
            return
        if not include_fallback and composite:
            return
        source_group, target_group = by_id[a]["group_id"], by_id[b]["group_id"]
        if source_group == target_group or source_group is None or target_group is None:
            return
        if cartesian(commands):
            cmd = commands[0]
            angle = min(
                (-180, -90, 90, 180), key=lambda a: abs(a - cmd["signed_angle_deg"])
            )
            commands = [command(cmd["start_quaternion_xyzw"], cmd["axis"], angle)]
        signature = (
            source_group,
            target_group,
            tuple(
                (c["axis"], round(c["signed_angle_deg"], 10) + 0.0) for c in commands
            ),
        )
        witness = dict(
            witness,
            source_member_id=a,
            target_member_id=b,
            commands=commands,
            is_composite=composite,
        )
        record = aggregate.setdefault(
            signature,
            dict(
                source=source_group,
                target=target_group,
                edge_id=f"group:{source_group}->{target_group}:{identity(signature)}",
                witnesses=[],
            ),
        )
        fingerprint = identity(witness)
        if fingerprint not in witness_keys[signature]:
            witness_keys[signature].add(fingerprint)
            record["witnesses"].append(witness)

    # Preserve existing non-cardinal options, including captures already analysed.
    for transfer in document.get("member_transfers", []):
        for a in transfer["source_member_ids"]:
            for b in transfer["possible_target_member_ids"]:
                settling = [
                    s
                    for s in transfer.get("settling_segments", [])
                    if s["target_member_id"] == b
                ]
                add(
                    a,
                    b,
                    transfer["commands"],
                    dict(
                        origin_edge_id=transfer["edge_id"],
                        landing_model=transfer["transfer_model"],
                        settling_segments=settling,
                        endpoint_error_deg=transfer.get("endpoint_error_deg"),
                        possible_outcomes=[
                            dict(
                                member_id=k,
                                group_id=by_id[k]["group_id"],
                                retained=by_id[k]["retained"],
                            )
                            for k in transfer["possible_target_member_ids"]
                        ],
                    ),
                    composite=transfer["transfer_model"] == "composite_fallback",
                )
    representatives = {n["node_id"]: n["source_pose_ids"][0] for n in document["nodes"]}
    for transfer in document.get("composite_transfers", []):
        add(
            representatives[transfer["source"]],
            representatives[transfer["target"]],
            transfer["commands"],
            dict(
                origin_edge_id=transfer["edge_id"],
                landing_model="composite_endpoint",
                settling_segments=[],
                endpoint_error_deg=transfer["endpoint_error_deg"],
            ),
            composite=True,
        )

    # Exact commands are evaluated independently of the constrained action domains.
    axes_angles = [(axis, angle) for axis in "xyz" for angle in (-180, -90, 90, 180)]
    for index, state in enumerate(retained):
        commands = [
            command(state["quaternion_xyzw"], axis, angle)
            for axis, angle in axes_angles
        ]
        endpoints = R.from_quat([c["end_quaternion_xyzw"] for c in commands])
        outcomes = [[] for _ in commands]
        witnesses = [[] for _ in commands]
        for target in states:  # Excluded observations remain competing destinations.
            orientation = R.from_quat(target["quaternion_xyzw"])
            errors = endpoint_errors(
                endpoints, orientation, symmetries, continuous_axis
            )
            downhill, vectors, terminals = landing_paths(
                energy, endpoints, orientation, symmetries, continuous_axis
            )
            for i in np.flatnonzero(
                (errors <= ENDPOINT_TOLERANCE_DEG + 1e-10) | downhill
            ):
                outcomes[i].append(
                    dict(
                        member_id=target["member_id"],
                        group_id=target["group_id"],
                        retained=target["retained"],
                    )
                )
                if not target["retained"] or target["group_id"] == state["group_id"]:
                    continue
                observed = errors[i] <= ENDPOINT_TOLERANCE_DEG + 1e-10
                settling = (
                    []
                    if observed
                    else [
                        dict(
                            target_member_id=target["member_id"],
                            start_quaternion_xyzw=commands[i]["end_quaternion_xyzw"],
                            end_quaternion_xyzw=R.from_matrix(terminals[i])
                            .as_quat(canonical=True)
                            .tolist(),
                            rotation_vector_chute_rad=vectors[i].tolist(),
                            evidence_status="sampled_downhill_geometry",
                        )
                    ]
                )
                witnesses[i].append(
                    (
                        target["member_id"],
                        dict(
                            landing_model="observed_endpoint"
                            if observed
                            else "sampled_downhill",
                            landing_error_deg=float(errors[i]),
                            endpoint_error_deg=float(errors[i]) if observed else 0.0,
                            settling_segments=settling,
                        ),
                    )
                )
        for cmd, found, possible in zip(commands, witnesses, outcomes):
            for target_id, witness in found:
                add(
                    state["member_id"],
                    target_id,
                    [cmd],
                    dict(witness, possible_outcomes=possible),
                )
        progress(
            f"Cartesian group candidates: {part} member {index + 1}/{len(retained)}"
        )

    def finish():
        records = []
        for record in aggregate.values():
            witnesses = sorted(
                record["witnesses"],
                key=lambda w: (
                    bool(w.get("settling_segments")),
                    w["is_composite"],
                    w.get("endpoint_error_deg") or 0.0,
                    w["source_member_id"],
                    w["target_member_id"],
                    identity(w),
                ),
            )
            chosen = witnesses[0]
            commands = chosen["commands"]
            segments = [dict(c, segment_kind="command") for c in commands]
            segments += [
                dict(s, segment_kind="settling")
                for s in chosen.get("settling_segments", [])
            ]
            record = dict(
                record,
                witnesses=witnesses,
                commands=commands,
                directed=True,
                transition_kind="group_transfer",
                evidence_status="geometry_only",
                experimental_status="untested",
                actuation="group_reorientation",
                display_name=command_name(commands),
                cartesian_preferred=cartesian(commands),
                is_composite=all(w["is_composite"] for w in witnesses),
                settling_required=bool(chosen.get("settling_segments")),
                source_group_key=keys[record["source"]],
                target_group_key=keys[record["target"]],
                source_member_ids=sorted({w["source_member_id"] for w in witnesses}),
                possible_target_member_ids=sorted(
                    {w["target_member_id"] for w in witnesses}
                ),
                source_group_member_ids=sorted(
                    s["member_id"] for s in groups[record["source"]]
                ),
                target_group_member_ids=sorted(
                    s["member_id"] for s in groups[record["target"]]
                ),
                preview_source_member_id=chosen["source_member_id"],
                preview_target_member_id=chosen["target_member_id"],
                actuation_count=len(commands),
                total_absolute_angle_deg=sum(
                    abs(c["signed_angle_deg"]) for c in commands
                ),
                preview_segments=segments,
                planning_assumption=PLANNING_ASSUMPTION,
                contact_feasibility_evaluated=False,
            )
            record["preference_cost"] = list(preference(record))
            records.append(record)
        return sorted(records, key=lambda r: (*r["preference_cost"], r["edge_id"]))

    transfers = finish()
    components = connectivity(groups, transfers)["strongly_connected_components"]
    if include_fallback and len(components) > 1:
        for index, component in enumerate(components):
            following = components[(index + 1) % len(components)]
            if any(
                t["source"] in component and t["target"] in following for t in transfers
            ):
                continue
            candidates = []
            for source_group in component:
                for target_group in following:
                    for a in groups[source_group]:
                        for b in groups[target_group]:
                            candidate = composite_transfer(
                                a["member_id"],
                                b["member_id"],
                                a["quaternion_xyzw"],
                                b["quaternion_xyzw"],
                                symmetries,
                            )
                            candidates.append(
                                (
                                    candidate["actuation_count"],
                                    candidate["total_absolute_angle_deg"],
                                    candidate["axis_sequence"],
                                    candidate["symmetry_index"],
                                    a["member_id"],
                                    b["member_id"],
                                    candidate,
                                )
                            )
            *_, a, b, candidate = min(candidates, key=lambda row: row[:-1])
            add(
                a,
                b,
                candidate["commands"],
                dict(
                    landing_model="composite_endpoint",
                    settling_segments=[],
                    endpoint_error_deg=candidate["endpoint_error_deg"],
                    terminal_symmetry_quaternion_xyzw=candidate[
                        "terminal_symmetry_quaternion_xyzw"
                    ],
                ),
                composite=True,
            )
        transfers = finish()
    document["group_keys"] = {str(group): key for group, key in sorted(keys.items())}
    document["group_transfers"] = transfers
    document["group_routes"] = preferred_group_routes(groups, transfers)
    document.setdefault("connectivity", {})["groups"] = dict(
        cartesian=connectivity(
            groups, [t for t in transfers if t["cartesian_preferred"]]
        ),
        all_candidates=connectivity(groups, transfers),
        transfer_count=len(transfers),
        planning_assumption=PLANNING_ASSUMPTION,
        endpoint_tolerance_deg=ENDPOINT_TOLERANCE_DEG,
    )
    return document
