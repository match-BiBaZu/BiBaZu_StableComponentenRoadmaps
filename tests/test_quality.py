import json
import pytest
from bibazu_stable_roadmaps.inputs import load_source, sha256
from bibazu_stable_roadmaps.published_quality import analyze_pose_quality

def test_legacy_inputs_are_unassessed_without_geometry_execution(source_folder):
    source=load_source(source_folder/"poses.json")
    report=analyze_pose_quality(source)
    assert report["published"] is False
    assert all(p["stability"]=="unknown" for p in report["poses"].values())
    assert report["label_counts"]["unknown"]==4

def test_stale_published_report_is_rejected(source_folder):
    report=analyze_pose_quality(load_source(source_folder/"poses.json"))
    report["producer"]="dashas_drop_sim"
    report["source_sha256"]="stale"
    (source_folder/"pose_quality.json").write_text(json.dumps(report))
    with pytest.raises(ValueError,match="stale"):
        analyze_pose_quality(load_source(source_folder/"poses.json"))
