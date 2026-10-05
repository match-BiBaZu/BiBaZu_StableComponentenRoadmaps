import time

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from bibazu_stable_roadmaps.gui import ObservedRoadmapGUI


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
