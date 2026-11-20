"""Read verified DropSim stability; this application does not assess geometry."""
from collections import Counter
from copy import deepcopy
import math
from .inputs import read_json, sha256

METHOD = "sampled_seated_escape_lift"
METHOD_VERSION = 1
THRESHOLDS_MM = {"fragile": .1, "resistant": .5}
STABILITY = {"resistant": "high", "marginal": "medium", "fragile": "low", "unknown": "unknown"}

def quality_label(lift):
    if lift is None:
        return "unknown"
    if isinstance(lift, bool) or not isinstance(lift, (float, int)) or not math.isfinite(lift) or lift < 0:
        raise ValueError("Invalid published lift estimate.")
    return "fragile" if lift < .1 - 1e-9 else "marginal" if lift < .5 - 1e-9 else "resistant"

def analyze_pose_quality(source, *, mesh=None, progress=lambda message: None, check_cancel=lambda: None):
    """Compatibility adapter: load upstream results, never calculate new scores."""
    check_cancel()
    observations = source.path if "poses" in read_json(source.path) else source.path.with_name("poses.json")
    config = source.path.with_name("config.json")
    hashes = {"source_sha256": sha256(source.path), "observations_sha256": sha256(observations),
              "mesh_sha256": sha256(source.mesh), "config_sha256": sha256(config) if config.is_file() else None}
    path = source.path.with_name("pose_quality.json")
    if path.is_file():
        report = read_json(path)
        upstream = report.get("upstream_provenance")
        if upstream:
            original = source.path.with_name("upstream_pose_quality.json")
            catalogue = source.path.with_name("catalogue.json")
            if (not original.is_file() or not catalogue.is_file()
                    or sha256(original) != upstream.get("report_sha256")
                    or sha256(catalogue) != upstream.get("catalogue_sha256")):
                raise ValueError("Original upstream stability provenance is missing or differs.")
        if report.get("producer") != "dashas_drop_sim" or report.get("method") != METHOD or report.get("method_version") != METHOD_VERSION:
            raise ValueError("Stability report was not published by the supported DropSim classifier.")
        if report.get("thresholds_mm") != THRESHOLDS_MM or any(report.get(k) != v for k, v in hashes.items()):
            raise ValueError("Published stability is stale; refresh the DropSim catalogue.")
        if set(report.get("poses", {})) != {p.source_id for p in source.poses}:
            raise ValueError("Published stability pose identities differ from the selected source.")
        for key, entry in report["poses"].items():
            if quality_label(entry.get("escape_lift_mm")) != entry.get("label"):
                raise ValueError("Published stability label differs from lift estimate.")
            if entry.get("escape_target_source_id") is not None and entry["escape_target_source_id"] not in report["poses"]:
                raise ValueError("Published stability target is absent.")
            entry["stability"] = STABILITY[entry["label"]]
        report["published"] = True
        progress("Loaded published DropSim stability; no geometry recalculated")
        check_cancel()
        return report
    entries = {p.source_id: {"label": "unknown", "stability": "unknown", "escape_lift_mm": None,
        "escape_target_source_id": None, "escape_within_group": None,
        "observed_count": p.count, "observed_frequency_percent": p.frequency_percent,
        "reason": "Not assessed: refresh the upstream DropSim catalogue to obtain stability."} for p in source.poses}
    return {"schema_version": 1, "method": METHOD, "method_version": METHOD_VERSION,
        "producer": "unassessed", "published": False, "thresholds_mm": dict(THRESHOLDS_MM),
        **hashes, "frequency_independent": True, "automatic_filtering": False,
        "label_counts": {k: len(entries) if k == "unknown" else 0 for k in STABILITY},
        "stability_counts": {v: len(entries) if v == "unknown" else 0 for v in STABILITY.values()}, "poses": entries}
