"""Direct observed-pose geometry, without enumerating or classifying poses."""
from __future__ import annotations

from dataclasses import dataclass, replace
import math

import numpy as np
from scipy.spatial.transform import Rotation

from .inputs import PoseSource, ObservedPose
from ._engine.contacts import ContactPose, _affine_dimension, _extract_support_faces, _with_contact_details
from ._engine.geometry import load_solid_mesh
from ._engine.symmetry import detect_rotational_symmetry
from ._engine.transitions import _ACTION_SPECS, _best_actuated_relation, _planar_face_min_span_mm, PracticalPoseClass

AXIS_TOLERANCE_DEG = 1.0
OPPOSITE_X_MIN_HEIGHT_MM = 25.0


@dataclass
class BuiltRoadmap:
    source: PoseSource
    numbered: list[tuple[ObservedPose, int]]
    contacts: dict[int, ContactPose]
    mesh: object
    document: dict
    warnings: list[str]


def _contact_pose(number, quaternion, hull_vertices, mesh_vertices, edges, triangles, faces, tolerance):
    rotation = Rotation.from_quat(quaternion).as_matrix()
    vertices = hull_vertices @ rotation.T
    floor = np.flatnonzero(vertices[:, 2] <= vertices[:, 2].min() + tolerance)
    wall = np.flatnonzero(vertices[:, 1] <= vertices[:, 1].min() + tolerance)
    floor_dimension = _affine_dimension(vertices[floor][:, (0, 1)], tolerance)
    wall_dimension = _affine_dimension(vertices[wall][:, (0, 2)], tolerance)
    # Observations are authoritative even for point/edge supports. No rejection,
    # reseating rotation, theoretical catalogue lookup, or clustering occurs.
    pose = ContactPose(number, tuple(float(q) for q in quaternion),
                       tuple(tuple(float(v) for v in row) for row in rotation),
                       (0.0, -float(vertices[:, 1].min()), -float(vertices[:, 2].min())),
                       floor_dimension, wall_dimension, tuple(int(v) for v in floor), tuple(int(v) for v in wall),
                       (), (), (), (), "unknown", "unknown", (), (), ("observed_simulation",))
    return _with_contact_details(pose, mesh_vertices, edges, triangles, faces, tolerance)


def _symmetry(source: PoseSource):
    raw = source.recognition.get("symmetry_quaternions_xyzw")
    axis = source.recognition.get("continuous_axis_part")
    if raw is None:
        group = detect_rotational_symmetry(source.mesh, tolerance_mm=.05)
        quats = Rotation.from_matrix(np.asarray([e.rotation_part_from_part for e in group.elements])).as_quat()
        axis = group.continuous_axis_part
        symbol = group.symbol
    else:
        quats = np.asarray(raw, dtype=float)
        if quats.ndim != 2 or quats.shape[1] != 4 or not len(quats) or not np.isfinite(quats).all():
            raise ValueError("Invalid source symmetry quaternions.")
        norms = np.linalg.norm(quats, axis=1)
        if np.any(norms < 1e-12) or not np.isfinite(norms).all():
            raise ValueError("Invalid source symmetry quaternion length.")
        quats = quats / norms[:, None]
        symbol = source.recognition.get("symmetry_symbol", "C1")
    if axis is not None:
        axis = np.asarray(axis, dtype=float)
        if axis.shape != (3,) or not np.isfinite(axis).all() or np.linalg.norm(axis) < 1e-12:
            raise ValueError("Invalid continuous part symmetry axis.")
        axis /= np.linalg.norm(axis)
    # Include the original orientation as a connection representation regardless
    # of whether a third-party symmetry list explicitly contains identity.
    rotations = Rotation.from_quat(np.vstack(([0, 0, 0, 1], quats)))
    return rotations, axis, symbol


def build_roadmap(source: PoseSource, numbered: list[tuple[ObservedPose, int]], progress=lambda message: None) -> BuiltRoadmap:
    if not numbered:
        raise ValueError("No retained observed poses to generate.")
    mesh = load_solid_mesh(source.mesh)
    center = np.asarray(mesh.center_mass, dtype=float)
    hull = mesh.convex_hull
    hull_vertices = np.asarray(hull.vertices) - center
    mesh_vertices = np.asarray(mesh.vertices) - center
    mesh_edges = np.asarray(mesh.edges_unique, dtype=int)
    triangles = np.asarray(mesh.faces, dtype=int)
    tolerance = max(.05, float(np.max(mesh.extents)) * 1e-4)
    faces = _extract_support_faces(hull, angular_tolerance_deg=.1,
                                   distance_tolerance_mm=max(1e-9, float(np.max(mesh.extents)) * 1e-6))
    main_face = max(faces, key=lambda face: face.area_mm2)
    main_faces = tuple(face for face in faces if math.isclose(face.area_mm2, main_face.area_mm2, rel_tol=1e-6, abs_tol=1e-6))
    main_ids = tuple(face.face_id for face in main_faces)
    min_span = min(_planar_face_min_span_mm(hull_vertices[list(face.vertex_indices)]) for face in main_faces)
    symmetries, continuous_axis, symbol = _symmetry(source)
    contacts, variants, classes, nodes, warnings = {}, {}, [], [], []
    progress(f"Reading geometry for {len(numbered)} retained observed poses")
    for pose, node_id in numbered:
        contact = _contact_pose(node_id, pose.quaternion_xyzw, hull_vertices, mesh_vertices, mesh_edges, triangles, faces, tolerance)
        contacts[node_id] = contact
        member_ids = []
        for quat in (Rotation.from_quat(pose.quaternion_xyzw) * symmetries).as_quat():
            member = len(variants)
            variants[member] = _contact_pose(member, quat, hull_vertices, mesh_vertices, mesh_edges, triangles, faces, tolerance)
            member_ids.append(member)
        classes.append(PracticalPoseClass(node_id, node_id, tuple(member_ids)))
        on_floor = any(set(main_ids).intersection(variants[pid].floor_face_ids) for pid in member_ids)
        on_wall = any(set(main_ids).intersection(variants[pid].wall_face_ids) for pid in member_ids)
        if contact.floor_contact_dimension < 1 or contact.wall_contact_dimension < 1:
            warnings.append(f"{pose.source_id}: uncertain/point contact; pose retained, constrained connections may be unavailable")
        nodes.append({
            "node_id": node_id, "pose_ids": [pose.source_index], "original_catalog_pose_id": pose.source_index,
            "source_pose_ids": [pose.source_id], "kind": "robust", "classification_basis": "observed_simulation",
            "cad_status": "provisional", "representative_quaternion_xyzw": list(pose.quaternion_xyzw),
            "floor_contact_topology": contact.floor_contact_topology, "wall_contact_topology": contact.wall_contact_topology,
            "main_face_on_floor": on_floor, "main_face_on_wall": on_wall,
            "observed_count": pose.count, "observed_frequency_percent": pose.frequency_percent,
            "rocking_barrier_mm": None, "csa_stability_index": None, "csa_applicable": None,
            "csa_feasible_fraction": None, "csa_feasible_solid_angle_sr": None, "csa_angular_clearance_deg": None,
            "classical_metrics": {},
        })
    nodes_by_id = {node["node_id"]: node for node in nodes}
    edges = []
    progress("Calculating direct geometric connections (no stability filtering)")
    for source_class in classes:
        for target_class in classes:
            if source_class.class_id == target_class.class_id:
                continue
            for action, (axis, domain) in _ACTION_SPECS.items():
                node = nodes_by_id[source_class.class_id]
                if action.startswith("floor_main_") and not node["main_face_on_floor"]:
                    continue
                if action.startswith("wall_main_") and not node["main_face_on_wall"]:
                    continue
                if action in {"floor_main_pos_x", "wall_main_neg_x"} and min_span <= OPPOSITE_X_MIN_HEIGHT_MM:
                    continue
                # S_target * inverse(S_source) is another group element: fixing
                # the source representative avoids a quadratic symmetry search.
                fixed_source = replace(source_class, pose_ids=source_class.pose_ids[:1])
                relation = _best_actuated_relation(fixed_source, target_class, variants, action,
                                                   main_ids, AXIS_TOLERANCE_DEG, continuous_axis)
                if relation is None:
                    continue
                error, angle, _, _ = relation
                from_id, to_id = source_class.class_id, target_class.class_id
                edges.append({
                    "edge_id": f"a{len(edges)}:{from_id}->{to_id}:{action}", "source": from_id, "target": to_id,
                    "transition_kind": "actuated", "actuation": action, "directed": True,
                    "axis_chute": axis.tolist(), "signed_angle_deg": angle, "axis_error_deg": error,
                    "capture_interval_deg": None, "capture_width_deg": None, "capture_fraction": None,
                    "target_barrier_score": None, "geometric_score": None, "escape_barrier_mm": None,
                    "saddle_angle_deg": None, "settling_pose_ids": [], "actuation_count": 1,
                    "experimental_status": "untested",
                })
        progress(f"Connections checked for pose {source_class.class_id}")
    def angle(key, default):
        value = source.config.get(key, default)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"Invalid {key} in source config.json.")
        return value
    document = {
        "schema_version": 1, "source": f"source/{source.mesh.name}", "geometry_status": "provisional",
        "alpha_deg": angle("alpha_deg", 45), "beta_deg": angle("beta_deg", 0),
        "symmetry_symbol": symbol, "symmetry_tolerance_mm": .05,
        "main_face_id": main_face.face_id, "main_face_ids": list(main_ids),
        "main_face_area_mm2": main_face.area_mm2, "main_face_min_span_mm": min_span,
        "opposite_x_min_height_mm": OPPOSITE_X_MIN_HEIGHT_MM, "axis_tolerance_deg": AXIS_TOLERANCE_DEG,
        "contact_tolerance_mm": tolerance, "pose_ranking_method": "observed_frequency",
        "robustness_method": "observed_simulation", "robust_barrier_threshold_mm": None,
        "minimum_csa_score": None, "minimum_braking_g": None, "csa_load_model": None,
        "csa_cap_half_angle_deg": None, "csa_direction_samples": None,
        "friction_policy": "not_evaluated", "csa_rocking_fallback_pose_ids": [],
        "unresolved_metastable_node_ids": [], "nodes": nodes, "edges": edges,
        "node_counts": {"total": len(nodes), "robust": len(nodes), "metastable": 0},
        "analytical_stability_evaluated": False, "catalogue_id_namespace": "input_pose_list_index",
        "classification_note": "Legacy robust labels designate observed stable targets for consumer compatibility; no analytical robustness is asserted.",
    }
    return BuiltRoadmap(source, numbered, contacts, mesh, document, warnings)


def handover_dict(document: dict) -> dict:
    poses = []
    for node in document["nodes"]:
        poses.append({"id": node["node_id"], "original_catalog_pose_id": node["original_catalog_pose_id"],
                      "equivalent_catalog_pose_ids": node["pose_ids"], "source_pose_ids": node["source_pose_ids"],
                      "stability": node["kind"], "planner_role": "stable_target", "classification_basis": "observed_simulation",
                      "orientation_quaternion_xyzw": node["representative_quaternion_xyzw"],
                      "observed_count": node["observed_count"], "observed_frequency_percent": node["observed_frequency_percent"],
                      "rocking_barrier_mm": None, "csa_stability_index": None, "cad_status": "provisional",
                      "csa_feasible_fraction": None, "csa_feasible_solid_angle_sr": None,
                      "csa_angular_clearance_deg": None, "csa_applicable": None,
                      "contacts": {"floor": node["floor_contact_topology"], "wall": node["wall_contact_topology"],
                                   "main_face_on_floor": node["main_face_on_floor"], "main_face_on_wall": node["main_face_on_wall"]}})
    transitions = []
    for edge in document["edges"]:
        action = edge["actuation"]
        axis = "x" if "main_" in action else action[-1]
        surface = "main_face_on_floor" if action.startswith("floor_main_") else "main_face_on_wall" if action.startswith("wall_main_") else None
        extra = "main_face_min_span_above_threshold" if action in {"floor_main_pos_x", "wall_main_neg_x"} else None
        transitions.append({"id": edge["edge_id"], "from_pose": edge["source"], "to_pose": edge["target"],
                            "directed": True, "type": "actuated", "action": {
                                "name": action, "axis": axis, "axis_vector_chute": edge["axis_chute"],
                                "direction": "positive" if edge["signed_angle_deg"] > 0 else "negative",
                                "commanded_angle_deg": edge["signed_angle_deg"], "impulse_cost": 1,
                                "surface_requirement": surface, "additional_requirement": extra},
                            "capture": {"interval_deg": None, "width_deg": None, "fraction": None},
                            "geometry": {"geometric_score": None, "target_barrier_score": None,
                                         "passive_escape_barrier_mm": None, "passive_saddle_angle_deg": None,
                                         "axis_error_deg": edge["axis_error_deg"], "passive_settling_via_catalog_pose_ids": []},
                            "experimental": {"status": "untested", "trials": None, "successes": None,
                                             "empirical_success_rate": None, "difficulty_rating": None, "notes": ""}})
    return {"format": "bibazu_pose_roadmap_handover", "schema_version": 1,
            "part": {"name": document["part_name"], "mesh_source": document["source"], "cad_status": "provisional"},
            "chute": {"coordinate_system": "right_handed", "x": "downhill", "y": "away_from_wall", "z": "away_from_floor",
                      "alpha_deg": document["alpha_deg"], "beta_deg": document["beta_deg"]},
            "classification": {"basis": "observed_simulation", "analytical_stability_evaluated": False,
                               "note": document["classification_note"], "pose_ranking_method": document["pose_ranking_method"],
                               "robustness_method": "observed_simulation", "symmetry": document["symmetry_symbol"],
                               "friction_policy": document["friction_policy"],
                               "robust_pose_ids": [n["node_id"] for n in document["nodes"]], "metastable_pose_ids": [],
                               "unresolved_metastable_pose_ids": [], "main_face_ids": document["main_face_ids"],
                               "main_face_min_span_mm": document["main_face_min_span_mm"],
                               "opposite_x_min_height_mm": document["opposite_x_min_height_mm"],
                               "robust_barrier_threshold_mm": None, "minimum_csa_score": None,
                               "csa_cap_half_angle_deg": None, "csa_direction_samples": None,
                               "csa_rocking_fallback_catalog_pose_ids": [],
                               "classical_metadata": document.get("classical_metadata", {})},
            "poses": poses, "transitions": transitions, "generation": document.get("generation", {})}
