from copy import deepcopy

import pytest

from bibazu_stable_roadmaps.import_catalogues import normalize_catalogue


@pytest.mark.parametrize("condition,phase", [("moving", "transport"), ("stationary", "stationary")])
def test_published_pose_identity_and_all_trial_frequency_are_preserved(condition, phase):
    catalogue = {
        "schema_version": 1, "condition": condition, "total_trials": 10000,
        "settled_trials": 9800, "model": "observed-seated-geodesic-basins-v1",
        "settings": {"recognition": {"quaternion_order": "xyzw"}},
        "source": {"mesh_path": "Test/Test.stl", "mesh_sha256": "mesh"},
        "poses": [{"id": "Test_0017", "count": 9800, "incidence_percent": 98.0,
                   "quaternion_xyzw": [0, 0, 0, 1], "group_id": "G2"}],
    }
    before = deepcopy(catalogue)
    result = normalize_catalogue(catalogue, "commit", "path/catalogue.json", "digest")
    assert catalogue == before
    assert result["completed_trials"] == 10000
    assert result["evaluation_phase"] == phase
    assert result["poses"][0] == {**before["poses"][0], "frequency_percent": 98.0}
    assert result["source_provenance"]["pose_revision"] == "commit"
    assert result["source_provenance"]["catalogue_sha256"] == "digest"
    catalogue["poses"][0]["incidence_percent"] = 100
    with pytest.raises(ValueError, match="denominator"):
        normalize_catalogue(catalogue, "commit", "path", "digest")
