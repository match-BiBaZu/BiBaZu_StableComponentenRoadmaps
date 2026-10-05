"""Detection of practical discrete rotational symmetries and pose quotients."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation

from .contacts import PoseCatalog, build_pose_catalog
from .geometry import detect_continuous_revolution_axis, load_solid_mesh


@dataclass(frozen=True, slots=True)
class SymmetryElement:
    """One proper rotation which approximately maps the part onto itself."""

    element_id: int
    rotation_part_from_part: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ]
    angle_deg: float
    mapping_error_mm: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RotationalSymmetryGroup:
    """Finite practical symmetry group found on a triangulated solid."""

    source: str
    symbol: str
    tolerance_mm: float
    elements: tuple[SymmetryElement, ...]
    continuous_axis_part: tuple[float, float, float] | None = None

    @property
    def order(self) -> int:
        return len(self.elements)

    @property
    def is_continuous(self) -> bool:
        return self.continuous_axis_part is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "symbol": self.symbol,
            "order": self.order,
            "tolerance_mm": self.tolerance_mm,
            "continuous": self.is_continuous,
            "continuous_axis_part": self.continuous_axis_part,
            "elements": [element.to_dict() for element in self.elements],
        }


@dataclass(frozen=True, slots=True)
class PoseEquivalenceClass:
    """Catalog poses representing the same physical orientation."""

    class_id: int
    representative_pose_id: int
    pose_ids: tuple[int, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SymmetryReducedCatalog:
    """The quotient of a pose catalog by the part's rotation group."""

    symmetry: RotationalSymmetryGroup
    classes: tuple[PoseEquivalenceClass, ...]
    angular_tolerance_deg: float

    def class_for_pose(self, pose_id: int) -> PoseEquivalenceClass:
        for equivalence_class in self.classes:
            if pose_id in equivalence_class.pose_ids:
                return equivalence_class
        raise KeyError(pose_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "symmetry": self.symmetry.to_dict(),
            "angular_tolerance_deg": self.angular_tolerance_deg,
            "class_count": len(self.classes),
            "classes": [value.to_dict() for value in self.classes],
        }


def _rotation_tuple(rotation: np.ndarray) -> tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]:
    return tuple(tuple(float(value) for value in row) for row in rotation)  # type: ignore[return-value]


def _axis_rotation(axis: np.ndarray, angle: float) -> np.ndarray:
    unit_axis = np.asarray(axis, dtype=float)
    unit_axis /= np.linalg.norm(unit_axis)
    return Rotation.from_rotvec(unit_axis * angle).as_matrix()


def _mapping_error(
    vertices_centered: np.ndarray,
    vertex_tree: cKDTree,
    rotation: np.ndarray,
) -> float:
    transformed = (rotation @ vertices_centered.T).T
    forward = float(np.max(vertex_tree.query(transformed)[0]))
    backward = float(np.max(cKDTree(transformed).query(vertices_centered)[0]))
    return max(forward, backward)


def _rotation_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(Rotation.from_matrix(a.T @ b).magnitude())


def detect_rotational_symmetry(
    mesh_path: str | Path,
    *,
    tolerance_mm: float | None = None,
    relative_tolerance: float = 0.005,
    maximum_cyclic_order: int = 12,
) -> RotationalSymmetryGroup:
    """Detect finite rotations around mass-principal axes.

    The comparison deliberately permits a small geometric deviation. This is
    needed for exported CAD meshes such as Df1a, whose nominally repeated
    sectors differ by roughly 0.32 mm. The used tolerance is always reported.
    """

    if maximum_cyclic_order < 2:
        raise ValueError("maximum_cyclic_order must be at least 2.")
    if not math.isfinite(relative_tolerance) or relative_tolerance <= 0.0:
        raise ValueError("relative_tolerance must be a positive finite number.")

    mesh = load_solid_mesh(mesh_path)
    vertices = np.asarray(mesh.vertices, dtype=float) - np.asarray(
        mesh.center_mass, dtype=float
    )
    length_scale = max(float(np.max(mesh.extents)), 1e-9)
    used_tolerance = (
        length_scale * relative_tolerance if tolerance_mm is None else tolerance_mm
    )
    if not math.isfinite(used_tolerance) or used_tolerance <= 0.0:
        raise ValueError("tolerance_mm must be a positive finite number.")

    continuous = detect_continuous_revolution_axis(
        mesh,
        tolerance_mm=used_tolerance,
        relative_tolerance=relative_tolerance,
    )
    if continuous is not None:
        identity = SymmetryElement(
            element_id=0,
            rotation_part_from_part=_rotation_tuple(np.eye(3)),
            angle_deg=0.0,
            mapping_error_mm=continuous.maximum_support_variation_mm,
        )
        return RotationalSymmetryGroup(
            source=str(Path(mesh_path).expanduser().resolve()),
            symbol="Cinf",
            tolerance_mm=float(used_tolerance),
            elements=(identity,),
            continuous_axis_part=continuous.axis_part,
        )

    vertex_tree = cKDTree(vertices)
    _, principal_axes = np.linalg.eigh(np.asarray(mesh.moment_inertia, dtype=float))
    rotations: list[tuple[np.ndarray, float]] = [(np.eye(3), 0.0)]
    detected_orders: list[int] = []

    for axis in principal_axes.T:
        detected_order = 1
        for order in range(maximum_cyclic_order, 1, -1):
            candidates = [
                _axis_rotation(axis, 2.0 * math.pi * step / order)
                for step in range(1, order)
            ]
            errors = [
                _mapping_error(vertices, vertex_tree, candidate)
                for candidate in candidates
            ]
            if all(error <= used_tolerance for error in errors):
                detected_order = order
                for candidate, error in zip(candidates, errors):
                    if all(
                        _rotation_distance(candidate, known) > 1e-7
                        for known, _ in rotations
                    ):
                        rotations.append((candidate, error))
                break
        if detected_order > 1:
            detected_orders.append(detected_order)

    rotations.sort(
        key=lambda item: (
            round(float(Rotation.from_matrix(item[0]).magnitude()), 12),
            *np.round(Rotation.from_matrix(item[0]).as_quat(), 12).tolist(),
        )
    )
    elements = tuple(
        SymmetryElement(
            element_id=index,
            rotation_part_from_part=_rotation_tuple(rotation),
            angle_deg=math.degrees(float(Rotation.from_matrix(rotation).magnitude())),
            mapping_error_mm=error,
        )
        for index, (rotation, error) in enumerate(rotations)
    )
    if len(detected_orders) == 1 and len(elements) == detected_orders[0]:
        symbol = f"C{detected_orders[0]}"
    elif len(elements) == 1:
        symbol = "C1"
    else:
        symbol = f"finite-SO3-order-{len(elements)}"
    return RotationalSymmetryGroup(
        source=str(Path(mesh_path).expanduser().resolve()),
        symbol=symbol,
        tolerance_mm=float(used_tolerance),
        elements=elements,
    )


def reduce_catalog_by_symmetry(
    catalog: PoseCatalog,
    symmetry: RotationalSymmetryGroup,
    *,
    angular_tolerance_deg: float = 0.25,
) -> SymmetryReducedCatalog:
    """Group rotations ``R`` and ``R @ S`` for every detected symmetry ``S``."""

    if not math.isfinite(angular_tolerance_deg) or angular_tolerance_deg <= 0.0:
        raise ValueError("angular_tolerance_deg must be a positive finite number.")
    tolerance = math.radians(angular_tolerance_deg)
    pose_rotations = [
        np.asarray(pose.rotation_chute_from_part, dtype=float) for pose in catalog.poses
    ]
    symmetry_rotations = [
        np.asarray(element.rotation_part_from_part, dtype=float)
        for element in symmetry.elements
    ]
    parents = list(range(len(catalog.poses)))

    if symmetry.order == 1 and not symmetry.is_continuous:
        return SymmetryReducedCatalog(
            symmetry=symmetry,
            classes=tuple(
                PoseEquivalenceClass(
                    class_id=index,
                    representative_pose_id=pose.pose_id,
                    pose_ids=(pose.pose_id,),
                )
                for index, pose in enumerate(catalog.poses)
            ),
            angular_tolerance_deg=angular_tolerance_deg,
        )

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(first: int, second: int) -> None:
        first_root = find(first)
        second_root = find(second)
        if first_root != second_root:
            parents[second_root] = first_root

    if symmetry.continuous_axis_part is not None:
        axis = np.asarray(symmetry.continuous_axis_part, dtype=float)
        oriented_axes = np.asarray(
            [rotation @ axis for rotation in pose_rotations], dtype=float
        )
        axis_tree = cKDTree(oriented_axes)
        chord_tolerance = 2.0 * math.sin(tolerance / 2.0) + 1e-12
        for first, first_axis in enumerate(oriented_axes):
            for second in axis_tree.query_ball_point(
                first_axis, chord_tolerance
            ):
                if second <= first:
                    continue
                separation = math.acos(
                    float(
                        np.clip(
                            np.dot(first_axis, oriented_axes[second]),
                            -1.0,
                            1.0,
                        )
                    )
                )
                if separation <= tolerance:
                    union(first, second)
    else:
        pose_quaternions = Rotation.from_matrix(
            np.asarray(pose_rotations)
        ).as_quat()
        quaternion_tree = cKDTree(
            np.vstack((pose_quaternions, -pose_quaternions))
        )
        tree_pose_ids = np.tile(
            np.arange(len(pose_rotations), dtype=int), 2
        )
        chord_tolerance = 2.0 * math.sin(tolerance / 4.0) + 1e-12
        for first, first_rotation in enumerate(pose_rotations):
            for symmetry_rotation in symmetry_rotations:
                target = first_rotation @ symmetry_rotation
                target_quaternion = Rotation.from_matrix(target).as_quat()
                for tree_index in quaternion_tree.query_ball_point(
                    target_quaternion, chord_tolerance
                ):
                    second = int(tree_pose_ids[tree_index])
                    if second <= first:
                        continue
                    relative = first_rotation.T @ pose_rotations[second]
                    if (
                        _rotation_distance(relative, symmetry_rotation)
                        <= tolerance
                    ):
                        union(first, second)

    grouped: dict[int, list[int]] = {}
    for pose in catalog.poses:
        grouped.setdefault(find(pose.pose_id), []).append(pose.pose_id)
    pose_groups = sorted(tuple(sorted(group)) for group in grouped.values())
    classes = tuple(
        PoseEquivalenceClass(
            class_id=index,
            representative_pose_id=pose_ids[0],
            pose_ids=pose_ids,
        )
        for index, pose_ids in enumerate(pose_groups)
    )
    return SymmetryReducedCatalog(
        symmetry=symmetry,
        classes=classes,
        angular_tolerance_deg=angular_tolerance_deg,
    )


def build_symmetry_reduced_catalog(
    mesh_path: str | Path,
    *,
    tolerance_mm: float | None = None,
    relative_tolerance: float = 0.005,
    angular_tolerance_deg: float = 0.25,
) -> tuple[PoseCatalog, SymmetryReducedCatalog]:
    """Convenience wrapper building and reducing a theoretical catalog."""

    catalog = build_pose_catalog(mesh_path)
    symmetry = detect_rotational_symmetry(
        mesh_path,
        tolerance_mm=tolerance_mm,
        relative_tolerance=relative_tolerance,
    )
    return catalog, reduce_catalog_by_symmetry(
        catalog, symmetry, angular_tolerance_deg=angular_tolerance_deg
    )
