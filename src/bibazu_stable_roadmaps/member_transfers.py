"""Member-conditioned geometric transfers and sampled downhill capture evidence.

Group representatives are presentation anchors. Neither membership nor a small
barrier is a free transition between member orientations.
"""

from __future__ import annotations

from dataclasses import replace
import hashlib
import heapq
import json
import math

import networkx as nx
import numpy as np
from scipy.spatial.transform import Rotation as R

from .connectivity import composite_transfer, connectivity
from .inputs import ObservedPose, read_json, sha256
from ._engine.transitions import _ACTION_SPECS

ENERGY_TOLERANCE_MM = 1e-6
SETTLING_STEP_DEG = 0.1
CAPTURE_STEP_DEG = 1.0
BOUNDARY_STEP_DEG = 0.1
MAX_SETTLING_DEG = 60.0


def transfer_id(record):
    identity = {
        k: record.get(k)
        for k in (
            "source",
            "target",
            "source_member_ids",
            "possible_target_member_ids",
            "actuation",
            "capture_interval_deg",
            "transfer_model",
        )
    }
    identity["commands"] = [
        [c["axis"], round(c["signed_angle_deg"], 10) + 0.0] for c in record["commands"]
    ]
    digest = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:16]
    return f"member:{record['source']}->{record['target']}:{digest}"


def command(quat, axis, angle):
    start = R.from_quat(quat)
    vector = np.eye(3)["xyz".index(axis)]
    end = R.from_rotvec(np.deg2rad(angle) * vector) * start
    return dict(
        axis=axis,
        actuation=f"free_{axis}" if axis != "x" else "x",
        signed_angle_deg=float(angle),
        start_quaternion_xyzw=start.as_quat(canonical=True).tolist(),
        end_quaternion_xyzw=end.as_quat(canonical=True).tolist(),
    )


def load_members(source, document):
    catalogue = read_json(source.path)
    if "poses" not in catalogue:
        catalogue = read_json(source.path.with_name("poses.json"))
    rows = {str(p["id"]): p for p in catalogue["poses"]}
    groups = {}
    for node in document["nodes"]:
        row = rows.get(node["source_pose_ids"][0], {})
        members = node.get("group_members", row.get("group_members", node["source_pose_ids"]))
        for member in members:
            if member in groups:
                raise ValueError(f"Member belongs to more than one retained group: {member}")
            groups[member] = node["node_id"]
    original_path = source.path.with_name("original_observations.json")
    original_data = read_json(original_path) if original_path.is_file() else catalogue
    if original_data.get('workpiece', source.workpiece) != source.workpiece:
        raise ValueError('Original member observations belong to another workpiece')
    expected_hash = original_data.get('geometry', {}).get('stl_sha256')
    if expected_hash and expected_hash != sha256(source.mesh):
        raise ValueError('Original member observations use different geometry')
    originals = original_data['poses']
    by_id = {str(p["id"]): p for p in originals}
    if len(by_id) != len(originals) or set(groups) - set(by_id):
        raise ValueError(
            f"Missing or duplicate original member orientations: {sorted(set(groups) - set(by_id))}"
        )
    states = []
    for key, row in sorted(by_id.items()):
        q = np.asarray(row["quaternion_xyzw"], dtype=float)
        if q.shape != (4,) or not np.isfinite(q).all() or np.linalg.norm(q) < 1e-12:
            raise ValueError(f"Invalid orientation for group member {key}")
        q = R.from_quat(q).as_quat(canonical=True).tolist()
        states.append(
            dict(
                member_id=key,
                group_id=groups.get(key),
                quaternion_xyzw=q,
                position_com_chute_mm=row.get("position_com_chute_mm"),
                retained=key in groups,
                observed_count=row.get("count", 0),
            )
        )
    return states


class SeatedEnergy:
    def __init__(self, vertices, alpha_deg=45, beta_deg=0):
        self.vertices = np.asarray(vertices, dtype=float)
        chute = R.from_euler("y", beta_deg, degrees=True) * R.from_euler(
            "x", alpha_deg, degrees=True
        )
        self.gravity = chute.inv().apply([0.0, 0.0, -1.0])

    def heights(self, rotations):
        points = np.einsum("...ij,vj->...vi", rotations, self.vertices)
        return self.gravity[1] * points[..., 1].min(axis=-1) + self.gravity[2] * points[..., 2].min(
            axis=-1
        )

    def downhill(self, endpoints, target, symmetries, continuous_axis=None):
        """Evaluate shortest symmetry paths, retaining the actual sampled witness."""
        endpoints = np.asarray(endpoints).reshape(-1, 3, 3)
        target_variants = (target * symmetries).as_matrix()
        vectors = R.from_matrix(
            (target_variants[None] @ endpoints[:, None].transpose(0, 1, 3, 2)).reshape(-1, 3, 3)
        ).as_rotvec()
        vectors = vectors.reshape(len(endpoints), len(target_variants), 3)
        if continuous_axis is not None:
            axis = np.asarray(continuous_axis, dtype=float)
            axis /= np.linalg.norm(axis)
            u = endpoints @ axis
            v = target.as_matrix() @ axis
            cross = np.cross(u, v)
            angles = np.arccos(np.clip(u @ v, -1.0, 1.0))
            norms = np.linalg.norm(cross, axis=1)
            singular = norms < 1e-10
            for i in np.flatnonzero(singular & (angles > 1e-8)):
                cross[i] = np.cross(u[i], np.eye(3)[np.argmin(np.abs(u[i]))])
            norms = np.linalg.norm(cross, axis=1)
            rv = cross / np.maximum(norms[:, None], 1e-30) * angles[:, None]
        else:
            lengths = np.linalg.norm(vectors, axis=2)
            best = np.argmin(lengths, axis=1)
            rv = vectors[np.arange(len(endpoints)), best]
        angles = np.rad2deg(np.linalg.norm(rv, axis=1))
        target_matrices = R.from_rotvec(rv).as_matrix() @ endpoints
        start_h = self.heights(endpoints)
        end_h = self.heights(target_matrices)
        exact = angles <= 1e-6
        eligible = (angles <= MAX_SETTLING_DEG + 1e-9) & (
            (end_h < start_h - ENERGY_TOLERANCE_MM) | exact
        )
        accepted = exact.copy()
        for batch_start in range(0, len(endpoints), 32):
            indices = (
                np.flatnonzero(
                    eligible[batch_start : batch_start + 32]
                    & ~exact[batch_start : batch_start + 32]
                )
                + batch_start
            )
            if not len(indices):
                continue
            # A shared grid is at least as fine as 0.1 degrees for every path.
            fractions = np.linspace(
                0.0, 1.0, max(2, math.ceil(angles[indices].max() / SETTLING_STEP_DEG) + 1)
            )
            matrices = R.from_rotvec(
                (rv[indices, None] * fractions[None, :, None]).reshape(-1, 3)
            ).as_matrix()
            matrices = matrices.reshape(len(indices), -1, 3, 3) @ endpoints[indices, None]
            heights = self.heights(matrices)
            accepted[indices] = np.all(np.diff(heights, axis=1) <= ENERGY_TOLERANCE_MM, axis=1)
        return accepted, rv, target_matrices


def capture_samples(source_quat, axis, domain, states, energy, symmetries, continuous_axis=None):
    start = R.from_quat(source_quat)
    vector = np.eye(3)["xyz".index(axis)]
    cache = {}

    def evaluate(angles):
        missing = sorted({round(float(a), 8) for a in angles} - cache.keys())
        if not missing:
            return
        endpoints = (R.from_rotvec(np.deg2rad(missing)[:, None] * vector) * start).as_matrix()
        outcomes = [[] for _ in missing]
        for state in states:
            accepted, _, _ = energy.downhill(
                endpoints, R.from_quat(state["quaternion_xyzw"]), symmetries, continuous_axis
            )
            for i in np.flatnonzero(accepted):
                outcomes[i].append(state["member_id"])
        for angle, found in zip(missing, outcomes):
            cache[angle] = tuple(sorted(found))

    coarse = np.arange(domain[0], domain[1] + CAPTURE_STEP_DEG / 2, CAPTURE_STEP_DEG)
    evaluate(coarse)
    refine = []
    for a, b in zip(coarse[:-1], coarse[1:]):
        if cache[round(float(a), 8)] != cache[round(float(b), 8)]:
            refine.extend(np.linspace(a, b, round((b - a) / BOUNDARY_STEP_DEG) + 1))
    evaluate(refine)
    # Zero is a no-op, not an actuated transfer or a bridge over unresolved space.
    samples = [(a, cache[a]) for a in sorted(cache) if abs(a) > 1e-9]
    runs = []
    for angle, outcome in samples:
        if runs and runs[-1]["outcomes"] == outcome and not (runs[-1]["angles"][-1] < 0 < angle):
            runs[-1]["angles"].append(angle)
        else:
            runs.append(dict(angles=[angle], outcomes=outcome))
    return runs


def member_routes(states, transfers):
    """Search belief states: every possible arrival must support the next action."""
    retained = {s["member_id"]: s for s in states if s["retained"]}
    routes = []
    for source in sorted(retained):
        queue = [((0, 0, 0.0, 0, ()), (source,), ())]
        visited, targets = set(), set()
        while queue:
            cost, possible, chain = heapq.heappop(queue)
            if possible in visited:
                continue
            visited.add(possible)
            group = retained[possible[0]]["group_id"]
            if group not in targets:
                targets.add(group)
                routes.append(
                    dict(
                        source=retained[source]["group_id"],
                        source_member_id=source,
                        target=group,
                        component_edge_ids=list(cost[4]),
                        possible_target_member_ids=list(possible),
                        member_chain=[list(x) for x in ((source,),) + chain],
                        actuation_count=cost[1],
                        composite_transfer_count=cost[0],
                        total_absolute_angle_deg=cost[2],
                        conditional=True,
                        evidence_status="geometry_only",
                    )
                )
            for transfer in transfers:
                if not set(possible).issubset(transfer["source_member_ids"]):
                    continue
                result = tuple(sorted(transfer["possible_target_member_ids"]))
                if not result or result in visited or any(k not in retained for k in result):
                    continue
                if len({retained[k]["group_id"] for k in result}) != 1:
                    continue
                new = (
                    cost[0] + int(transfer["transfer_model"] == "composite_fallback"),
                    cost[1] + transfer["actuation_count"],
                    cost[2] + transfer["total_absolute_angle_deg"],
                    cost[3] + int(transfer["transfer_model"] == "downhill_capture"),
                    cost[4] + (transfer["edge_id"],),
                )
                heapq.heappush(queue, (new, result, chain + (result,)))
    return sorted(routes, key=lambda r: (r["source_member_id"], r["target"]))


def augment_members(
    source, built, *, sample_capture=True, include_fallback=True, progress=lambda message: None
):
    from .roadmap import build_roadmap, _symmetry

    doc = built.document
    states = load_members(source, doc)
    retained = [s for s in states if s["retained"]]
    by_id = {s["member_id"]: s for s in states}
    poses = tuple(
        ObservedPose(s["member_id"], tuple(s["quaternion_xyzw"]), s["observed_count"], 0.0, i)
        for i, s in enumerate(retained)
    )
    member_source = replace(source, poses=poses)
    geometric = build_roadmap(member_source, [(p, i) for i, p in enumerate(poses)], progress)
    symmetries, continuous_axis, _ = _symmetry(source)
    transfers, captures = [], []

    def base(source_member, target_members, model, action, commands):
        target_members = sorted(target_members)
        return dict(
            source=by_id[source_member]["group_id"],
            target=by_id[target_members[0]]["group_id"],
            source_member_ids=[source_member],
            possible_target_member_ids=target_members,
            transfer_model=model,
            actuation=action,
            commands=commands,
            actuation_count=len(commands),
            total_absolute_angle_deg=sum(abs(c["signed_angle_deg"]) for c in commands),
            evidence_status="geometry_only",
            directed=True,
            conditional=True,
            experimental_status="untested",
            capture_interval_deg=None,
            settling_segments=[],
        )

    for edge in geometric.document["edges"]:
        a, b = retained[edge["source"]], retained[edge["target"]]
        axis = "x" if "main_" in edge["actuation"] else edge["actuation"][-1]
        record = base(
            a["member_id"],
            [b["member_id"]],
            "known_member_endpoint",
            edge["actuation"],
            [command(a["quaternion_xyzw"], axis, edge["signed_angle_deg"])],
        )
        record["axis_error_deg"] = edge["axis_error_deg"]
        record["edge_id"] = transfer_id(record)
        transfers.append(record)

    if sample_capture:
        mesh = built.mesh
        energy = SeatedEnergy(
            np.asarray(mesh.convex_hull.vertices) - np.asarray(mesh.center_mass),
            doc["alpha_deg"],
            doc["beta_deg"],
        )
        for index, state in enumerate(retained):
            node = geometric.document["nodes"][index]
            for action, (_, domain) in _ACTION_SPECS.items():
                if action.startswith("floor_main_") and not node["main_face_on_floor"]:
                    continue
                if action.startswith("wall_main_") and not node["main_face_on_wall"]:
                    continue
                if (
                    action in {"floor_main_pos_x", "wall_main_neg_x"}
                    and doc["main_face_min_span_mm"] <= doc["opposite_x_min_height_mm"]
                ):
                    continue
                axis = "x" if "main_" in action else action[-1]
                progress(f"Sampling capture angles for {state['member_id']}: {action}")
                runs = capture_samples(
                    state["quaternion_xyzw"],
                    axis,
                    domain,
                    states,
                    energy,
                    symmetries,
                    continuous_axis,
                )
                evidence = dict(source_member_id=state["member_id"], actuation=action, intervals=[])
                for run in runs:
                    outcomes = run["outcomes"]
                    groups = {by_id[k]["group_id"] for k in outcomes}
                    interval = [min(run["angles"]), max(run["angles"])]
                    status = (
                        "unique_group"
                        if outcomes and len(groups) == 1 and None not in groups
                        else "unresolved_or_competing"
                    )
                    evidence["intervals"].append(
                        dict(
                            interval_deg=interval,
                            possible_target_member_ids=list(outcomes),
                            status=status,
                            sample_count=len(run["angles"]),
                        )
                    )
                    if status != "unique_group" or set(outcomes) == {state["member_id"]}:
                        continue
                    nominal = min(
                        run["angles"], key=lambda a: (abs(a - sum(interval) / 2), abs(a), a)
                    )
                    cmds = [command(state["quaternion_xyzw"], axis, nominal)]
                    record = base(state["member_id"], outcomes, "downhill_capture", action, cmds)
                    record.update(
                        capture_interval_deg=interval,
                        capture_width_deg=interval[1] - interval[0],
                        sample_count=len(run["angles"]),
                    )
                    landing = R.from_quat(cmds[-1]["end_quaternion_xyzw"])
                    for target in outcomes:
                        _, rv, terminal = energy.downhill(
                            landing.as_matrix()[None],
                            R.from_quat(by_id[target]["quaternion_xyzw"]),
                            symmetries,
                            continuous_axis,
                        )
                        record["settling_segments"].append(
                            dict(
                                target_member_id=target,
                                start_quaternion_xyzw=landing.as_quat(canonical=True).tolist(),
                                end_quaternion_xyzw=R.from_matrix(terminal[0])
                                .as_quat(canonical=True)
                                .tolist(),
                                rotation_vector_chute_rad=rv[0].tolist(),
                                evidence_status="sampled_downhill_geometry",
                            )
                        )
                    record["edge_id"] = transfer_id(record)
                    transfers.append(record)
                captures.append(evidence)
            progress(
                f"Capture intervals checked for member {index + 1}/{len(retained)}: {state['member_id']}"
            )

    # Connect actual states, not the optimistic group quotient. Only deterministic
    # arrivals can join this fallback graph without an unobserved member switch.
    graph = nx.DiGraph()
    graph.add_nodes_from(s["member_id"] for s in retained)
    graph.add_edges_from(
        (t["source_member_ids"][0], t["possible_target_member_ids"][0])
        for t in transfers
        if len(t["possible_target_member_ids"]) == 1
    )
    components = sorted(
        (sorted(c) for c in nx.strongly_connected_components(graph)), key=lambda c: c[0]
    )
    if include_fallback and len(components) > 1:
        for i, component in enumerate(components):
            following = components[(i + 1) % len(components)]
            if any(graph.has_edge(a, b) for a in component for b in following):
                continue
            choices = [
                composite_transfer(
                    a, b, by_id[a]["quaternion_xyzw"], by_id[b]["quaternion_xyzw"], symmetries
                )
                for a in component
                for b in following
            ]
            chosen = min(
                choices,
                key=lambda t: (
                    t["actuation_count"],
                    t["total_absolute_angle_deg"],
                    t["axis_sequence"],
                    t["symmetry_index"],
                    t["source"],
                    t["target"],
                ),
            )
            record = base(
                chosen["source"],
                [chosen["target"]],
                "composite_fallback",
                "member_composite",
                chosen["commands"],
            )
            record["edge_id"] = transfer_id(record)
            transfers.append(record)
    routes = member_routes(states, transfers)
    group_ids = [n["node_id"] for n in doc["nodes"]]
    inter = [t for t in transfers if t["source"] != t["target"]]
    coverage = {
        s["member_id"]: sorted(
            {r["target"] for r in routes if r["source_member_id"] == s["member_id"]}
        )
        for s in retained
    }
    doc.update(
        member_states=states,
        member_transfers=transfers,
        member_routes=routes,
        capture_analysis=dict(
            model="sampled_seated_downhill_v1",
            action_step_deg=CAPTURE_STEP_DEG,
            boundary_step_deg=BOUNDARY_STEP_DEG,
            settling_step_deg=SETTLING_STEP_DEG,
            maximum_settling_angle_deg=MAX_SETTLING_DEG,
            energy_tolerance_mm=ENERGY_TOLERANCE_MM,
            grouping_barrier_used_as_passive_permission=False,
            samples=captures,
        ),
    )
    doc.setdefault("connectivity", {})["members"] = dict(
        group_overview=connectivity(group_ids, inter),
        known_member_inter_group_action_count=sum(
            t["transfer_model"] == "known_member_endpoint" for t in inter
        ),
        source_member_coverage=coverage,
        every_source_member_reaches_every_group=all(
            set(v) == set(group_ids) for v in coverage.values()
        ),
        note="Group overview is existential. Executable route candidates preserve possible member states; profiles require explicit source coverage.",
    )
    return doc
