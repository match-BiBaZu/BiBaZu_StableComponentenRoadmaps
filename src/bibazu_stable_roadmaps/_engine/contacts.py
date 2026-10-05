"""Exact theoretical floor-wall contact-pose enumeration."""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass, replace
from itertools import product
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.spatial import ConvexHull
from scipy.spatial.transform import Rotation

from .geometry import detect_continuous_revolution_axis, load_solid_mesh

Vector3 = NDArray[np.float64]
Matrix3 = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class SupportFace:
    """One maximal coplanar polygon on the oriented convex hull."""

    face_id: int
    normal_part: tuple[float, float, float]
    plane_offset_mm: float
    vertex_indices: tuple[int, ...]
    area_mm2: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ContactPose:
    """A theoretical orientation with non-point floor and wall contact."""

    pose_id: int
    quaternion_xyzw: tuple[float, float, float, float]
    rotation_chute_from_part: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ]
    translation_to_corner_mm: tuple[float, float, float]
    floor_contact_dimension: int
    wall_contact_dimension: int
    floor_contact_vertex_indices: tuple[int, ...]
    wall_contact_vertex_indices: tuple[int, ...]
    floor_mesh_contact_vertex_indices: tuple[int, ...]
    wall_mesh_contact_vertex_indices: tuple[int, ...]
    floor_mesh_contact_edges: tuple[tuple[int, int], ...]
    wall_mesh_contact_edges: tuple[tuple[int, int], ...]
    floor_contact_topology: str
    wall_contact_topology: str
    floor_face_ids: tuple[int, ...]
    wall_face_ids: tuple[int, ...]
    provenance: tuple[str, ...]

    @property
    def floor_contact_type(self) -> str:
        return _dimension_name(self.floor_contact_dimension)

    @property
    def wall_contact_type(self) -> str:
        return _dimension_name(self.wall_contact_dimension)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["floor_contact_type"] = self.floor_contact_type
        result["wall_contact_type"] = self.wall_contact_type
        return result


@dataclass(frozen=True, slots=True)
class PoseCatalog:
    """All theoretical physical floor-wall contact orientations."""

    source: str
    units: str
    center_mass_part_mm: tuple[float, float, float]
    support_faces: tuple[SupportFace, ...]
    poses: tuple[ContactPose, ...]
    contact_tolerance_mm: float
    rotation_tolerance_rad: float
    continuous_symmetry_axis_part: tuple[float, float, float] | None = None
    point_contacts_excluded: bool = True
    edge_edge_contacts_excluded: bool = True
    continuous_symmetry_edge_edge_exception: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "units": self.units,
            "center_mass_part_mm": self.center_mass_part_mm,
            "support_faces": [face.to_dict() for face in self.support_faces],
            "poses": [pose.to_dict() for pose in self.poses],
            "contact_tolerance_mm": self.contact_tolerance_mm,
            "rotation_tolerance_rad": self.rotation_tolerance_rad,
            "continuous_symmetry_axis_part": self.continuous_symmetry_axis_part,
            "point_contacts_excluded": self.point_contacts_excluded,
            "edge_edge_contacts_excluded": self.edge_edge_contacts_excluded,
            "continuous_symmetry_edge_edge_exception": (
                self.continuous_symmetry_edge_edge_exception
            ),
        }


def _dimension_name(dimension: int) -> str:
    return {0: "point", 1: "edge", 2: "face"}.get(dimension, "invalid")


def _rotation_axis(axis: int, angle: float) -> Matrix3:
    c = math.cos(angle)
    s = math.sin(angle)
    if axis == 0:  # X
        return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])
    if axis == 1:  # Y
        return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])
    if axis == 2:  # Z
        return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    raise ValueError(f"Unsupported rotation axis: {axis}")


def _rotation_from_to(source: Vector3, target: Vector3) -> Matrix3:
    a = np.asarray(source, dtype=float).copy()
    b = np.asarray(target, dtype=float).copy()
    a /= np.linalg.norm(a)
    b /= np.linalg.norm(b)
    dot = float(np.clip(np.dot(a, b), -1.0, 1.0))

    if dot > 1.0 - 1e-12:
        return np.eye(3)
    if dot < -1.0 + 1e-12:
        basis = np.eye(3)[int(np.argmin(np.abs(a)))]
        axis = np.cross(a, basis)
        axis /= np.linalg.norm(axis)
        return Rotation.from_rotvec(math.pi * axis).as_matrix()

    axis = np.cross(a, b)
    axis /= np.linalg.norm(axis)
    return Rotation.from_rotvec(math.acos(dot) * axis).as_matrix()


def _extract_support_faces(
    hull,
    *,
    angular_tolerance_deg: float,
    distance_tolerance_mm: float,
) -> tuple[SupportFace, ...]:
    normals = np.asarray(hull.face_normals, dtype=float).copy()
    triangles = np.asarray(hull.triangles, dtype=float).copy()
    faces = np.asarray(hull.faces, dtype=int).copy()
    areas = np.asarray(hull.area_faces, dtype=float).copy()
    cos_tolerance = float(np.cos(np.deg2rad(angular_tolerance_deg)))

    groups: list[dict[str, Any]] = []
    for triangle_index, (normal, triangle) in enumerate(zip(normals, triangles)):
        normal /= np.linalg.norm(normal)
        offset = float(np.dot(normal, triangle[0]))
        match = None
        for group in groups:
            if (
                float(np.dot(normal, group["normal"])) >= cos_tolerance
                and abs(offset - group["offset"]) <= distance_tolerance_mm
            ):
                match = group
                break
        if match is None:
            match = {
                "normal": normal,
                "offset": offset,
                "vertices": set(),
                "area": 0.0,
            }
            groups.append(match)
        match["vertices"].update(int(index) for index in faces[triangle_index])
        match["area"] += float(areas[triangle_index])

    groups.sort(
        key=lambda group: (
            *np.round(group["normal"], 10).tolist(),
            round(group["offset"], 10),
        )
    )
    return tuple(
        SupportFace(
            face_id=face_id,
            normal_part=tuple(float(value) for value in group["normal"]),
            plane_offset_mm=float(group["offset"]),
            vertex_indices=tuple(sorted(group["vertices"])),
            area_mm2=float(group["area"]),
        )
        for face_id, group in enumerate(groups)
    )


def _reduce_continuous_face_orbits(
    support_faces: tuple[SupportFace, ...],
    axis_part: tuple[float, float, float],
    center_mass_part: NDArray[np.float64],
    *,
    angular_tolerance_deg: float,
    distance_tolerance_mm: float,
) -> tuple[SupportFace, ...]:
    """Keep one representative plane from every SO(2) face orbit."""

    axis = np.asarray(axis_part, dtype=float)
    axis /= np.linalg.norm(axis)
    center_mass = np.asarray(center_mass_part, dtype=float)
    angular_tolerance = math.sin(math.radians(angular_tolerance_deg))
    groups: list[list[SupportFace]] = []
    signatures: list[tuple[float, float]] = []
    for face in support_faces:
        axial_normal = float(np.dot(face.normal_part, axis))
        centered_offset = face.plane_offset_mm - float(
            np.dot(face.normal_part, center_mass)
        )
        match = next(
            (
                index
                for index, (known_axial, known_offset) in enumerate(signatures)
                if abs(axial_normal - known_axial) <= angular_tolerance
                and abs(centered_offset - known_offset) <= distance_tolerance_mm
            ),
            None,
        )
        if match is None:
            signatures.append((axial_normal, centered_offset))
            groups.append([face])
        else:
            groups[match].append(face)
    representatives = [max(group, key=lambda face: face.area_mm2) for group in groups]
    representatives.sort(
        key=lambda face: (
            round(float(np.dot(face.normal_part, axis)), 10),
            round(face.plane_offset_mm, 10),
            face.face_id,
        )
    )
    return tuple(
        replace(face, face_id=index) for index, face in enumerate(representatives)
    )


def _unique_points(points: NDArray[np.float64], tolerance: float) -> NDArray[np.float64]:
    scale = max(tolerance, np.finfo(float).eps)
    keys = np.round(points / scale).astype(np.int64)
    _, first_indices = np.unique(keys, axis=0, return_index=True)
    return points[np.sort(first_indices)]


def _silhouette_edges(
    rotated_vertices: NDArray[np.float64], projection_axes: tuple[int, int], tolerance: float
) -> Iterable[tuple[Vector3, Vector3]]:
    projected = _unique_points(rotated_vertices[:, projection_axes], tolerance)
    if len(projected) < 3:
        return ()
    hull_2d = ConvexHull(projected)
    polygon = projected[hull_2d.vertices]
    return tuple(
        (polygon[index], polygon[(index + 1) % len(polygon)])
        for index in range(len(polygon))
    )


def _affine_dimension(points: NDArray[np.float64], tolerance: float) -> int:
    if len(points) == 0:
        return -1
    if len(points) == 1:
        return 0
    centered = points - points[0]
    singular_values = np.linalg.svd(centered, compute_uv=False)
    return int(np.count_nonzero(singular_values > tolerance))


def _contact_topology(
    contact_indices: NDArray[np.int64],
    mesh_edges: NDArray[np.int64],
    mesh_faces: NDArray[np.int64],
) -> tuple[str, tuple[tuple[int, int], ...]]:
    """Describe connected mesh features in one geometric support set.

    Convex support dimension alone cannot distinguish a real face from, for
    example, an edge plus a remote outlet point.  This routine uses the full
    STL adjacency and deliberately reports disconnected point supports.
    """

    contact_set = {int(index) for index in contact_indices}
    if not contact_set:
        return "none", ()
    contact_edges = tuple(
        sorted(
            tuple(sorted((int(first), int(second))))
            for first, second in mesh_edges
            if int(first) in contact_set and int(second) in contact_set
        )
    )
    adjacency = {index: set() for index in contact_set}
    for first, second in contact_edges:
        adjacency[first].add(second)
        adjacency[second].add(first)

    components: list[set[int]] = []
    remaining = set(contact_set)
    while remaining:
        seed = remaining.pop()
        component = {seed}
        stack = [seed]
        while stack:
            current = stack.pop()
            neighbors = adjacency[current].intersection(remaining)
            remaining.difference_update(neighbors)
            component.update(neighbors)
            stack.extend(neighbors)
        components.append(component)

    component_by_vertex = {
        vertex: component_index
        for component_index, component in enumerate(components)
        for vertex in component
    }
    components_with_faces: set[int] = set()
    for face in mesh_faces:
        face_vertices = tuple(int(vertex) for vertex in face)
        if all(vertex in contact_set for vertex in face_vertices):
            components_with_faces.add(component_by_vertex[face_vertices[0]])
    components_with_edges = {
        component_by_vertex[first] for first, _ in contact_edges
    }

    pieces: list[str] = []
    for component_index, component in enumerate(components):
        contains_face = component_index in components_with_faces
        contains_edge = component_index in components_with_edges
        if contains_face:
            pieces.append("face")
        elif contains_edge:
            pieces.append("edge")
        else:
            pieces.extend("point" for _ in component)

    counts = {piece: pieces.count(piece) for piece in ("face", "edge", "point")}
    terms: list[str] = []
    for piece in ("face", "edge", "point"):
        count = counts[piece]
        if count == 1:
            terms.append(piece)
        elif count > 1:
            terms.append(f"{count}-{piece}")
    return "+".join(terms), contact_edges


def _canonical_quaternion(rotation: Matrix3) -> tuple[float, float, float, float]:
    quaternion = Rotation.from_matrix(rotation).as_quat()
    if quaternion[3] < -1e-14:
        quaternion = -quaternion
    elif abs(quaternion[3]) <= 1e-14:
        first_nonzero = next((value for value in quaternion[:3] if abs(value) > 1e-14), 1.0)
        if first_nonzero < 0.0:
            quaternion = -quaternion
    return tuple(float(value) for value in quaternion)


def _face_ids_in_contact(
    contact_indices: NDArray[np.int64], support_faces: tuple[SupportFace, ...]
) -> tuple[int, ...]:
    contact_set = {int(index) for index in contact_indices}
    return tuple(
        face.face_id
        for face in support_faces
        if set(face.vertex_indices).issubset(contact_set)
    )


def _make_candidate(
    rotation: Matrix3,
    vertices_centered: NDArray[np.float64],
    mesh_vertices_centered: NDArray[np.float64],
    mesh_edges: NDArray[np.int64],
    mesh_faces: NDArray[np.int64],
    support_faces: tuple[SupportFace, ...],
    contact_tolerance_mm: float,
    provenance: str,
    *,
    allow_edge_edge: bool = False,
    include_contact_details: bool = True,
) -> ContactPose | None:
    rotated = (rotation @ vertices_centered.T).T
    min_y = float(np.min(rotated[:, 1]))
    min_z = float(np.min(rotated[:, 2]))
    floor_indices = np.flatnonzero(rotated[:, 2] <= min_z + contact_tolerance_mm)
    wall_indices = np.flatnonzero(rotated[:, 1] <= min_y + contact_tolerance_mm)

    floor_dimension = _affine_dimension(
        rotated[floor_indices][:, (0, 1)], contact_tolerance_mm
    )
    wall_dimension = _affine_dimension(
        rotated[wall_indices][:, (0, 2)], contact_tolerance_mm
    )

    # Pure point contacts are transitions. Edge-edge configurations have a
    # remaining rotational degree of freedom and are not isolated poses.
    if floor_dimension < 1 or wall_dimension < 1:
        return None
    if floor_dimension < 2 and wall_dimension < 2 and not allow_edge_edge:
        return None

    if include_contact_details:
        rotated_mesh = (rotation @ mesh_vertices_centered.T).T
        mesh_floor_indices = np.flatnonzero(
            rotated_mesh[:, 2]
            <= float(np.min(rotated_mesh[:, 2])) + contact_tolerance_mm
        )
        mesh_wall_indices = np.flatnonzero(
            rotated_mesh[:, 1]
            <= float(np.min(rotated_mesh[:, 1])) + contact_tolerance_mm
        )
        floor_topology, floor_mesh_edges = _contact_topology(
            mesh_floor_indices, mesh_edges, mesh_faces
        )
        wall_topology, wall_mesh_edges = _contact_topology(
            mesh_wall_indices, mesh_edges, mesh_faces
        )
        floor_face_ids = _face_ids_in_contact(floor_indices, support_faces)
        wall_face_ids = _face_ids_in_contact(wall_indices, support_faces)
    else:
        mesh_floor_indices = np.empty(0, dtype=np.int64)
        mesh_wall_indices = np.empty(0, dtype=np.int64)
        floor_mesh_edges = ()
        wall_mesh_edges = ()
        floor_topology = _dimension_name(floor_dimension)
        wall_topology = _dimension_name(wall_dimension)
        floor_face_ids = ()
        wall_face_ids = ()

    matrix_tuple = tuple(
        tuple(float(value) for value in row) for row in np.asarray(rotation)
    )
    return ContactPose(
        pose_id=-1,
        quaternion_xyzw=_canonical_quaternion(rotation),
        rotation_chute_from_part=matrix_tuple,  # type: ignore[arg-type]
        translation_to_corner_mm=(0.0, -min_y, -min_z),
        floor_contact_dimension=floor_dimension,
        wall_contact_dimension=wall_dimension,
        floor_contact_vertex_indices=tuple(int(index) for index in floor_indices),
        wall_contact_vertex_indices=tuple(int(index) for index in wall_indices),
        floor_mesh_contact_vertex_indices=tuple(
            int(index) for index in mesh_floor_indices
        ),
        wall_mesh_contact_vertex_indices=tuple(
            int(index) for index in mesh_wall_indices
        ),
        floor_mesh_contact_edges=floor_mesh_edges,
        wall_mesh_contact_edges=wall_mesh_edges,
        floor_contact_topology=floor_topology,
        wall_contact_topology=wall_topology,
        floor_face_ids=floor_face_ids,
        wall_face_ids=wall_face_ids,
        provenance=(provenance,),
    )


def _with_contact_details(
    candidate: ContactPose,
    mesh_vertices_centered: NDArray[np.float64],
    mesh_edges: NDArray[np.int64],
    mesh_faces: NDArray[np.int64],
    support_faces: tuple[SupportFace, ...],
    contact_tolerance_mm: float,
    *,
    force_dimension_topology: bool = False,
    topology_cache: ContactTopologyCache | None = None,
    face_contact_cache: FaceContactCache | None = None,
) -> ContactPose:
    """Populate full-mesh contact metadata after rotation deduplication."""

    rotation = np.asarray(candidate.rotation_chute_from_part, dtype=float)
    rotated_mesh = (rotation @ mesh_vertices_centered.T).T
    mesh_floor_indices = np.flatnonzero(
        rotated_mesh[:, 2]
        <= float(np.min(rotated_mesh[:, 2])) + contact_tolerance_mm
    )
    mesh_wall_indices = np.flatnonzero(
        rotated_mesh[:, 1]
        <= float(np.min(rotated_mesh[:, 1])) + contact_tolerance_mm
    )
    floor_mesh_key = tuple(int(index) for index in mesh_floor_indices)
    wall_mesh_key = tuple(int(index) for index in mesh_wall_indices)
    floor_details = (
        topology_cache.get(floor_mesh_key) if topology_cache is not None else None
    )
    if floor_details is None:
        floor_details = _contact_topology(
            mesh_floor_indices, mesh_edges, mesh_faces
        )
        if topology_cache is not None:
            topology_cache[floor_mesh_key] = floor_details
    wall_details = (
        topology_cache.get(wall_mesh_key) if topology_cache is not None else None
    )
    if wall_details is None:
        wall_details = _contact_topology(mesh_wall_indices, mesh_edges, mesh_faces)
        if topology_cache is not None:
            topology_cache[wall_mesh_key] = wall_details
    floor_topology, floor_mesh_edges = floor_details
    wall_topology, wall_mesh_edges = wall_details
    if force_dimension_topology:
        floor_topology = _dimension_name(candidate.floor_contact_dimension)
        wall_topology = _dimension_name(candidate.wall_contact_dimension)
    floor_hull_key = candidate.floor_contact_vertex_indices
    wall_hull_key = candidate.wall_contact_vertex_indices
    floor_face_ids = (
        face_contact_cache.get(floor_hull_key)
        if face_contact_cache is not None
        else None
    )
    if floor_face_ids is None:
        floor_face_ids = _face_ids_in_contact(
            np.asarray(floor_hull_key, dtype=np.int64), support_faces
        )
        if face_contact_cache is not None:
            face_contact_cache[floor_hull_key] = floor_face_ids
    wall_face_ids = (
        face_contact_cache.get(wall_hull_key)
        if face_contact_cache is not None
        else None
    )
    if wall_face_ids is None:
        wall_face_ids = _face_ids_in_contact(
            np.asarray(wall_hull_key, dtype=np.int64), support_faces
        )
        if face_contact_cache is not None:
            face_contact_cache[wall_hull_key] = wall_face_ids
    return replace(
        candidate,
        floor_mesh_contact_vertex_indices=floor_mesh_key,
        wall_mesh_contact_vertex_indices=wall_mesh_key,
        floor_mesh_contact_edges=floor_mesh_edges,
        wall_mesh_contact_edges=wall_mesh_edges,
        floor_contact_topology=floor_topology,
        wall_contact_topology=wall_topology,
        floor_face_ids=floor_face_ids,
        wall_face_ids=wall_face_ids,
    )


def _rotation_distance(a: ContactPose, b: ContactPose) -> float:
    dot = abs(float(np.dot(a.quaternion_xyzw, b.quaternion_xyzw)))
    return 2.0 * math.acos(float(np.clip(dot, -1.0, 1.0)))


QuaternionBucket = tuple[int, int, int, int]
CandidateBuckets = dict[QuaternionBucket, list[int]]
_QUATERNION_NEIGHBOR_OFFSETS = tuple(product((-1, 0, 1), repeat=4))
ContactTopology = tuple[str, tuple[tuple[int, int], ...]]
ContactTopologyCache = dict[tuple[int, ...], ContactTopology]
FaceContactCache = dict[tuple[int, ...], tuple[int, ...]]


def _quaternion_bucket(
    quaternion: NDArray[np.float64], bucket_width: float
) -> QuaternionBucket:
    return tuple(  # type: ignore[return-value]
        int(value) for value in np.floor(quaternion / bucket_width)
    )


def _nearby_candidate_indices(
    quaternion: NDArray[np.float64],
    bucket_width: float,
    buckets: CandidateBuckets,
) -> tuple[int, ...]:
    """Return possible quaternion matches, including the antipodal form."""

    result: set[int] = set()
    for variant in (quaternion, -quaternion):
        center = _quaternion_bucket(variant, bucket_width)
        for offset in _QUATERNION_NEIGHBOR_OFFSETS:
            key = tuple(
                center[axis] + int(offset[axis]) for axis in range(4)
            )
            result.update(buckets.get(key, ()))  # type: ignore[arg-type]
    return tuple(sorted(result))


def _add_candidate(
    candidates: list[ContactPose],
    candidate: ContactPose | None,
    tolerance_rad: float,
    buckets: CandidateBuckets | None = None,
) -> None:
    if candidate is None:
        return
    bucket_width = max(
        2.0 * math.sin(max(tolerance_rad, np.finfo(float).eps) / 4.0),
        np.finfo(float).eps,
    )
    quaternion = np.asarray(candidate.quaternion_xyzw, dtype=float)
    known_indices = (
        range(len(candidates))
        if buckets is None
        else _nearby_candidate_indices(quaternion, bucket_width, buckets)
    )
    for index in known_indices:
        known = candidates[index]
        if _rotation_distance(candidate, known) <= tolerance_rad:
            candidates[index] = replace(
                known,
                provenance=tuple(sorted(set(known.provenance + candidate.provenance))),
                floor_face_ids=tuple(
                    sorted(set(known.floor_face_ids + candidate.floor_face_ids))
                ),
                wall_face_ids=tuple(
                    sorted(set(known.wall_face_ids + candidate.wall_face_ids))
                ),
            )
            return
    candidates.append(candidate)
    if buckets is not None:
        key = _quaternion_bucket(quaternion, bucket_width)
        buckets.setdefault(key, []).append(len(candidates) - 1)


def _continuous_axisymmetric_candidates(
    end_faces: tuple[SupportFace, ...],
    symmetry_axis_part: Vector3,
    vertices_centered: NDArray[np.float64],
    mesh_vertices_centered: NDArray[np.float64],
    mesh_edges: NDArray[np.int64],
    mesh_faces: NDArray[np.int64],
    support_faces: tuple[SupportFace, ...],
    contact_tolerance_mm: float,
) -> list[ContactPose]:
    """Construct physical floor-wall poses of a body of revolution.

    In addition to the isolated end-face poses, discrete lateral-lateral
    support combinations are physical states.  Their contact looks like
    edge-edge contact in a faceted mesh, but the remaining spin is only
    rotation about the body's continuous symmetry axis and therefore does not
    change pose.
    """

    candidates: list[ContactPose] = []
    for face in end_faces:
        normal = np.asarray(face.normal_part, dtype=float)
        floor_alignment = _rotation_from_to(normal, np.array([0.0, 0.0, -1.0]))
        floor_aligned = (floor_alignment @ vertices_centered.T).T
        floor_candidate: ContactPose | None = None
        for edge_start, edge_end in _silhouette_edges(
            floor_aligned, (0, 1), contact_tolerance_mm
        ):
            edge = edge_end - edge_start
            theta = -math.atan2(float(edge[1]), float(edge[0]))
            for candidate_theta in (theta, theta + math.pi):
                floor_candidate = _make_candidate(
                    _rotation_axis(2, candidate_theta) @ floor_alignment,
                    vertices_centered,
                    mesh_vertices_centered,
                    mesh_edges,
                    mesh_faces,
                    support_faces,
                    contact_tolerance_mm,
                    provenance=f"continuous_floor_end_face:{face.face_id}",
                    include_contact_details=False,
                )
                if floor_candidate is not None:
                    break
            if floor_candidate is not None:
                break
        if floor_candidate is not None:
            candidates.append(
                replace(
                    floor_candidate,
                    floor_contact_dimension=2,
                    wall_contact_dimension=1,
                    floor_contact_topology="face",
                    wall_contact_topology="edge",
                )
            )

        wall_alignment = _rotation_from_to(normal, np.array([0.0, -1.0, 0.0]))
        wall_aligned = (wall_alignment @ vertices_centered.T).T
        wall_candidate: ContactPose | None = None
        for edge_start, edge_end in _silhouette_edges(
            wall_aligned, (0, 2), contact_tolerance_mm
        ):
            edge = edge_end - edge_start
            theta = math.atan2(float(edge[1]), float(edge[0]))
            for candidate_theta in (theta, theta + math.pi):
                wall_candidate = _make_candidate(
                    _rotation_axis(1, candidate_theta) @ wall_alignment,
                    vertices_centered,
                    mesh_vertices_centered,
                    mesh_edges,
                    mesh_faces,
                    support_faces,
                    contact_tolerance_mm,
                    provenance=f"continuous_wall_end_face:{face.face_id}",
                    include_contact_details=False,
                )
                if wall_candidate is not None:
                    break
            if wall_candidate is not None:
                break
        if wall_candidate is not None:
            candidates.append(
                replace(
                    wall_candidate,
                    floor_contact_dimension=1,
                    wall_contact_dimension=2,
                    floor_contact_topology="edge",
                    wall_contact_topology="face",
                )
            )

    # Combine every pair of lateral support orbits.  If their normals have
    # axial components a_floor and a_wall, an orientation touching both chute
    # planes must satisfy axis_z=-a_floor and axis_y=-a_wall.  The remaining X
    # component has two signs, which are the two physically distinct downhill
    # directions.  This includes an exactly axial cylinder (a=0), but also the
    # slightly tilted two-rim support that makes a stepped shaft robust.
    axis = np.asarray(symmetry_axis_part, dtype=float)
    axis /= np.linalg.norm(axis)
    axial_merge_tolerance = max(contact_tolerance_mm, 1e-9) / max(
        float(np.ptp(vertices_centered @ axis)), 1e-9
    )
    lateral_orbits: list[tuple[int, float]] = []
    for face in sorted(support_faces, key=lambda value: value.area_mm2, reverse=True):
        axial_component = float(np.dot(face.normal_part, axis))
        if abs(axial_component) >= 1.0 - 1e-6:
            continue
        if any(
            abs(axial_component - known_component) <= axial_merge_tolerance
            for _, known_component in lateral_orbits
        ):
            continue
        lateral_orbits.append((face.face_id, axial_component))

    for floor_face_id, floor_axial in lateral_orbits:
        for wall_face_id, wall_axial in lateral_orbits:
            x_squared = 1.0 - floor_axial**2 - wall_axial**2
            if x_squared < -1e-10:
                continue
            x_magnitude = math.sqrt(max(0.0, x_squared))
            for direction in (1, -1):
                axis_chute = np.array(
                    [direction * x_magnitude, -wall_axial, -floor_axial]
                )
                alignment = _rotation_from_to(axis, axis_chute)
                best_candidate: ContactPose | None = None
                best_score: tuple[float, int] = (-math.inf, -1)
                for spin in np.linspace(0.0, 2.0 * math.pi, 360, endpoint=False):
                    spin_about_axis = Rotation.from_rotvec(
                        float(spin) * axis_chute
                    ).as_matrix()
                    candidate = _make_candidate(
                        spin_about_axis @ alignment,
                        vertices_centered,
                        mesh_vertices_centered,
                        mesh_edges,
                        mesh_faces,
                        support_faces,
                        contact_tolerance_mm,
                        provenance=(
                            "continuous_lateral:"
                            f"floor_orbit_{floor_face_id}:"
                            f"wall_orbit_{wall_face_id}:"
                            f"{'+' if direction > 0 else '-'}axis_downhill"
                        ),
                        allow_edge_edge=True,
                        include_contact_details=False,
                    )
                    if candidate is None:
                        continue
                    floor_points = vertices_centered[
                        np.asarray(candidate.floor_contact_vertex_indices, dtype=int)
                    ]
                    wall_points = vertices_centered[
                        np.asarray(candidate.wall_contact_vertex_indices, dtype=int)
                    ]
                    floor_span = float(np.ptp(floor_points @ axis))
                    wall_span = float(np.ptp(wall_points @ axis))
                    score = (
                        min(floor_span, wall_span),
                        len(candidate.floor_contact_vertex_indices)
                        + len(candidate.wall_contact_vertex_indices),
                    )
                    if score > best_score:
                        best_candidate = candidate
                        best_score = score
                if best_candidate is not None:
                    candidates.append(
                        replace(
                            best_candidate,
                            floor_contact_dimension=1,
                            wall_contact_dimension=1,
                            floor_contact_topology="edge",
                            wall_contact_topology="edge",
                        )
                    )
    return candidates


def build_pose_catalog(
    mesh_path: str | Path,
    *,
    units: str = "mm",
    angular_tolerance_deg: float = 0.1,
    relative_distance_tolerance: float = 1e-6,
    rotation_tolerance_rad: float = 1e-6,
) -> PoseCatalog:
    """Enumerate all isolated theoretical face-edge floor-wall poses.

    The catalog is purely geometric and therefore independent of alpha/beta.
    Angle-dependent perturbation stability is applied in the next pipeline
    step.
    """

    mesh = load_solid_mesh(mesh_path, units=units)
    hull = mesh.convex_hull
    vertices = np.asarray(hull.vertices, dtype=float).copy()
    center_mass = np.asarray(mesh.center_mass, dtype=float).copy()
    vertices_centered = vertices - center_mass
    mesh_vertices_centered = np.asarray(mesh.vertices, dtype=float).copy() - center_mass
    mesh_edges = np.asarray(mesh.edges_unique, dtype=int).copy()
    mesh_faces = np.asarray(mesh.faces, dtype=int).copy()
    length_scale = float(np.max(hull.extents))
    distance_tolerance = max(length_scale * relative_distance_tolerance, 1e-9)

    support_faces = _extract_support_faces(
        hull,
        angular_tolerance_deg=angular_tolerance_deg,
        distance_tolerance_mm=distance_tolerance,
    )
    continuous_symmetry = detect_continuous_revolution_axis(mesh)
    if continuous_symmetry is not None:
        support_faces = _reduce_continuous_face_orbits(
            support_faces,
            continuous_symmetry.axis_part,
            center_mass,
            angular_tolerance_deg=angular_tolerance_deg,
            distance_tolerance_mm=max(
                distance_tolerance, continuous_symmetry.tolerance_mm
            ),
        )
    candidates: list[ContactPose] = []
    candidate_buckets: CandidateBuckets = {}

    if continuous_symmetry is not None:
        axis = np.asarray(continuous_symmetry.axis_part, dtype=float)
        largest_area = max(face.area_mm2 for face in support_faces)
        end_faces = tuple(
            face
            for face in support_faces
            if abs(float(np.dot(face.normal_part, axis)))
            >= math.cos(math.radians(angular_tolerance_deg))
            and face.area_mm2 >= 0.25 * largest_area
        )
        candidates = _continuous_axisymmetric_candidates(
            end_faces,
            axis,
            vertices_centered,
            mesh_vertices_centered,
            mesh_edges,
            mesh_faces,
            support_faces,
            max(distance_tolerance, continuous_symmetry.tolerance_mm),
        )

    for face in () if continuous_symmetry is not None else support_faces:
        normal = np.asarray(face.normal_part, dtype=float)

        # Anchor this face on the floor, then rotate around floor normal Z
        # until every projected silhouette edge has been tested at the wall.
        floor_alignment = _rotation_from_to(normal, np.array([0.0, 0.0, -1.0]))
        floor_aligned = (floor_alignment @ vertices_centered.T).T
        for edge_start, edge_end in _silhouette_edges(
            floor_aligned, (0, 1), distance_tolerance
        ):
            edge = edge_end - edge_start
            theta = -math.atan2(float(edge[1]), float(edge[0]))
            for candidate_theta in (theta, theta + math.pi):
                rotation = _rotation_axis(2, candidate_theta) @ floor_alignment
                candidate = _make_candidate(
                    rotation,
                    vertices_centered,
                    mesh_vertices_centered,
                    mesh_edges,
                    mesh_faces,
                    support_faces,
                    distance_tolerance,
                    provenance=f"floor_face:{face.face_id}",
                    include_contact_details=False,
                )
                _add_candidate(
                    candidates,
                    candidate,
                    rotation_tolerance_rad,
                    candidate_buckets,
                )

        # Mirror case: anchor the face on the wall, then rotate around wall
        # normal Y until a projected silhouette edge supports the floor.
        wall_alignment = _rotation_from_to(normal, np.array([0.0, -1.0, 0.0]))
        wall_aligned = (wall_alignment @ vertices_centered.T).T
        for edge_start, edge_end in _silhouette_edges(
            wall_aligned, (0, 2), distance_tolerance
        ):
            edge = edge_end - edge_start
            theta = math.atan2(float(edge[1]), float(edge[0]))
            for candidate_theta in (theta, theta + math.pi):
                rotation = _rotation_axis(1, candidate_theta) @ wall_alignment
                candidate = _make_candidate(
                    rotation,
                    vertices_centered,
                    mesh_vertices_centered,
                    mesh_edges,
                    mesh_faces,
                    support_faces,
                    distance_tolerance,
                    provenance=f"wall_face:{face.face_id}",
                    include_contact_details=False,
                )
                _add_candidate(
                    candidates,
                    candidate,
                    rotation_tolerance_rad,
                    candidate_buckets,
                )

    candidates.sort(
        key=lambda pose: tuple(round(value, 12) for value in pose.quaternion_xyzw)
    )
    topology_cache: ContactTopologyCache = {}
    face_contact_cache: FaceContactCache = {}
    candidates = [
        _with_contact_details(
            candidate,
            mesh_vertices_centered,
            mesh_edges,
            mesh_faces,
            support_faces,
            (
                distance_tolerance
                if continuous_symmetry is None
                else max(distance_tolerance, continuous_symmetry.tolerance_mm)
            ),
            force_dimension_topology=continuous_symmetry is not None,
            topology_cache=topology_cache,
            face_contact_cache=face_contact_cache,
        )
        for candidate in candidates
    ]
    candidates = [
        replace(candidate, pose_id=index)
        for index, candidate in enumerate(candidates)
    ]

    effective_contact_tolerance = (
        distance_tolerance
        if continuous_symmetry is None
        else max(distance_tolerance, continuous_symmetry.tolerance_mm)
    )
    return PoseCatalog(
        source=str(Path(mesh_path).expanduser().resolve()),
        units=units,
        center_mass_part_mm=tuple(float(value) for value in center_mass),
        support_faces=support_faces,
        poses=tuple(candidates),
        contact_tolerance_mm=effective_contact_tolerance,
        rotation_tolerance_rad=rotation_tolerance_rad,
        continuous_symmetry_axis_part=(
            None
            if continuous_symmetry is None
            else continuous_symmetry.axis_part
        ),
        continuous_symmetry_edge_edge_exception=continuous_symmetry is not None,
    )
