import time
import json

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from bibazu_stable_roadmaps.gui import ObservedRoadmapGUI
from bibazu_stable_roadmaps.inputs import sha256


def test_condition_defaults_and_saved_catalogue_root_migrate(tmp_path, monkeypatch):
    import bibazu_stable_roadmaps.gui as gui
    app = QApplication.instance() or QApplication([])
    monkeypatch.setattr(gui, "ROOT", tmp_path)
    (tmp_path / "pose_catalogues" / "moving").mkdir(parents=True)
    settings = QSettings(str(tmp_path / "condition.ini"), QSettings.Format.IniFormat)
    window = ObservedRoadmapGUI(settings=settings)
    assert window.source_path.text() == str(tmp_path / "pose_catalogues" / "moving")
    assert window.output_root.text() == str(tmp_path / "moving")
    (tmp_path / "pose_catalogues" / "stationary").mkdir()
    window.source_path.setText(str(tmp_path / "pose_catalogues" / "stationary"))
    window.scan()
    assert window.output_root.text() == str(tmp_path / "stationary")
    window.output_root.setText(str(tmp_path / "custom_output"))
    window.source_path.setText(str(tmp_path / "pose_catalogues" / "moving"))
    window.scan()
    assert window.output_root.text() == str(tmp_path / "custom_output")
    window.close()
    settings.setValue("source", str(tmp_path / "pose_catalogues"))
    settings.setValue("config", json.dumps({"output_root": str(tmp_path)}))
    window = ObservedRoadmapGUI(settings=settings)
    assert window.source_path.text() == str(tmp_path / "pose_catalogues" / "moving")
    assert window.output_root.text() == str(tmp_path / "moving")
    window.close()


def wait_for_worker(window, timeout=45):
    deadline = time.monotonic() + timeout
    while window.process is not None and time.monotonic() < deadline:
        QTest.qWait(25)
    assert window.process is None, window.log.toPlainText()


def test_preview_defaults_and_persisted_settings(source_folder, tmp_path):
    app = QApplication.instance() or QApplication([])
    settings = QSettings(str(tmp_path / "settings.ini"), QSettings.Format.IniFormat)
    window = ObservedRoadmapGUI(settings=settings)
    window.source_path.setText(str(source_folder))
    window.scan()
    assert window.minimum_frequency.value() == 5
    assert window.renumber.isChecked()
    assert len(window.sources) == 1
    assert window.component_table.item(0, 2).text() == "3 / 4"
    assert window.preview_table.item(0, 3).text() == "0"
    assert window.preview_table.item(3, 2).text() == "Removed"
    window.minimum_frequency.setValue(0)
    window.renumber.setChecked(False)
    assert window.preview_table.item(0, 3).text() == "7"
    assert window.preview_table.item(3, 2).text() == "Retained"
    window.show()
    app.processEvents()
    assert window.grab().save(str(tmp_path / "gui.png"))
    window.close()
    restored = ObservedRoadmapGUI(settings=settings)
    assert restored.minimum_frequency.value() == 0
    assert not restored.renumber.isChecked()
    assert restored.source_path.text() == str(source_folder)
    restored.close()


def test_gui_worker_completes_and_cancels_safely(source_folder, tmp_path):
    app = QApplication.instance() or QApplication([])
    window = ObservedRoadmapGUI(settings=QSettings(str(tmp_path / "settings.ini"), QSettings.Format.IniFormat))
    window.source_path.setText(str(source_folder / "pose_registry.json"))
    window.output_root.setText(str(tmp_path / "outputs"))
    window.scan()
    for key, check in window.outputs.items():
        check.setChecked(key == "yaml")
    window.start()
    wait_for_worker(window)
    assert window.component_table.item(0, 3).text() == "completed", window.log.toPlainText()
    assert window.generate_button.isEnabled()
    old = (tmp_path / "outputs/Test1/Test1_roadmap.yaml").read_bytes()
    window.start()
    window.cancel()
    wait_for_worker(window)
    assert "Cancelled" in window.log.toPlainText()
    assert (tmp_path / "outputs/Test1/Test1_roadmap.yaml").read_bytes() == old
    assert window.generate_button.isEnabled()
    assert not (tmp_path / "outputs/.roadmaps.lock").exists()
    window.close()


def quality_report(source_folder):
    source = json.loads((source_folder / "poses.json").read_text())
    rows = source["poses"]
    entries = {}
    labels = (("fragile", .02), ("marginal", .2), ("resistant", 1.2), ("unknown", None))
    for index, (row, (label, lift)) in enumerate(zip(rows, labels)):
        entries[row["id"]] = {"label": label, "escape_lift_mm": lift,
                              "escape_target_source_id": rows[(index + 1) % len(rows)]["id"] if lift is not None else None,
                              "escape_within_group": index == 0, "reason": "No distinct target" if lift is None else ""}
    return {"schema_version": 1, "method": "sampled_seated_escape_lift", "method_version": 1,
            "thresholds_mm": {"fragile": .1, "resistant": .5},
            "source_sha256": sha256(source_folder / "poses.json"),
            "observations_sha256": sha256(source_folder / "poses.json"),
            "mesh_sha256": sha256(source_folder / "Test1.stl"),
            "config_sha256": sha256(source_folder / "config.json"), "poses": entries}


def test_saved_quality_is_separate_from_frequency_and_rejects_stale_config(source_folder, tmp_path):
    app = QApplication.instance() or QApplication([])
    output = tmp_path / "exports"
    (output / "Test1").mkdir(parents=True)
    (output / "Test1/pose_quality.json").write_text(json.dumps(quality_report(source_folder)), encoding="utf-8")
    window = ObservedRoadmapGUI(settings=QSettings(str(tmp_path / "quality.ini"), QSettings.Format.IniFormat))
    window.source_path.setText(str(source_folder))
    window.output_root.setText(str(output))
    window.scan()
    assert window.preview_table.item(0, 4).text() == "Fragile"
    assert window.preview_table.item(0, 5).text() == "0.020"
    assert "(rocking)" in window.preview_table.item(0, 6).text()
    assert "Rocking" in window.preview_table.item(0, 6).toolTip()
    assert window.preview_table.item(2, 4).text() == "Resistant"
    window.minimum_frequency.setValue(25)
    assert window.preview_table.item(2, 2).text() == "Removed"
    assert window.preview_table.item(2, 4).text() == "Resistant"
    (source_folder / "config.json").write_text(json.dumps({"alpha_deg": 10, "beta_deg": 0}), encoding="utf-8")
    window.scan()
    assert window.preview_table.item(0, 4).text() == "Not assessed"
    window.close()


def test_registry_quality_rejects_changed_companion_observations(source_folder, tmp_path):
    app = QApplication.instance() or QApplication([])
    output = tmp_path / "registry_exports"
    (output / "Test1").mkdir(parents=True)
    report = quality_report(source_folder)
    report["source_sha256"] = sha256(source_folder / "pose_registry.json")
    (output / "Test1/pose_quality.json").write_text(json.dumps(report), encoding="utf-8")
    window = ObservedRoadmapGUI(settings=QSettings(str(tmp_path / "registry-quality.ini"), QSettings.Format.IniFormat))
    window.source_path.setText(str(source_folder / "pose_registry.json"))
    window.output_root.setText(str(output))
    window.scan()
    assert window.preview_table.item(0, 4).text() == "Fragile"
    observations = json.loads((source_folder / "poses.json").read_text())
    observations["poses"][0]["count"] += 1
    (source_folder / "poses.json").write_text(json.dumps(observations), encoding="utf-8")
    window.scan()
    assert window.preview_table.item(0, 4).text() == "Not assessed"
    window.close()


def test_quality_worker_assesses_filtered_poses_without_writing_exports(source_folder, tmp_path):
    app = QApplication.instance() or QApplication([])
    before = (source_folder / "poses.json").read_bytes()
    output = tmp_path / "untouched_exports"
    window = ObservedRoadmapGUI(settings=QSettings(str(tmp_path / "assess.ini"), QSettings.Format.IniFormat))
    window.source_path.setText(str(source_folder))
    window.output_root.setText(str(output))
    window.scan()
    window.minimum_frequency.setValue(95)
    assert all(window.preview_table.item(row, 2).text() == "Removed" for row in range(4))
    window.assess_quality()
    assert window.process is not None
    assert not window.generate_button.isEnabled()
    assert not window.assess_button.isEnabled()
    wait_for_worker(window)
    assert window.component_table.item(0, 3).text() == "quality assessed", window.log.toPlainText()
    assert all(window.preview_table.item(row, 4).text() != "Not assessed" for row in range(4))
    assert all(window.preview_table.item(row, 2).text() == "Removed" for row in range(4))
    assert (source_folder / "poses.json").read_bytes() == before
    assert not output.exists()
    assert window.quality_report_file is None
    assert window.assess_button.isEnabled()
    previous = [window.preview_table.item(row, 4).text() for row in range(4)]
    window.assess_quality()
    window.cancel()
    wait_for_worker(window)
    assert "Cancelled" in window.log.toPlainText()
    assert [window.preview_table.item(row, 4).text() for row in range(4)] == previous
    window.close()
