from __future__ import annotations

import json
import multiprocessing as mp
import queue
from pathlib import Path
from typing import Any

import pyqtgraph as pg
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QAction, QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QSplitter,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QGraphicsScene,
    QGraphicsView,
)

from .analysis import compare_artifacts
from .artifacts import config_hash, load_run_artifact, make_run_artifact, write_json
from .parameters import CORE_SCHEMA, ParameterSchema, ParameterSpec
from .protocol import make_command
from .worker import engine_process_main


APP_STYLE = """
QMainWindow, QWidget {
    background: #f4f7fb;
    color: #172033;
    font-size: 13px;
}
QToolBar {
    background: #ffffff;
    border: none;
    border-bottom: 1px solid #dfe6ef;
    spacing: 6px;
    padding: 8px 10px;
}
QToolButton, QPushButton {
    background: #ffffff;
    border: 1px solid #cfd8e5;
    border-radius: 7px;
    padding: 7px 11px;
    color: #1d2a3a;
}
QToolButton:hover, QPushButton:hover {
    background: #eef4fb;
    border-color: #9fb4cc;
}
QToolButton#primaryButton, QPushButton#primaryButton {
    background: #1f6feb;
    color: #ffffff;
    border-color: #1f6feb;
    font-weight: 600;
}
QToolButton#dangerButton, QPushButton#dangerButton {
    background: #fff3f2;
    color: #a12622;
    border-color: #efb2ad;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QPlainTextEdit {
    background: #ffffff;
    border: 1px solid #cfd8e5;
    border-radius: 6px;
    padding: 6px;
    selection-background-color: #cfe2ff;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QPlainTextEdit:focus {
    border-color: #1f6feb;
}
QScrollArea {
    border: none;
    background: transparent;
}
QFrame#panelCard {
    background: #ffffff;
    border: 1px solid #dde5ef;
    border-radius: 10px;
}
QFrame#parameterRow {
    background: #ffffff;
    border: 1px solid #edf1f6;
    border-radius: 7px;
}
QLabel#sectionTitle {
    font-size: 14px;
    font-weight: 700;
    color: #182338;
}
QLabel#panelTitle {
    font-size: 16px;
    font-weight: 700;
    color: #172033;
}
QLabel#mutedLabel {
    color: #637083;
}
QLabel#statusBadge {
    background: #e8f1ff;
    color: #1f5fad;
    border: 1px solid #c8dcf7;
    border-radius: 8px;
    padding: 4px 8px;
    font-weight: 600;
}
QToolButton#accordionButton {
    text-align: left;
    background: #ffffff;
    border: 1px solid #dce5ef;
    border-radius: 8px;
    padding: 9px 10px;
    font-weight: 700;
}
QToolButton#accordionButton:checked {
    background: #eef5ff;
    border-color: #bdd2ed;
}
QSplitter::handle {
    background: #e4eaf2;
}
"""


class CollapsibleSection(QWidget):
    def __init__(self, title: str, *, expanded: bool = False, parent: QWidget | None = None):
        super().__init__(parent)
        self.toggle = QToolButton()
        self.toggle.setObjectName("accordionButton")
        self.toggle.setText(title)
        self.toggle.setCheckable(True)
        self.toggle.setChecked(expanded)
        self.toggle.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle.toggled.connect(self._set_expanded)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(4, 6, 4, 8)
        self.content_layout.setSpacing(6)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        layout.addWidget(self.toggle)
        layout.addWidget(self.content)
        self._set_expanded(expanded)

    def _set_expanded(self, expanded: bool) -> None:
        self.content.setVisible(expanded)
        self.toggle.setArrowType(
            Qt.ArrowType.DownArrow if expanded else Qt.ArrowType.RightArrow
        )

    def set_expanded(self, expanded: bool) -> None:
        self.toggle.setChecked(expanded)


class ParameterPanel(QWidget):
    values_changed = Signal(dict)

    def __init__(self, schema: ParameterSchema, parent: QWidget | None = None):
        super().__init__(parent)
        self.schema = schema
        self.widgets: dict[str, QWidget] = {}
        self.rows: dict[str, QWidget] = {}
        self.sections: dict[str, CollapsibleSection] = {}

        title = QLabel("Experiment setup")
        title.setObjectName("panelTitle")
        subtitle = QLabel("Configure the run without changing the scientific engine contract.")
        subtitle.setObjectName("mutedLabel")
        subtitle.setWordWrap(True)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search parameters…")
        self.search.textChanged.connect(self._filter)

        self.show_advanced = QCheckBox("Show advanced settings")
        self.show_advanced.setChecked(False)
        self.show_advanced.toggled.connect(lambda _checked: self._filter(self.search.text()))

        self.body = QWidget()
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(7)
        self._build()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.body)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 10, 12)
        layout.setSpacing(8)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.search)
        layout.addWidget(self.show_advanced)
        layout.addWidget(scroll, 1)

    def _build(self) -> None:
        grouped: dict[str, list[ParameterSpec]] = {
            group: [] for group in self.schema.groups()
        }
        for spec in self.schema.specs:
            grouped[spec.group].append(spec)

        for group, specs in grouped.items():
            section = CollapsibleSection(
                group,
                expanded=group in {"Run", "World"},
            )
            self.sections[group] = section
            for spec in specs:
                row = QFrame()
                row.setObjectName("parameterRow")
                row_layout = QGridLayout(row)
                row_layout.setContentsMargins(9, 7, 9, 7)
                row_layout.setHorizontalSpacing(8)
                row_layout.setVerticalSpacing(3)

                label = QLabel(spec.label)
                label.setWordWrap(True)
                if spec.advanced:
                    label.setText(f"{spec.label}  ·  Advanced")
                widget = self._widget_for(spec)
                widget.setToolTip(spec.description)
                widget.setMinimumWidth(115)
                widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
                label.setToolTip(spec.description)

                row_layout.addWidget(label, 0, 0)
                row_layout.addWidget(widget, 0, 1)
                row_layout.setColumnStretch(0, 1)
                row_layout.setColumnStretch(1, 0)

                if spec.description:
                    description = QLabel(spec.description)
                    description.setObjectName("mutedLabel")
                    description.setWordWrap(True)
                    row_layout.addWidget(description, 1, 0, 1, 2)

                section.content_layout.addWidget(row)
                self.widgets[spec.path] = widget
                self.rows[spec.path] = row
            self.body_layout.addWidget(section)
        self.body_layout.addStretch()
        self._filter("")

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
                int(spec.minimum if spec.minimum is not None else -2_147_483_648),
                int(spec.maximum if spec.maximum is not None else 2_147_483_647),
            )
            widget.setSingleStep(int(spec.step))
            widget.setValue(int(spec.default))
            return widget
        widget = QDoubleSpinBox()
        widget.setRange(
            float(spec.minimum if spec.minimum is not None else -1e12),
            float(spec.maximum if spec.maximum is not None else 1e12),
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

    def set_values(self, values: dict[str, Any]) -> None:
        for spec in self.schema.specs:
            if spec.path not in values:
                continue
            widget = self.widgets[spec.path]
            value = values[spec.path]
            if isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))
            elif isinstance(widget, QComboBox):
                widget.setCurrentText(str(value))
            elif isinstance(widget, QSpinBox):
                widget.setValue(int(value))
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(float(value))

    def _filter(self, text: str) -> None:
        query = text.strip().lower()
        show_advanced = self.show_advanced.isChecked()
        group_has_visible: dict[str, bool] = {group: False for group in self.sections}

        for spec in self.schema.specs:
            matches = (
                not query
                or query in spec.path.lower()
                or query in spec.label.lower()
                or query in spec.group.lower()
                or query in spec.description.lower()
            )
            advanced_allowed = show_advanced or not spec.advanced or bool(query)
            visible = matches and advanced_allowed
            self.rows[spec.path].setVisible(visible)
            if visible:
                group_has_visible[spec.group] = True

        for group, section in self.sections.items():
            section.setVisible(group_has_visible[group])
            if query and group_has_visible[group]:
                section.set_expanded(True)


class WorldView(QGraphicsView):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setMinimumSize(520, 420)
        self.setBackgroundBrush(QBrush(QColor("#0d1621")))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.show_organisms = True
        self.show_boundaries = True
        self.show_resources = True
        self.last_snapshot: dict[str, Any] = {}

    def set_layers(self, *, organisms: bool, boundaries: bool, resources: bool) -> None:
        self.show_organisms = organisms
        self.show_boundaries = boundaries
        self.show_resources = resources
        if self.last_snapshot:
            self.render_snapshot(self.last_snapshot)

    def _render_resources(self, snapshot: dict[str, Any], width: float, height: float) -> None:
        grid = snapshot.get("resource_grid")
        if not isinstance(grid, dict):
            return
        cols = max(1, int(grid.get("cols", 1)))
        rows = max(1, int(grid.get("rows", 1)))
        values = [float(value) for value in grid.get("values", [])]
        if len(values) != cols * rows:
            return
        maximum = max(values, default=0.0)
        cell_width = width / cols
        cell_height = height / rows
        for row in range(rows):
            for col in range(cols):
                value = values[row * cols + col]
                intensity = 0.0 if maximum <= 0.0 else min(1.0, value / maximum)
                color = QColor.fromHsvF(0.55, 0.72, 0.14 + 0.52 * intensity, 0.72)
                self.scene.addRect(
                    col * cell_width,
                    row * cell_height,
                    cell_width,
                    cell_height,
                    QPen(QColor("#19334a"), 0.08),
                    QBrush(color),
                )

    def render_snapshot(self, snapshot: dict[str, Any]) -> None:
        self.last_snapshot = snapshot
        self.scene.clear()
        width = float(snapshot.get("world_width", 100.0))
        height = float(snapshot.get("world_height", 70.0))
        self.scene.setSceneRect(0, 0, width, height)
        if self.show_resources:
            self._render_resources(snapshot, width, height)
        if self.show_boundaries:
            self.scene.addRect(
                0.0,
                0.0,
                width,
                height,
                QPen(QColor("#dfe9f3"), 0.42),
                QBrush(Qt.BrushStyle.NoBrush),
            )
        if self.show_organisms:
            for organism in snapshot.get("organisms", []):
                radius = max(0.45, min(2.5, float(organism["energy"]) / 18.0))
                color = QColor("#5fd4ff") if int(organism["age"]) % 2 == 0 else QColor("#ffc86a")
                self.scene.addEllipse(
                    float(organism["x"]) - radius,
                    float(organism["y"]) - radius,
                    radius * 2,
                    radius * 2,
                    QPen(QColor("#d9f5ff"), 0.12),
                    QBrush(color),
                )
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)


class ChartWindow(QWidget):
    PLOT_METRICS = (
        "active_population",
        "energy_pool",
        "local_resource_total",
        "mean_local_neighbors",
        "movement_distance",
        "historical_genotypes",
    )

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Melakat — Live time-series")
        self.resize(940, 600)
        self.series: dict[str, list[float]] = {key: [] for key in self.PLOT_METRICS}

        title = QLabel("Live simulation chart")
        title.setObjectName("panelTitle")
        note = QLabel("The chart is presentation-only; it does not alter the simulation state.")
        note.setObjectName("mutedLabel")

        self.metric_selector = QComboBox()
        self.metric_selector.addItems(list(self.PLOT_METRICS))
        self.metric_selector.currentTextChanged.connect(self.refresh)

        self.plot = pg.PlotWidget()
        self.plot.setBackground("#0d1621")
        self.plot.showGrid(x=True, y=True, alpha=0.18)
        self.plot.setLabel("bottom", "Recorded samples")
        self.curve = self.plot.plot(pen=pg.mkPen(width=2.2))

        header = QHBoxLayout()
        header.addWidget(title)
        header.addStretch()
        header.addWidget(QLabel("Metric"))
        header.addWidget(self.metric_selector)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.addLayout(header)
        layout.addWidget(note)
        layout.addWidget(self.plot, 1)

    def set_series(self, series: dict[str, list[float]]) -> None:
        self.series = series
        self.refresh()

    def refresh(self) -> None:
        key = self.metric_selector.currentText()
        values = self.series.get(key, [])
        self.curve.setData(values)
        self.plot.setTitle(key.replace("_", " ").title())
        self.plot.setLabel("left", key.replace("_", " "))


class MetricsPanel(QWidget):
    PLOT_METRICS = ChartWindow.PLOT_METRICS

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.series: dict[str, list[float]] = {key: [] for key in self.PLOT_METRICS}
        self.chart_window: ChartWindow | None = None
        self._organisms: dict[str, dict[str, Any]] = {}

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        heading = QLabel("Research monitor")
        heading.setObjectName("panelTitle")
        self.status = QLabel("Ready")
        self.status.setObjectName("statusBadge")
        header_layout.addWidget(heading)
        header_layout.addStretch()
        header_layout.addWidget(self.status)

        self.engine = QLabel("—")
        self.measurement = QLabel("—")
        self.world_contract = QLabel("—")
        self.config = QLabel("—")
        self.tick = QLabel("0")

        self.population = QLabel("0")
        self.memory = QLabel("0")
        self.instructions = QLabel("0")
        self.faults = QLabel("0")
        self.births = QLabel("0")
        self.deaths = QLabel("0")
        self.genotypes = QLabel("0")
        self.historical_genotypes = QLabel("0")
        self.lineages = QLabel("0")
        self.blocked_divisions = QLabel("0")
        self.waiting_for_memory = QLabel("0")
        self.waiting_for_energy = QLabel("0")

        self.balance = QLabel("0")
        self.resource = QLabel("—")
        self.resource_balance = QLabel("—")
        self.neighbors = QLabel("—")
        self.movement = QLabel("—")
        self.boundary = QLabel("—")

        runtime_card = self._card(
            "Run",
            (
                ("Engine", self.engine),
                ("Measurement", self.measurement),
                ("World contract", self.world_contract),
                ("Config hash", self.config),
                ("Tick", self.tick),
            ),
        )
        population_card = self._card(
            "Population & execution",
            (
                ("Population", self.population),
                ("Memory used", self.memory),
                ("Instructions", self.instructions),
                ("Births", self.births),
                ("Deaths", self.deaths),
                ("Faults", self.faults),
                ("Active genotypes", self.genotypes),
                ("Historical genotypes", self.historical_genotypes),
                ("Active lineages", self.lineages),
                ("Blocked divisions", self.blocked_divisions),
                ("Waiting for memory", self.waiting_for_memory),
                ("Waiting for energy", self.waiting_for_energy),
            ),
        )
        spatial_card = self._card(
            "Energy, resources & space",
            (
                ("Energy balance error", self.balance),
                ("Local resource total", self.resource),
                ("Resource balance error", self.resource_balance),
                ("Mean local neighbors", self.neighbors),
                ("Movement ops / distance", self.movement),
                ("Boundary contacts", self.boundary),
            ),
        )

        self.organism_selector = QComboBox()
        self.organism_selector.setPlaceholderText("Select an organism…")
        self.organism_selector.currentTextChanged.connect(self._show_organism)
        self.organism_details = QPlainTextEdit()
        self.organism_details.setReadOnly(True)
        self.organism_details.setMinimumHeight(140)

        inspector = QFrame()
        inspector.setObjectName("panelCard")
        inspector_layout = QVBoxLayout(inspector)
        inspector_layout.setContentsMargins(12, 12, 12, 12)
        inspector_title = QLabel("Organism inspector")
        inspector_title.setObjectName("sectionTitle")
        inspector_note = QLabel("Position, local resource, neighborhood and VM-visible state.")
        inspector_note.setObjectName("mutedLabel")
        inspector_note.setWordWrap(True)
        inspector_layout.addWidget(inspector_title)
        inspector_layout.addWidget(inspector_note)
        inspector_layout.addWidget(self.organism_selector)
        inspector_layout.addWidget(self.organism_details)

        chart_card = QFrame()
        chart_card.setObjectName("panelCard")
        chart_layout = QVBoxLayout(chart_card)
        chart_layout.setContentsMargins(12, 12, 12, 12)
        chart_title = QLabel("Time-series")
        chart_title.setObjectName("sectionTitle")
        chart_note = QLabel("Open the graph in a dedicated resizable window for readable inspection.")
        chart_note.setObjectName("mutedLabel")
        chart_note.setWordWrap(True)
        self.open_chart_button = QPushButton("Open live chart window")
        self.open_chart_button.setObjectName("primaryButton")
        self.open_chart_button.clicked.connect(self.open_chart)
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(chart_note)
        chart_layout.addWidget(self.open_chart_button)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(9)
        body_layout.addWidget(header)
        body_layout.addWidget(runtime_card)
        body_layout.addWidget(population_card)
        body_layout.addWidget(spatial_card)
        body_layout.addWidget(inspector)
        body_layout.addWidget(chart_card)
        body_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(body)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 12, 12, 12)
        layout.addWidget(scroll)

    def _card(self, title: str, rows: tuple[tuple[str, QLabel], ...]) -> QFrame:
        card = QFrame()
        card.setObjectName("panelCard")
        layout = QGridLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(7)
        heading = QLabel(title)
        heading.setObjectName("sectionTitle")
        layout.addWidget(heading, 0, 0, 1, 2)
        for row_index, (name, value) in enumerate(rows, start=1):
            label = QLabel(name)
            label.setObjectName("mutedLabel")
            value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            value.setWordWrap(True)
            layout.addWidget(label, row_index, 0)
            layout.addWidget(value, row_index, 1)
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        return card

    def open_chart(self) -> None:
        if self.chart_window is None:
            self.chart_window = ChartWindow(self)
        self.chart_window.set_series(self.series)
        self.chart_window.show()
        self.chart_window.raise_()
        self.chart_window.activateWindow()

    def reset_series(self) -> None:
        for values in self.series.values():
            values.clear()
        if self.chart_window is not None:
            self.chart_window.refresh()

    def update_metrics(self, metrics: dict[str, Any]) -> None:
        self.engine.setText(str(metrics.get("engine_version", "unknown")))
        self.measurement.setText(str(metrics.get("measurement_version", "unknown")))
        self.world_contract.setText(str(metrics.get("world_contract_version", "—")))
        self.config.setText(str(metrics.get("config_hash", "unknown")))
        self.tick.setText(str(metrics.get("tick", 0)))
        self.population.setText(str(metrics.get("active_population", 0)))
        self.memory.setText(str(metrics.get("memory_used", 0)))
        self.instructions.setText(str(metrics.get("instructions_executed", 0)))
        self.faults.setText(str(metrics.get("faults", 0)))
        self.births.setText(str(metrics.get("births", 0)))
        self.deaths.setText(str(metrics.get("deaths", 0)))
        self.genotypes.setText(str(metrics.get("active_genotypes", 0)))
        self.historical_genotypes.setText(str(metrics.get("historical_genotypes", 0)))
        self.lineages.setText(str(metrics.get("active_lineages", 0)))
        self.blocked_divisions.setText(str(metrics.get("blocked_divisions", 0)))
        self.waiting_for_memory.setText(str(metrics.get("waiting_for_memory", 0)))
        self.waiting_for_energy.setText(str(metrics.get("waiting_for_energy", 0)))
        self.balance.setText(str(metrics.get("energy_balance_error", 0)))
        self.resource.setText(str(metrics.get("local_resource_total", "—")))
        self.resource_balance.setText(str(metrics.get("local_resource_balance_error", "—")))
        self.neighbors.setText(str(metrics.get("mean_local_neighbors", "—")))
        self.movement.setText(
            f"{metrics.get('movement_operations', '—')} / {metrics.get('movement_distance', '—')}"
        )
        self.boundary.setText(str(metrics.get("boundary_contacts", "—")))

        for key in self.PLOT_METRICS:
            value = metrics.get(key, 0.0)
            try:
                self.series[key].append(float(value))
            except (TypeError, ValueError):
                self.series[key].append(0.0)
        if self.chart_window is not None and self.chart_window.isVisible():
            self.chart_window.refresh()

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
        self.organism_selector.addItems(sorted(self._organisms, key=lambda value: int(value)))
        if selected in self._organisms:
            self.organism_selector.setCurrentText(selected)
        elif self._organisms:
            self.organism_selector.setCurrentIndex(0)
        self.organism_selector.blockSignals(False)
        self._show_organism(self.organism_selector.currentText())

    def _show_organism(self, organism_id: str) -> None:
        organism = self._organisms.get(organism_id)
        if organism is None:
            self.organism_details.setPlainText("No rendered organism is available.")
            return
        self.organism_details.setPlainText(
            json.dumps(organism, ensure_ascii=False, indent=2, sort_keys=True)
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
            args=(config, self.command_queue, self.event_queue, self.stop_event),
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
        self.setWindowTitle("Melakat Desktop Lab — Phase Two")
        self.resize(1600, 940)
        self.setStyleSheet(APP_STYLE)
        self.controller = EngineController(self)
        self.controller.event_received.connect(self._handle_event)
        self.current_config: dict[str, Any] = {}
        self.last_summary: dict[str, Any] | None = None

        toolbar = QToolBar("Simulation", self)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        self._add_toolbar_button(toolbar, "Start", self._start, role="primary")
        self._add_toolbar_button(toolbar, "Pause", lambda: self.controller.send("pause"))
        self._add_toolbar_button(toolbar, "Resume", lambda: self.controller.send("resume"))
        self._add_toolbar_button(toolbar, "Step", lambda: self.controller.send("step"))
        self._add_toolbar_button(toolbar, "Reset", lambda: self.controller.send("reset"))
        self._add_toolbar_button(toolbar, "Stop", self.controller.stop, role="danger")
        toolbar.addSeparator()
        self._add_action(toolbar, "Export config", self._export_config)
        self._add_action(toolbar, "Export result", self._export_result)
        self._add_action(toolbar, "Open result", self._open_result)
        self._add_action(toolbar, "Compare results", self._compare_results)

        self.parameters = ParameterPanel(CORE_SCHEMA)
        self.world = WorldView()
        self.metrics = MetricsPanel()
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumBlockCount(4000)

        self.organism_layer = QCheckBox("Organisms")
        self.boundary_layer = QCheckBox("Boundaries")
        self.resource_layer = QCheckBox("Resources")
        for checkbox in (self.organism_layer, self.boundary_layer, self.resource_layer):
            checkbox.setChecked(True)
            checkbox.toggled.connect(self._update_layers)

        world_panel = QFrame()
        world_panel.setObjectName("panelCard")
        world_layout = QVBoxLayout(world_panel)
        world_layout.setContentsMargins(10, 10, 10, 10)
        world_layout.setSpacing(8)
        world_header = QHBoxLayout()
        world_title = QLabel("World")
        world_title.setObjectName("panelTitle")
        world_hint = QLabel("Visible layers")
        world_hint.setObjectName("mutedLabel")
        world_header.addWidget(world_title)
        world_header.addStretch()
        world_header.addWidget(world_hint)
        world_header.addWidget(self.organism_layer)
        world_header.addWidget(self.boundary_layer)
        world_header.addWidget(self.resource_layer)
        world_layout.addLayout(world_header)
        world_layout.addWidget(self.world, 1)

        split = QSplitter(Qt.Orientation.Horizontal)
        split.addWidget(self.parameters)
        split.addWidget(world_panel)
        split.addWidget(self.metrics)
        split.setStretchFactor(0, 0)
        split.setStretchFactor(1, 1)
        split.setStretchFactor(2, 0)
        split.setSizes([330, 880, 390])

        event_panel = QFrame()
        event_panel.setObjectName("panelCard")
        event_layout = QVBoxLayout(event_panel)
        event_layout.setContentsMargins(10, 8, 10, 10)
        event_layout.setSpacing(6)
        event_header = QHBoxLayout()
        event_title = QLabel("Event log")
        event_title.setObjectName("sectionTitle")
        self.event_filter = QComboBox()
        self.event_filter.addItems(
            ("all", "birth/death", "movement", "boundary", "resource", "reproduction")
        )
        clear_log = QPushButton("Clear")
        clear_log.clicked.connect(self.log.clear)
        event_header.addWidget(event_title)
        event_header.addStretch()
        event_header.addWidget(QLabel("Filter"))
        event_header.addWidget(self.event_filter)
        event_header.addWidget(clear_log)
        event_layout.addLayout(event_header)
        event_layout.addWidget(self.log)
        event_panel.setMaximumHeight(220)

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        layout.addWidget(split, 1)
        layout.addWidget(event_panel, 0)
        self.setCentralWidget(root)

    def _add_toolbar_button(
        self,
        toolbar: QToolBar,
        label: str,
        callback: Any,
        *,
        role: str | None = None,
    ) -> None:
        button = QToolButton()
        button.setText(label)
        if role == "primary":
            button.setObjectName("primaryButton")
        elif role == "danger":
            button.setObjectName("dangerButton")
        button.clicked.connect(callback)
        toolbar.addWidget(button)

    def _add_action(self, toolbar: QToolBar, label: str, callback: Any) -> None:
        action = QAction(label, self)
        action.triggered.connect(callback)
        toolbar.addAction(action)

    def _update_layers(self, _checked: bool | None = None) -> None:
        self.world.set_layers(
            organisms=self.organism_layer.isChecked(),
            boundaries=self.boundary_layer.isChecked(),
            resources=self.resource_layer.isChecked(),
        )

    def _start(self) -> None:
        try:
            config = self.parameters.values()
        except ValueError as exc:
            QMessageBox.critical(self, "Invalid parameters", str(exc))
            return
        self.current_config = config
        self.last_summary = None
        self.metrics.reset_series()
        self.organism_layer.setChecked(bool(config.get("visual.show_organisms", True)))
        self.boundary_layer.setChecked(bool(config.get("visual.show_boundaries", True)))
        self.resource_layer.setChecked(bool(config.get("visual.show_resources", True)))
        self._update_layers()
        backend = config.get("run.engine_backend", "phase-zero-vm")
        self.log.appendPlainText(f"Starting {backend} engine…")
        self.controller.start(config)

    def _export_config(self) -> None:
        try:
            config = self.parameters.values()
        except ValueError as exc:
            QMessageBox.critical(self, "Invalid parameters", str(exc))
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export configuration", "melakat-config.json", "JSON files (*.json)"
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
                self, "No completed run", "Run a simulation before exporting its result."
            )
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export result", "melakat-run.json", "JSON files (*.json)"
        )
        if not path:
            return
        try:
            artifact = make_run_artifact(self.current_config, self.last_summary)
            write_json(Path(path), artifact)
        except OSError as exc:
            QMessageBox.critical(self, "Export failed", str(exc))
            return
        self.log.appendPlainText(f"Result exported: {path}")

    def _open_result(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open result", "", "JSON files (*.json)")
        if not path:
            return
        try:
            artifact = load_run_artifact(Path(path))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            QMessageBox.critical(self, "Open failed", str(exc))
            return
        self.current_config = artifact["config"]
        self.parameters.set_values(self.current_config)
        self.last_summary = artifact["summary"]
        snapshot = self.last_summary.get("final_snapshot", {})
        self.world.render_snapshot(snapshot)
        self.metrics.reset_series()
        for sample in self.last_summary.get("history", []):
            self.metrics.update_metrics(sample)
        self.metrics.update_metrics(self.last_summary)
        self.metrics.update_snapshot(snapshot)
        self.metrics.status.setText("Loaded")
        self.log.appendPlainText(
            f"Result loaded: {path}; config_hash={artifact.get('config_hash')}"
        )

    def _compare_results(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(self, "Compare results", "", "JSON files (*.json)")
        if len(paths) != 2:
            return
        try:
            first = load_run_artifact(Path(paths[0]))
            second = load_run_artifact(Path(paths[1]))
            report = compare_artifacts(first, second)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            QMessageBox.critical(self, "Compare failed", str(exc))
            return
        text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
        self.log.appendPlainText("Result comparison:\n" + text)
        QMessageBox.information(
            self,
            "Result comparison",
            "Same artifact: "
            f"{report['same_artifact']}\n"
            "Same configuration: "
            f"{report['same_config']}\n"
            "Configuration differs only by seed: "
            f"{report['same_config_except_seed']}",
        )

    def _event_visible(self, name: str, payload: dict[str, Any]) -> bool:
        selected = self.event_filter.currentText()
        if selected == "all":
            return True
        groups = {
            "birth/death": {"organism_born", "organism_died"},
            "movement": {"organism_moved"},
            "resource": {"resource_captured", "resource_renewed"},
            "reproduction": {"reproduction_blocked", "organism_born"},
        }
        if selected == "boundary":
            return name in {"organism_born", "organism_moved"} and int(
                payload.get("boundary_contacts", 0) or 0
            ) > 0
        return name in groups.get(selected, set())

    def _handle_event(self, event: dict[str, Any]) -> None:
        name = str(event.get("name", ""))
        payload = event.get("payload", {})
        if name in {"tick", "ready", "reset", "finished"}:
            snapshot = payload.get("snapshot", {})
            metrics = payload.get("metrics", {})
            self.world.render_snapshot(snapshot)
            self.metrics.update_snapshot(snapshot)
            self.metrics.update_metrics(metrics)
        if name == "ready":
            self.metrics.status.setText("Ready")
        elif name == "status":
            self.metrics.status.setText(str(payload.get("status", "Unknown")).title())
        elif name == "reset":
            self.metrics.status.setText("Paused")
        elif name == "finished":
            self.last_summary = payload.get("summary")
            self.metrics.status.setText("Finished")
            self.log.appendPlainText(
                "finished: "
                f"{payload.get('reason', 'unknown')}; "
                f"population={payload.get('metrics', {}).get('active_population', 0)}; "
                f"births={payload.get('metrics', {}).get('births', 0)}; "
                f"deaths={payload.get('metrics', {}).get('deaths', 0)}"
            )
        elif name == "stopped":
            self.log.appendPlainText("stopped")
        elif name in {
            "organism_born",
            "organism_died",
            "organism_moved",
            "resource_captured",
            "resource_renewed",
            "reproduction_blocked",
        } and self._event_visible(name, payload):
            self.log.appendPlainText(f"{name}: {payload}")

    def closeEvent(self, event: Any) -> None:
        self.controller.stop()
        event.accept()
