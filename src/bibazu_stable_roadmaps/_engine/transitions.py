"""Geometric action rules extracted from the MIT geometry-to-pose engine.
No stability, capture-basin, or ranking code is included.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
from scipy.spatial.transform import Rotation
from .contacts import ContactPose

@dataclass(frozen=True)
class PracticalPoseClass:
    class_id: int
    representative_pose_id: int
    pose_ids: tuple[int, ...]

_ACTION_SPECS: dict[str, tuple[np.ndarray, tuple[float, float]]] = {'floor_main_neg_x': (np.array([1.0, 0.0, 0.0]), (-180.0, 0.0)), 'floor_main_pos_x': (np.array([1.0, 0.0, 0.0]), (0.0, 180.0)), 'wall_main_neg_x': (np.array([1.0, 0.0, 0.0]), (-180.0, 0.0)), 'wall_main_pos_x': (np.array([1.0, 0.0, 0.0]), (0.0, 180.0)), 'free_y': (np.array([0.0, 1.0, 0.0]), (-180.0, 180.0)), 'free_z': (np.array([0.0, 0.0, 1.0]), (-180.0, 180.0))}

def _planar_face_min_span_mm(points: np.ndarray) -> float:
    """Return the smaller intrinsic PCA span of one planar support face."""
    centered = np.asarray(points, dtype=float) - np.mean(points, axis=0)
    _, _, axes = np.linalg.svd(centered, full_matrices=False)
    coordinates = centered @ axes[:2].T
    spans = np.ptp(coordinates, axis=0)
    positive = spans[spans > 1e-08]
    return float(np.min(positive)) if len(positive) else 0.0

def _best_actuated_relation(source_class: PracticalPoseClass, target_class: PracticalPoseClass, poses: dict[int, ContactPose], action: str, main_face_ids: tuple[int, ...], axis_tolerance_deg: float, continuous_axis_part: np.ndarray | None=None) -> tuple[float, float, int, int] | None:
    axis, domain = _ACTION_SPECS[action]
    face_ids = set(main_face_ids)
    best: tuple[float, float, int, int] | None = None
    for source_pose_id in source_class.pose_ids:
        source_pose = poses[source_pose_id]
        if action.startswith('floor_main_') and (not face_ids.intersection(source_pose.floor_face_ids)):
            continue
        if action.startswith('wall_main_') and (not face_ids.intersection(source_pose.wall_face_ids)):
            continue
        source_rotation = np.asarray(source_pose.rotation_chute_from_part, dtype=float)
        for target_pose_id in target_class.pose_ids:
            target_rotation = np.asarray(poses[target_pose_id].rotation_chute_from_part, dtype=float)
            if continuous_axis_part is None:
                rotvec = Rotation.from_matrix(target_rotation @ source_rotation.T).as_rotvec()
                angle_rad = float(np.linalg.norm(rotvec))
                if angle_rad <= 1e-09:
                    continue
                unit = rotvec / angle_rad
                alignment = float(np.dot(unit, axis))
                axis_error = math.degrees(math.acos(float(np.clip(abs(alignment), -1.0, 1.0))))
                signed_angle = math.degrees(angle_rad) * (1.0 if alignment >= 0.0 else -1.0)
            else:
                source_axis = source_rotation @ continuous_axis_part
                target_axis = target_rotation @ continuous_axis_part
                source_perpendicular = source_axis - np.dot(source_axis, axis) * axis
                target_perpendicular = target_axis - np.dot(target_axis, axis) * axis
                source_norm = float(np.linalg.norm(source_perpendicular))
                target_norm = float(np.linalg.norm(target_perpendicular))
                if source_norm <= 1e-10 or target_norm <= 1e-10:
                    signed_angle = 0.0
                else:
                    source_perpendicular /= source_norm
                    target_perpendicular /= target_norm
                    signed_angle = math.degrees(math.atan2(float(np.dot(axis, np.cross(source_perpendicular, target_perpendicular))), float(np.dot(source_perpendicular, target_perpendicular))))
                rotated_axis = Rotation.from_rotvec(math.radians(signed_angle) * axis).as_matrix() @ source_axis
                axis_error = math.degrees(math.acos(float(np.clip(np.dot(rotated_axis, target_axis), -1.0, 1.0))))
                if abs(signed_angle) <= 1e-09 and axis_error <= axis_tolerance_deg:
                    continue
            if axis_error > axis_tolerance_deg:
                continue
            if abs(abs(signed_angle) - 180.0) <= 1e-07:
                if action in {'floor_main_neg_x', 'wall_main_neg_x'}:
                    signed_angle = -180.0
                elif action in {'floor_main_pos_x', 'wall_main_pos_x'}:
                    signed_angle = 180.0
            if signed_angle < domain[0] - 1e-07 or signed_angle > domain[1] + 1e-07:
                continue
            candidate = (axis_error, signed_angle, source_pose_id, target_pose_id)
            if best is None or (candidate[0], abs(candidate[1])) < (best[0], abs(best[1])):
                best = candidate
    return best
