from __future__ import annotations

import json
import multiprocessing as mp
import queue
from pathlib import Path
from typing import Any

import pyqtgraph as pg
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QAction, QColor, QBrush, QPen
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QScrollArea,
    QSpinBox,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QGraphicsScene,
    QGraphicsView,
)

from .artifacts import (
    config_hash,
    load_run_artifact,
    make_run_artifact,
    write_json,
)
from .parameters import CORE_SCHEMA, ParameterSchema, ParameterSpec
from .protocol import make_command
from .worker import engine_process_main


class ParameterPanel(QWidget):
    values_changed = Signal(dict)

    def __init__(self, schema: ParameterSchema, parent: QWidget | None = None):
        super().__init__(parent)
        self.schema = schema
        self.widgets: dict[str, QWidget] = {}
        self.rows: dict[str, QWidget] = {}
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search parameters...")
        self.search.textChanged.connect(self._filter)
        self.body = QWidget()
        self.body_layout = QVBoxLayout(self.body)
        self._build()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.body)

        layout = QVBoxLayout(self)
        layout.addWidget(self.search)
        layout.addWidget(scroll)

    def _build(self) -> None:
        grouped: dict[str, list[ParameterSpec]] = {
            group: [] for group in self.schema.groups()
        }
        for spec in self.schema.specs:
            grouped[spec.group].append(spec)

        for group, specs in grouped.items():
            box = QGroupBox(group)
            form = QFormLayout(box)
            for spec in specs:
                widget = self._widget_for(spec)
                widget.setToolTip(spec.description)
                row = QWidget()
                row_layout = QHBoxLayout(row)
                row_layout.setContentsMargins(0, 0, 0, 0)
                row_layout.addWidget(widget)
                if spec.description:
                    row_layout.addWidget(QLabel(spec.description))
                form.addRow(spec.label, row)
                self.widgets[spec.path] = widget
                self.rows[spec.path] = row
            self.body_layout.addWidget(box)
        self.body_layout.addStretch()

    def _widget_for(self, spec: ParameterSpec) -> QWidget:
        if spec.kind == "boolean":
            widget = QCheckBox()
            widget.setChecked(bool(spec.default))
            return widget
        if spec.kind == "choice":
            widget = QComboBox()
            widget.addItems(list(spec.choices))
            widget.setCurrentText(str(spec.default))
            return widget
        if spec.kind == "integer":
            widget = QSpinBox()
            widget.setRange(
                int(spec.minimum or -2_147_483_648),
                int(spec.maximum or 2_147_483_647),
            )
            widget.setSingleStep(int(spec.step))
            widget.setValue(int(spec.default))
            return widget
        widget = QDoubleSpinBox()
        widget.setRange(
            float(spec.minimum or -1e12),
            float(spec.maximum or 1e12),
        )
        widget.setSingleStep(float(spec.step))
        widget.setDecimals(6)
        widget.setValue(float(spec.default))
        return widget

    def values(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for spec in self.schema.specs:
            widget = self.widgets[spec.path]
            if isinstance(widget, QCheckBox):
                result[spec.path] = widget.isChecked()
            elif isinstance(widget, QComboBox):
                result[spec.path] = widget.currentText()
            elif isinstance(widget, QSpinBox):
                result[spec.path] = widget.value()
            else:
                result[spec.path] = widget.value()
        return self.schema.validate(result)

    def _filter(self, text: str) -> None:
        query = text.strip().lower()
        for spec in self.schema.specs:
            visible = (
                not query
                or query in spec.path.lower()
                or query in spec.label.lower()
                or query in spec.group.lower()
            )
            self.rows[spec.path].setVisible(visible)


class WorldView(QGraphicsView):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setMinimumSize(480, 360)
        self.setBackgroundBrush(QBrush(QColor("#101820")))

    def render_snapshot(self, snapshot: dict[str, Any]) -> None:
        self.scene.clear()
        width = float(snapshot.get("world_width", 100.0))
        height = float(snapshot.get("world_height", 70.0))
        self.scene.setSceneRect(0, 0, width, height)
        for organism in snapshot.get("organisms", []):
            radius = max(1.0, min(4.0, organism["energy"] / 15.0))
            color = (
                QColor("#63d8ff")
                if organism["age"] % 2 == 0
                else QColor("#f8c15c")
            )
            self.scene.addEllipse(
                organism["x"] - radius,
                organism["y"] - radius,
                radius * 2,
                radius * 2,
                QPen(Qt.PenStyle.NoPen),
                QBrush(color),
            )
        self.fitInView(
            self.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio,
        )


class MetricsPanel(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.status = QLabel("Ready")
        self.engine = QLabel("Engine: —")
        self.measurement = QLabel("Measurement: —")
        self.config = QLabel("Config hash: —")
        self.tick = QLabel("Tick: 0")
        self.population = QLabel("Population: 0")
        self.memory = QLabel("Memory: 0")
        self.instructions = QLabel("Instructions: 0")
        self.faults = QLabel("Faults: 0")
        self.births = QLabel("Births: 0")
        self.deaths = QLabel("Deaths: 0")
        self.genotypes = QLabel("Active genotypes: 0")
        self.historical_genotypes = QLabel("Historical genotypes: 0")
        self.lineages = QLabel("Active lineages: 0")
        self.blocked_divisions = QLabel("Blocked divisions: 0")
        self.waiting_for_memory = QLabel("Waiting for memory: 0")
        self.waiting_for_energy = QLabel("Waiting for energy: 0")
        self.balance = QLabel("Energy balance error: 0")
        self.organism_selector = QComboBox()
        self.organism_selector.setPlaceholderText(
            "Select an organism..."
        )
        self.organism_selector.currentTextChanged.connect(
            self._show_organism
        )
        self.organism_details = QPlainTextEdit()
        self.organism_details.setReadOnly(True)
        self.organism_details.setMaximumHeight(170)
        self._organisms: dict[str, dict[str, Any]] = {}
        self.plot = pg.PlotWidget()
        self.plot.setBackground("#101820")
        self.plot.addLegend()
        self.population_curve = self.plot.plot(
            pen="#63d8ff",
            name="population",
        )
        self.energy_curve = self.plot.plot(
            pen="#f8c15c",
            name="energy pool",
        )
        self.population_data: list[float] = []
        self.energy_data: list[float] = []
        layout = QVBoxLayout(self)
        for widget in (
            self.status,
            self.engine,
            self.measurement,
            self.config,
            self.tick,
            self.population,
            self.memory,
            self.instructions,
            self.faults,
            self.births,
            self.deaths,
            self.genotypes,
            self.historical_genotypes,
            self.lineages,
            self.blocked_divisions,
            self.waiting_for_memory,
            self.waiting_for_energy,
            self.balance,
        ):
            layout.addWidget(widget)
        layout.addWidget(QLabel("Organism inspector"))
        layout.addWidget(self.organism_selector)
        layout.addWidget(self.organism_details)
        layout.addWidget(self.plot)

    def update_metrics(self, metrics: dict[str, Any]) -> None:
        self.engine.setText(
            f"Engine: {metrics.get('engine_version', 'unknown')}"
        )
        self.measurement.setText(
            f"Measurement: {metrics.get('measurement_version', 'unknown')}"
        )
        self.config.setText(
            f"Config hash: {metrics.get('config_hash', 'unknown')}"
        )
        self.tick.setText(f"Tick: {metrics.get('tick', 0)}")
        self.population.setText(
            f"Population: {metrics.get('active_population', 0)}"
        )
        self.memory.setText(f"Memory: {metrics.get('memory_used', 0)}")
        self.instructions.setText(
            f"Instructions: {metrics.get('instructions_executed', 0)}"
        )
        self.faults.setText(f"Faults: {metrics.get('faults', 0)}")
        self.births.setText(f"Births: {metrics.get('births', 0)}")
        self.deaths.setText(f"Deaths: {metrics.get('deaths', 0)}")
        self.genotypes.setText(
            f"Active genotypes: {metrics.get('active_genotypes', 0)}"
        )
        self.historical_genotypes.setText(
            "Historical genotypes: "
            f"{metrics.get('historical_genotypes', 0)}"
        )
        self.lineages.setText(
            f"Active lineages: {metrics.get('active_lineages', 0)}"
        )
        self.blocked_divisions.setText(
            f"Blocked divisions: {metrics.get('blocked_divisions', 0)}"
        )
        self.waiting_for_memory.setText(
            f"Waiting for memory: {metrics.get('waiting_for_memory', 0)}"
        )
        self.waiting_for_energy.setText(
            f"Waiting for energy: {metrics.get('waiting_for_energy', 0)}"
        )
        self.balance.setText(
            f"Energy balance error: {metrics.get('energy_balance_error', 0)}"
        )
        self.population_data.append(
            float(metrics.get("active_population", 0))
        )
        self.energy_data.append(float(metrics.get("energy_pool", 0)))
        self.population_curve.setData(self.population_data)
        self.energy_curve.setData(self.energy_data)


    def update_snapshot(self, snapshot: dict[str, Any]) -> None:
        organisms = snapshot.get("organisms", [])
        self._organisms = {
            str(organism.get("id")): organism
            for organism in organisms
            if organism.get("id") is not None
        }
        selected = self.organism_selector.currentText()
        self.organism_selector.blockSignals(True)
        self.organism_selector.clear()
        self.organism_selector.addItems(
            sorted(
                self._organisms,
                key=lambda value: int(value),
            )
        )
        if selected in self._organisms:
            self.organism_selector.setCurrentText(selected)
        elif self._organisms:
            self.organism_selector.setCurrentIndex(0)
        self.organism_selector.blockSignals(False)
        self._show_organism(self.organism_selector.currentText())

    def _show_organism(self, organism_id: str) -> None:
        organism = self._organisms.get(organism_id)
        if organism is None:
            self.organism_details.setPlainText(
                "No rendered organism is available."
            )
            return
        self.organism_details.setPlainText(
            json.dumps(
                organism,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )


class EngineController(QWidget):
    event_received = Signal(dict)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.ctx = mp.get_context("spawn")
        self.process: mp.Process | None = None
        self.command_queue: Any = None
        self.event_queue: Any = None
        self.stop_event: Any = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._poll)
        self.timer.start(50)

    def start(self, config: dict[str, Any]) -> None:
        self.stop()
        self.command_queue = self.ctx.Queue()
        self.event_queue = self.ctx.Queue()
        self.stop_event = self.ctx.Event()
        self.process = self.ctx.Process(
            target=engine_process_main,
            args=(
                config,
                self.command_queue,
                self.event_queue,
                self.stop_event,
            ),
            daemon=True,
        )
        self.process.start()
        self.command_queue.put(make_command("start"))

    def send(self, name: str) -> None:
        if self.command_queue is not None:
            self.command_queue.put(make_command(name))

    def stop(self) -> None:
        if self.stop_event is not None:
            self.stop_event.set()
        if self.process is not None and self.process.is_alive():
            self.process.join(timeout=1)
            if self.process.is_alive():
                self.process.terminate()
        self.process = None

    def _poll(self) -> None:
        if self.event_queue is None:
            return
        while True:
            try:
                event = self.event_queue.get_nowait()
            except queue.Empty:
                break
            self.event_received.emit(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Melakat Desktop Lab")
        self.resize(1500, 900)
        self.controller = EngineController(self)
        self.controller.event_received.connect(self._handle_event)
        self.current_config: dict[str, Any] = {}
        self.last_summary: dict[str, Any] | None = None

        toolbar = QToolBar("Simulation", self)
        self.addToolBar(toolbar)
        self._add_action(toolbar, "Start", self._start)
        self._add_action(
            toolbar,
            "Pause",
            lambda: self.controller.send("pause"),
        )
        self._add_action(
            toolbar,
            "Resume",
            lambda: self.controller.send("resume"),
        )
        self._add_action(
            toolbar,
            "Step",
            lambda: self.controller.send("step"),
        )
        self._add_action(
            toolbar,
            "Reset",
            lambda: self.controller.send("reset"),
        )
        self._add_action(toolbar, "Stop", self.controller.stop)
        toolbar.addSeparator()
        self._add_action(toolbar, "Export config", self._export_config)
        self._add_action(toolbar, "Export result", self._export_result)
        self._add_action(toolbar, "Open result", self._open_result)

        self.parameters = ParameterPanel(CORE_SCHEMA)
        self.world = WorldView()
        self.metrics = MetricsPanel()
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)

        split = QSplitter(Qt.Orientation.Horizontal)
        split.addWidget(self.parameters)
        split.addWidget(self.world)
        split.addWidget(self.metrics)
        split.setSizes([330, 760, 360])

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.addWidget(split, 1)
        layout.addWidget(self.log, 0)
        self.setCentralWidget(root)

    def _add_action(
        self,
        toolbar: QToolBar,
        label: str,
        callback: Any,
    ) -> None:
        action = QAction(label, self)
        action.triggered.connect(callback)
        toolbar.addAction(action)

    def _start(self) -> None:
        try:
            config = self.parameters.values()
        except ValueError as exc:
            QMessageBox.critical(self, "Invalid parameters", str(exc))
            return
        self.current_config = config
        self.last_summary = None
        self.metrics.population_data.clear()
        self.metrics.energy_data.clear()
        backend = config.get("run.engine_backend", "phase-zero-vm")
        self.log.appendPlainText(f"Starting {backend} engine...")
        self.controller.start(config)

    def _export_config(self) -> None:
        try:
            config = self.parameters.values()
        except ValueError as exc:
            QMessageBox.critical(self, "Invalid parameters", str(exc))
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export configuration",
            "melakat-config.json",
            "JSON files (*.json)",
        )
        if not path:
            return
        payload = {
            "format": "melakat-config-0.1",
            "config_hash": config_hash(config),
            "config": config,
        }
        try:
            write_json(Path(path), payload)
        except OSError as exc:
            QMessageBox.critical(self, "Export failed", str(exc))
            return
        self.log.appendPlainText(f"Configuration exported: {path}")

    def _export_result(self) -> None:
        if self.last_summary is None:
            QMessageBox.information(
                self,
                "No completed run",
                "Run a simulation before exporting its result.",
            )
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export result",
            "melakat-run.json",
            "JSON files (*.json)",
        )
        if not path:
            return
        try:
            artifact = make_run_artifact(
                self.current_config,
                self.last_summary,
            )
            write_json(Path(path), artifact)
        except OSError as exc:
            QMessageBox.critical(self, "Export failed", str(exc))
            return
        self.log.appendPlainText(f"Result exported: {path}")


    def _open_result(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open result",
            "",
            "JSON files (*.json)",
        )
        if not path:
            return
        try:
            artifact = load_run_artifact(Path(path))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            QMessageBox.critical(self, "Open failed", str(exc))
            return
        self.current_config = artifact["config"]
        self.last_summary = artifact["summary"]
        snapshot = self.last_summary.get("final_snapshot", {})
        self.world.render_snapshot(snapshot)
        self.metrics.update_metrics(self.last_summary)
        self.metrics.update_snapshot(snapshot)
        self.metrics.status.setText("loaded")
        self.log.appendPlainText(
            "Result loaded: "
            f"{path}; "
            f"config_hash={artifact.get('config_hash')}"
        )

    def _handle_event(self, event: dict[str, Any]) -> None:
        name = event.get("name")
        payload = event.get("payload", {})
        if name == "tick":
            self.world.render_snapshot(payload.get("snapshot", {}))
            self.metrics.update_snapshot(payload.get("snapshot", {}))
            self.metrics.update_metrics(payload.get("metrics", {}))
        elif name == "ready":
            self.world.render_snapshot(payload.get("snapshot", {}))
            self.metrics.update_metrics(payload.get("metrics", {}))
        elif name == "status":
            self.metrics.status.setText(
                str(payload.get("status", "unknown"))
            )
        elif name == "reset":
            self.world.render_snapshot(payload.get("snapshot", {}))
            self.metrics.update_metrics(payload.get("metrics", {}))
            self.metrics.status.setText("Paused")
        elif name == "finished":
            self.world.render_snapshot(payload.get("snapshot", {}))
            self.metrics.update_metrics(payload.get("metrics", {}))
            self.last_summary = payload.get("summary")
            self.metrics.update_snapshot(payload.get("snapshot", {}))
            self.metrics.status.setText("finished")
            self.log.appendPlainText(
                "finished: "
                f"{payload.get('reason', 'unknown')}; "
                f"population="
                f"{payload.get('metrics', {}).get('active_population', 0)}; "
                f"births={payload.get('metrics', {}).get('births', 0)}; "
                f"deaths={payload.get('metrics', {}).get('deaths', 0)}"
            )
        elif name == "stopped":
            self.log.appendPlainText("stopped")
        elif name in {"organism_born", "organism_died"}:
            self.log.appendPlainText(f"{name}: {payload}")
        elif name == "reproduction_blocked":
            self.log.appendPlainText(
                f"reproduction_blocked: organism="
                f"{payload.get('organism_id')}; "
                f"reason={payload.get('reason')}"
            )

    def closeEvent(self, event: Any) -> None:
        self.controller.stop()
        event.accept()
