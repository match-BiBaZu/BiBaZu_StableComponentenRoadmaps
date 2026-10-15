"""Offline geometry verification and member-route materialization."""

from __future__ import annotations

import heapq
import math


def multiply(a, b):
    x, y, z, w = a
    X, Y, Z, W = b
    return (
        w * X + x * W + y * Z - z * Y,
        w * Y - x * Z + y * W + z * X,
        w * Z + x * Y - y * X + z * W,
        w * W - x * X - y * Y - z * Z,
    )


def quaternion(value):
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        raise ValueError("Expected an xyzw quaternion")
    q = tuple(float(v) for v in value)
    norm = math.sqrt(sum(v * v for v in q))
    if not all(math.isfinite(v) for v in q) or abs(norm - 1) > 1e-6:
        raise ValueError("Invalid unit quaternion")
    return q


def error_deg(a, b):
    # Relative quaternion avoids the precision loss of acos near identity.
    relative = multiply(a, (-b[0], -b[1], -b[2], b[3]))
    return math.degrees(
        2 * math.atan2(math.sqrt(sum(v * v for v in relative[:3])), abs(relative[3]))
    )


def rotate(q, axis, angle):
    half = math.radians(angle) / 2
    vector = [0.0, 0.0, 0.0, math.cos(half)]
    vector["xyz".index(axis)] = math.sin(half)
    return multiply(vector, q)


def validate_commands(commands):
    if not isinstance(commands, (list, tuple)):
        raise ValueError("Composite commands must be a list")
    result = []
    for raw in commands:
        if not isinstance(raw, dict) or raw.get("axis") not in {"x", "y", "z"}:
            raise ValueError("Invalid composite command axis")
        angle = float(raw["signed_angle_deg"])
        if not math.isfinite(angle) or abs(angle) > 180 + 1e-7:
            raise ValueError("Invalid composite command angle")
        start = quaternion(raw["start_quaternion_xyzw"])
        end = quaternion(raw["end_quaternion_xyzw"])
        if error_deg(rotate(start, raw["axis"], angle), end) > 1e-6:
            raise ValueError("Composite command endpoint mismatch")
        result.append(
            dict(
                raw,
                signed_angle_deg=angle,
                start_quaternion_xyzw=list(start),
                end_quaternion_xyzw=list(end),
            )
        )
    return tuple(result)


def validate_transfer(raw, poses):
    if not isinstance(raw, dict) or raw.get("transition_kind") != "composite_candidate":
        raise ValueError("Invalid composite transfer")
    if raw.get("evidence_status") != "geometry_only" or raw.get("directed") is not True:
        raise ValueError("Composite transfers must be directed geometry-only candidates")
    source, target = int(raw["source"]), int(raw["target"])
    if source not in poses or target not in poses or source == target:
        raise ValueError("Composite transfer references an unknown or identical pose")
    commands = validate_commands(raw["commands"])
    if len(commands) != raw.get("actuation_count"):
        raise ValueError("Composite actuation count mismatch")
    current = quaternion(poses[source])
    for command in commands:
        if (
            command["axis"] not in {"y", "z"}
            or error_deg(current, command["start_quaternion_xyzw"]) > 1e-6
        ):
            raise ValueError("Invalid composite command chain")
        current = command["end_quaternion_xyzw"]
    terminal = quaternion(raw["terminal_quaternion_xyzw"])
    expected = multiply(
        quaternion(poses[target]), quaternion(raw["terminal_symmetry_quaternion_xyzw"])
    )
    if error_deg(current, terminal) > 1e-6 or error_deg(terminal, expected) > 1e-6:
        raise ValueError("Composite transfer endpoint mismatch")
    if not str(raw.get("edge_id", "")).startswith("composite:"):
        raise ValueError("Invalid composite transfer ID")
    return commands


def preferred_path(edges, start, target):
    """One deterministic preferred simple path; O(E log V), no depth-three cap.

    Edges are portable dicts with source/target, edge_id, commands and angle.
    """
    adjacency = {}
    for edge in edges:
        adjacency.setdefault(edge["source"], []).append(edge)
    queue = [((0, 0, 0.0, ()), start, ())]
    visited = set()
    while queue:
        cost, pose, path = heapq.heappop(queue)
        if pose in visited:
            continue
        visited.add(pose)
        if pose == target:
            return path
        for edge in adjacency.get(pose, ()):
            if edge["target"] in visited:
                continue
            commands = edge.get("commands", ())
            composite = edge.get("evidence_status") == "geometry_only"
            new = (
                cost[0] + int(composite),
                cost[1] + edge.get("actuation_count", 1),
                cost[2]
                + sum(abs(c["signed_angle_deg"]) for c in commands)
                + (0 if commands else abs(edge.get("signed_angle_deg") or 0)),
                cost[3] + (edge["edge_id"],),
            )
            # IDs are unique, so path dictionaries are never heap tie breakers.
            heapq.heappush(queue, (new, edge["target"], path + (edge,)))
    return ()


def command_frame(commands, progress):
    """Interpolate along the specified axes, rather than an endpoint SLERP."""
    if not commands:
        return None
    scaled = min(1.0, max(0.0, progress)) * len(commands)
    index = min(int(scaled), len(commands) - 1)
    command = commands[index]
    return rotate(
        command["start_quaternion_xyzw"],
        command["axis"],
        command["signed_angle_deg"] * min(1.0, scaled - index),
    )


def validate_members(payload):
    """Validate the optional member graph without changing legacy schema-v1 data."""
    states = payload.get("member_states", [])
    transfers = payload.get("member_transfers", [])
    if not isinstance(states, list) or not isinstance(transfers, list):
        raise ValueError("Member states and transfers must be lists")
    by_id = {}
    groups = {
        int(n.get("node_id", n.get("id"))) for n in payload.get("nodes", payload.get("poses", []))
    }
    for state in states:
        key = str(state["member_id"])
        if key in by_id:
            raise ValueError("Duplicate member state")
        quaternion(state["quaternion_xyzw"])
        if state["retained"] and state["group_id"] not in groups:
            raise ValueError("Unknown member group")
        by_id[key] = state
    ids = set()
    for transfer in transfers:
        key = transfer["edge_id"]
        if key in ids or not key.startswith("member:"):
            raise ValueError("Invalid or duplicate member transfer ID")
        ids.add(key)
        if transfer.get("evidence_status") != "geometry_only" or not transfer.get("directed"):
            raise ValueError("Member candidates must be directed geometry-only transfers")
        for field, group_field in (
            ("source_member_ids", "source"),
            ("possible_target_member_ids", "target"),
        ):
            if not transfer.get(field):
                raise ValueError("Member transfer has no member applicability")
            for member in transfer[field]:
                if (
                    member not in by_id
                    or not by_id[member]["retained"]
                    or by_id[member]["group_id"] != transfer[group_field]
                ):
                    raise ValueError("Member transfer references unknown/incompatible member")
        commands = validate_commands(transfer["commands"])
        if len(commands) != transfer["actuation_count"]:
            raise ValueError("Member actuation count mismatch")
        current = by_id[transfer["source_member_ids"][0]]["quaternion_xyzw"]
        for cmd in commands:
            if error_deg(current, cmd["start_quaternion_xyzw"]) > 1e-6:
                raise ValueError("Member command continuity mismatch")
            current = cmd["end_quaternion_xyzw"]
        interval = transfer.get("capture_interval_deg")
        if interval is not None and (
            len(interval) != 2
            or not all(math.isfinite(float(v)) for v in interval)
            or interval[0] > interval[1]
            or abs(interval[0]) > 180.000001
            or abs(interval[1]) > 180.000001
        ):
            raise ValueError("Invalid capture interval")
        for segment in transfer.get("settling_segments", []):
            quaternion(segment["start_quaternion_xyzw"])
            quaternion(segment["end_quaternion_xyzw"])
            if error_deg(current, segment["start_quaternion_xyzw"]) > 1e-6:
                raise ValueError("Settling segment does not start at landing")
    # Do not trust exported macro routes to teleport between member states.
    known = {t["edge_id"]: t for t in transfers}
    for route in payload.get("member_routes", []):
        possible = {route["source_member_id"]}
        if not possible.issubset(by_id):
            raise ValueError("Unknown route source member")
        for key in route["component_edge_ids"]:
            transfer = known.get(key)
            if transfer is None or not possible.issubset(transfer["source_member_ids"]):
                raise ValueError("Member route has incompatible arrival/departure members")
            possible = set(transfer["possible_target_member_ids"])
        if not possible or any(by_id[k]["group_id"] != route["target"] for k in possible):
            raise ValueError("Member route target mismatch")
        if possible != set(route["possible_target_member_ids"]):
            raise ValueError("Member route outcome mismatch")
    return tuple(states), tuple(transfers)


def member_route_record(route, transfers):
    import hashlib

    by_id = {t["edge_id"]: t for t in transfers}
    legs = [by_id[key] for key in route["component_edge_ids"]]
    if not legs:
        return None
    if len(legs) == 1:
        return legs[0]
    digest = hashlib.sha256("|".join(route["component_edge_ids"]).encode()).hexdigest()[:16]
    return dict(
        edge_id=f"member-route:{route['source_member_id']}->{route['target']}:{digest}",
        source=route["source"],
        target=route["target"],
        source_member_ids=[route["source_member_id"]],
        possible_target_member_ids=route["possible_target_member_ids"],
        directed=True,
        commands=[c for leg in legs for c in leg["commands"]],
        actuation_count=route["actuation_count"],
        evidence_status="geometry_only",
        transfer_model="member_route",
        actuation="member_route",
        component_edge_ids=route["component_edge_ids"],
        via_pose_ids=[leg["target"] for leg in legs[:-1]],
        capture_interval_deg=None,
        settling_segments=[],
        legs=legs,
        member_chain=route["member_chain"],
    )


def member_preview(context, progress):
    """Preview actuation and each supported settling branch, without a free switch."""
    segments = []
    for leg in context.get("legs", [context]):
        segments.extend(("command", c) for c in leg.get("commands", []))
        # All branches are shown independently. A new leg never follows an
        # arbitrary selected branch: its source applicability was validated.
        segments.extend(("settling", s) for s in leg.get("settling_segments", []))
    if not segments:
        return None
    position = min(1.0, max(0.0, progress)) * len(segments)
    index = min(int(position), len(segments) - 1)
    kind, segment = segments[index]
    fraction = min(1.0, position - index)
    if kind == "command":
        return rotate(
            segment["start_quaternion_xyzw"],
            segment["axis"],
            segment["signed_angle_deg"] * fraction,
        )
    vector = segment["rotation_vector_chute_rad"]
    angle = math.sqrt(sum(float(v) ** 2 for v in vector))
    if angle < 1e-15:
        return segment["start_quaternion_xyzw"]
    rotation = tuple(float(v) / angle * math.sin(angle * fraction / 2) for v in vector) + (
        math.cos(angle * fraction / 2),
    )
    return multiply(rotation, segment["start_quaternion_xyzw"])


def source_coverage(raw, allowed):
    if not isinstance(raw, (list, tuple)) or any(not isinstance(v, str) for v in raw):
        raise ValueError("Source-member coverage must be a list of member IDs")
    if len(set(raw)) != len(raw) or not set(raw).issubset(allowed):
        raise ValueError("Source-member coverage contains duplicate or unknown members")
    return tuple(sorted(raw))
