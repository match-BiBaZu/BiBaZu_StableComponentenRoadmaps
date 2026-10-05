"""Focused Windows/PyQt GUI for simulator pose files and observed frequencies."""
from __future__ import annotations

from dataclasses import asdict
import json
import os
from pathlib import Path
import sys
import tempfile
from uuid import uuid4

from PyQt6.QtCore import QProcess, QProcessEnvironment, QSettings, Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QIcon, QFontDatabase, QFont
from PyQt6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFileDialog, QGridLayout,
                             QGroupBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow,
                             QMessageBox, QPlainTextEdit, QProgressBar, QPushButton, QSplitter,
                             QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from .generate import ROOT, OUTPUTS, GenerationConfig
from .inputs import EmptyPoseList, discover_sources, load_source, select_poses


class ObservedRoadmapGUI(QMainWindow):
    def __init__(self, *, settings=None):
        super().__init__()
        if sys.platform == "win32" and not QFontDatabase.families():
            font_path = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts/segoeui.ttf"
            font_id = QFontDatabase.addApplicationFont(str(font_path))
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                QApplication.instance().setFont(QFont(families[0], 9))
        self.setWindowTitle("BiBaZu Observed Pose Roadmaps")
        self.setWindowIcon(QIcon(str(ROOT / "WindowsLaunchers/icons/stable-roadmaps.ico")))
        self.resize(1160, 790)
        self.settings = settings if settings is not None else QSettings(
            QSettings.Format.IniFormat, QSettings.Scope.UserScope, "BiBaZu", "StableComponentRoadmaps")
        self.sources = []
        self.source_data = {}
        self.source_errors = {}
        self.process = None
        self.pending = b""
        self.cancel_file = None
        self.cancel_requested = False
        self.active_sources = []
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.controls = QWidget()
        body = QVBoxLayout(self.controls)
        body.setContentsMargins(0, 0, 0, 0)
        self.source_path = QLineEdit(str(ROOT.parent / "BiBaZu_StableComponentenPoses"))
        self.source_path.setPlaceholderText("poses.json, pose_registry.json, or a poses repository folder")
        row = QHBoxLayout()
        row.addWidget(QLabel("Pose input"))
        row.addWidget(self.source_path, 1)
        for label, action in (("JSON file…", self.browse_file), ("Folder…", self.browse_source_folder), ("Refresh", self.scan)):
            button = QPushButton(label)
            button.clicked.connect(action)
            row.addWidget(button)
        body.addLayout(row)
        self.output_root = QLineEdit(str(ROOT))
        row = QHBoxLayout()
        row.addWidget(QLabel("Output repository"))
        row.addWidget(self.output_root, 1)
        browse = QPushButton("Browse…")
        browse.clicked.connect(self.browse_output)
        row.addWidget(browse)
        body.addLayout(row)
        options = QGroupBox("Observed frequency")
        row = QHBoxLayout(options)
        row.addWidget(QLabel("Minimum frequency"))
        self.minimum_frequency = QDoubleSpinBox()
        self.minimum_frequency.setRange(0, 100)
        self.minimum_frequency.setDecimals(3)
        self.minimum_frequency.setSuffix(" %")
        self.minimum_frequency.setValue(5)
        self.minimum_frequency.setToolTip("Below this value is removed; exactly this value is retained. 0% disables filtering.")
        row.addWidget(self.minimum_frequency)
        self.renumber = QCheckBox("Renumber by frequency (pose 0 = most frequent)")
        self.renumber.setChecked(True)
        row.addWidget(self.renumber)
        row.addStretch()
        body.addWidget(options)
        formats = QGroupBox("Files to generate")
        grid = QGridLayout(formats)
        self.outputs = {}
        for index, (key, label) in enumerate(OUTPUTS.items()):
            check = QCheckBox(label)
            check.setChecked(key in GenerationConfig().outputs)
            self.outputs[key] = check
            grid.addWidget(check, index // 4, index % 4)
        body.addWidget(formats)
        note = QLabel("The observed poses determine the nodes. Geometry calculates direct connections and draws the poses. "
                      "Each component has one current result set; regeneration replaces its generated files.")
        note.setWordWrap(True)
        body.addWidget(note)
        splitter = QSplitter()
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        row = QHBoxLayout()
        row.addWidget(QLabel("Components"))
        for label, selected in (("Select all", True), ("Select none", False)):
            button = QPushButton(label)
            button.clicked.connect(lambda checked=False, value=selected: self.select_all(value))
            row.addWidget(button)
        left_layout.addLayout(row)
        self.component_table = QTableWidget(0, 4)
        self.component_table.setHorizontalHeaderLabels(["Generate", "Component", "Retained / total", "Status"])
        self.component_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.component_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.component_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.component_table.setMinimumWidth(460)
        left_layout.addWidget(self.component_table)
        splitter.addWidget(left)
        right = QWidget()
        right.setMinimumWidth(480)
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.preview_label = QLabel("Pose preview")
        right_layout.addWidget(self.preview_label)
        self.preview_table = QTableWidget(0, 4)
        self.preview_table.setHorizontalHeaderLabels(["Original pose ID", "Frequency", "Selection", "Roadmap ID"])
        self.preview_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        right_layout.addWidget(self.preview_table)
        splitter.addWidget(right)
        splitter.setSizes([480, 620])
        body.addWidget(splitter, 1)
        layout.addWidget(self.controls, 1)
        row = QHBoxLayout()
        self.generate_button = QPushButton("Generate selected components")
        self.generate_button.clicked.connect(self.start)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel)
        open_button = QPushButton("Open output folder")
        open_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(self.output_root.text())))
        for button in (self.generate_button, self.cancel_button, open_button):
            row.addWidget(button)
        layout.addLayout(row)
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(150)
        layout.addWidget(self.log)
        self.source_path.editingFinished.connect(self.scan)
        self.minimum_frequency.valueChanged.connect(self.refresh_preview)
        self.renumber.toggled.connect(self.refresh_preview)
        self.component_table.currentCellChanged.connect(lambda *args: self.refresh_preview())
        self.restore()
        self.scan()

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose simulator pose JSON", self.source_path.text(), "JSON files (*.json)")
        if path:
            self.source_path.setText(path)
            self.scan()

    def browse_source_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Choose poses repository", self.source_path.text())
        if path:
            self.source_path.setText(path)
            self.scan()

    def browse_output(self):
        path = QFileDialog.getExistingDirectory(self, "Choose output repository", self.output_root.text())
        if path:
            self.output_root.setText(path)

    @staticmethod
    def item(text):
        item = QTableWidgetItem(str(text))
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        return item

    def scan(self):
        old = {str(path): self.component_table.item(row, 0).checkState() == Qt.CheckState.Checked
               for row, path in enumerate(self.sources)}
        try:
            self.sources = discover_sources(self.source_path.text())
        except (ValueError, OSError) as error:
            self.sources = []
            self.log.appendPlainText(str(error))
        self.source_data, self.source_errors = {}, {}
        self.component_table.setRowCount(len(self.sources))
        names = {}
        for row, path in enumerate(self.sources):
            try:
                data = load_source(path)
                self.source_data[path] = data
                name = data.workpiece
                if name.casefold() in names:
                    self.source_errors[path] = "Duplicate component input"
                    self.source_errors[names[name.casefold()]] = "Duplicate component input"
                names[name.casefold()] = path
            except (ValueError, OSError, TypeError) as error:
                name = path.parent.name
                self.source_errors[path] = str(error)
            check = QTableWidgetItem()
            check.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
            check.setCheckState(Qt.CheckState.Checked if old.get(str(path), True) else Qt.CheckState.Unchecked)
            self.component_table.setItem(row, 0, check)
            item = self.item(name)
            item.setToolTip(str(path))
            self.component_table.setItem(row, 1, item)
            self.component_table.setItem(row, 2, self.item(""))
            self.component_table.setItem(row, 3, self.item(self.source_errors.get(path, "Ready")))
        if self.sources:
            self.component_table.setCurrentCell(0, 1)
        self.refresh_preview()

    def select_all(self, selected):
        for row in range(self.component_table.rowCount()):
            self.component_table.item(row, 0).setCheckState(Qt.CheckState.Checked if selected else Qt.CheckState.Unchecked)

    def refresh_preview(self):
        # Signals can fire while scan is still populating rows.
        if not hasattr(self, "preview_table"):
            return
        selections = {}
        for row, path in enumerate(self.sources):
            data = self.source_data.get(path)
            if not data or self.component_table.item(row, 2) is None:
                continue
            try:
                numbered, removed = select_poses(data, self.minimum_frequency.value(), self.renumber.isChecked())
                selections[path] = dict((pose.source_id, number) for pose, number in numbered)
                self.component_table.item(row, 2).setText(f"{len(numbered)} / {len(data.poses)}")
                if self.process is None:
                    self.component_table.item(row, 3).setText(self.source_errors.get(path, "Ready" if numbered else "No poses pass cutoff"))
            except ValueError as error:
                self.component_table.item(row, 3).setText(str(error))
        row = self.component_table.currentRow()
        path = self.sources[row] if 0 <= row < len(self.sources) else None
        data = self.source_data.get(path)
        self.preview_table.setRowCount(len(data.poses) if data else 0)
        self.preview_label.setText(f"Pose preview — {data.workpiece}" if data else "Pose preview")
        if not data:
            return
        mapping = selections.get(path, {})
        for row, pose in enumerate(data.poses):
            retained = pose.source_id in mapping
            texts = (pose.source_id, f"{pose.frequency_percent:g}%", "Retained" if retained else "Removed", mapping.get(pose.source_id, "—"))
            for column, text in enumerate(texts):
                self.preview_table.setItem(row, column, self.item(text))

    def config(self):
        return GenerationConfig(output_root=self.output_root.text(), minimum_frequency_percent=self.minimum_frequency.value(),
                                renumber_by_frequency=self.renumber.isChecked(),
                                outputs=tuple(key for key, check in self.outputs.items() if check.isChecked()))

    def persist(self):
        self.settings.setValue("source", self.source_path.text())
        self.settings.setValue("config", json.dumps(asdict(self.config())))
        self.settings.sync()

    def restore(self):
        try:
            self.source_path.setText(self.settings.value("source", self.source_path.text()))
            data = json.loads(self.settings.value("config", "{}"))
            self.output_root.setText(data.get("output_root", self.output_root.text()))
            self.minimum_frequency.setValue(data.get("minimum_frequency_percent", 5))
            self.renumber.setChecked(data.get("renumber_by_frequency", True))
            if "outputs" in data:
                for key, check in self.outputs.items():
                    check.setChecked(key in data["outputs"])
        except (ValueError, TypeError):
            self.log.appendPlainText("Saved settings could not be read; using defaults.")

    def start(self):
        if self.process is not None:
            return
        try:
            config = self.config()
            config.validate()
            selected = [path for row, path in enumerate(self.sources) if self.component_table.item(row, 0).checkState() == Qt.CheckState.Checked]
            if not selected:
                raise ValueError("Select at least one component.")
            for path in selected:
                if path in self.source_errors and path in self.source_data:
                    raise ValueError(f"{path.parent.name}: {self.source_errors[path]}")
                try:
                    data = load_source(path)
                    select_poses(data, config.minimum_frequency_percent, config.renumber_by_frequency)
                except EmptyPoseList:
                    continue
        except (ValueError, OSError, TypeError) as error:
            QMessageBox.warning(self, "Check inputs", str(error))
            return
        self.persist()
        self.active_sources = selected
        self.cancel_requested = False
        self.cancel_file = Path(tempfile.gettempdir()) / ("bibazu-roadmap-cancel-" + uuid4().hex)
        self.pending = b""
        for row, path in enumerate(self.sources):
            if path in selected:
                self.component_table.item(row, 3).setText("queued")
        self.controls.setEnabled(False)
        self.generate_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress.setRange(0, len(selected))
        self.progress.setValue(0)
        process = QProcess(self)
        self.process = process
        process.setWorkingDirectory(str(ROOT))
        environment = QProcessEnvironment.systemEnvironment()
        environment.insert("PYTHONPATH", str(ROOT / "src"))
        process.setProcessEnvironment(environment)
        process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        process.readyReadStandardOutput.connect(self.read_output)
        process.finished.connect(self.finished)
        process.errorOccurred.connect(self.process_error)
        request = json.dumps({"sources": [str(path) for path in selected], "settings": asdict(config), "cancel_file": str(self.cancel_file)}).encode("utf-8")
        process.started.connect(lambda: (process.write(request), process.closeWriteChannel()))
        python = str(Path(sys.executable).with_name("python.exe")) if sys.platform == "win32" else sys.executable
        process.start(python, ["-X", "utf8", "-u", "-m", "bibazu_stable_roadmaps.generate"])

    def handle_line(self, line):
        text = line.decode("utf-8", errors="replace").strip()
        if not text:
            return
        try:
            event = json.loads(text)
        except ValueError:
            self.log.appendPlainText(text)
            return
        self.log.appendPlainText(f"{event.get('part', '')} {event.get('status', '')}: {event.get('message', event.get('reason', event.get('folder', '')))}")
        if event.get("detail"):
            self.log.appendPlainText(event["detail"])
        for row, path in enumerate(self.sources):
            if str(path) == event.get("source") and event.get("status"):
                self.component_table.item(row, 3).setText(event["status"])
        if "index" in event:
            self.progress.setValue(event["index"])

    def read_output(self):
        if self.process is None:
            return
        self.pending += bytes(self.process.readAllStandardOutput())
        while b"\n" in self.pending:
            line, self.pending = self.pending.split(b"\n", 1)
            self.handle_line(line)

    def finished(self, exit_code, *args):
        if self.process is None:
            return
        self.read_output()
        if self.pending:
            self.handle_line(self.pending)
            self.pending = b""
        self.process.deleteLater()
        self.process = None
        if self.cancel_file:
            self.cancel_file.unlink(missing_ok=True)
        self.controls.setEnabled(True)
        self.generate_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        for row, path in enumerate(self.sources):
            if path in self.active_sources and self.component_table.item(row, 3).text() in {"running", "queued"}:
                self.component_table.item(row, 3).setText("cancelled" if self.cancel_requested else "failed")
        self.log.appendPlainText("Cancelled; previously completed results are retained." if self.cancel_requested else f"Generation finished (exit code {exit_code}).")

    def process_error(self, error):
        if error == QProcess.ProcessError.FailedToStart:
            self.log.appendPlainText("Could not start worker: " + self.process.errorString())
            self.finished(1)

    def cancel(self):
        if self.process and self.cancel_file:
            self.cancel_requested = True
            self.cancel_file.touch()
            self.cancel_button.setEnabled(False)
            self.log.appendPlainText("Cancellation requested; finishing the current operation safely…")

    def closeEvent(self, event):
        if self.process:
            self.cancel()
            event.ignore()
            return
        self.persist()
        event.accept()


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    window = ObservedRoadmapGUI()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
