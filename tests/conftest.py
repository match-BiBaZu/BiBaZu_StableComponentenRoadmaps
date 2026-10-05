import json
import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
import trimesh
from scipy.spatial.transform import Rotation

from bibazu_stable_roadmaps.inputs import sha256


@pytest.fixture
def source_folder(tmp_path):
    folder = tmp_path / "inputs" / "Test1"
    folder.mkdir(parents=True)
    mesh = folder / "Test1.stl"
    trimesh.creation.box(extents=(30, 40, 50)).export(mesh)
    rows = [
        {"id": "Test1_0007", "count": 27, "frequency_percent": 27., "quaternion_xyzw": [0., 0., 0., 1.]},
        {"id": "Test1_0009", "count": 20, "frequency_percent": 20., "quaternion_xyzw": Rotation.from_euler("y", 90, degrees=True).as_quat().tolist()},
        {"id": "Test1_0003", "count": 5, "frequency_percent": 5., "quaternion_xyzw": Rotation.from_euler("x", 90, degrees=True).as_quat().tolist()},
        {"id": "Test1_0010", "count": 4, "frequency_percent": 4., "quaternion_xyzw": Rotation.from_euler("z", 90, degrees=True).as_quat().tolist()},
    ]
    data = {"schema_version": 1, "workpiece": "Test1", "completed_trials": 100,
            "geometry": {"stl": mesh.name, "stl_sha256": sha256(mesh)}, "poses": rows,
            "recognition": {"quaternion_order": "xyzw", "rotation": "part_to_chute",
                            "symmetry_quaternions_xyzw": [[0, 0, 0, 1]], "symmetry_symbol": "C1"}}
    (folder / "poses.json").write_text(json.dumps(data), encoding="utf-8")
    (folder / "pose_registry.json").write_text(json.dumps({"schema_version": 1, "mesh_sha256": sha256(mesh),
        "entries": [{"id": row["id"], "anchor_quaternion_xyzw": row["quaternion_xyzw"]} for row in rows]}), encoding="utf-8")
    (folder / "config.json").write_text(json.dumps({"alpha_deg": 45, "beta_deg": 0}))
    return folder
