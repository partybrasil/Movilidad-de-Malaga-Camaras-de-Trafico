"""Diálogo para configurar nuevas sesiones de timelapse."""

from __future__ import annotations

from typing import Iterable, List, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSpinBox,
    QVBoxLayout,
)

import config
from src.models.camera import Camera


class TimelapseStartDialog(QDialog):
    def __init__(self, cameras: Iterable[Camera], parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Iniciar timelapse")
        self._cameras = list(cameras)
        self.selected_ids: List[int] = []
        self.interval_seconds = config.TIMELAPSE_DEFAULT_INTERVAL
        self.duration_seconds = config.TIMELAPSE_DEFAULT_DURATION

        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header = QLabel("Selecciona las cámaras a grabar y la cadencia de captura.")
        header.setWordWrap(True)
        layout.addWidget(header)

        self.all_checkbox = QCheckBox("Usar todas las cámaras disponibles")
        self.all_checkbox.toggled.connect(self._toggle_all_cameras)
        layout.addWidget(self.all_checkbox)

        self.camera_list = QListWidget()
        self.camera_list.setSelectionMode(QListWidget.NoSelection)
        for camera in self._cameras:
            item = QListWidgetItem(f"{camera.nombre} — {camera.direccion}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, camera.id)
            self.camera_list.addItem(item)
        layout.addWidget(self.camera_list)

        form = QFormLayout()

        self.interval_spin = QSpinBox()
        self.interval_spin.setMinimum(1)
        self.interval_spin.setMaximum(600)
        self.interval_spin.setValue(config.TIMELAPSE_DEFAULT_INTERVAL)
        self.interval_spin.setSuffix(" s")
        form.addRow("Intervalo entre capturas", self.interval_spin)

        duration_container = QHBoxLayout()
        self.duration_checkbox = QCheckBox("Limitar duración")
        self.duration_checkbox.toggled.connect(self._toggle_duration)
        duration_container.addWidget(self.duration_checkbox)

        self.duration_spin = QSpinBox()
        self.duration_spin.setMinimum(1)
        self.duration_spin.setMaximum(240)
        self.duration_spin.setSuffix(" min")
        self.duration_spin.setEnabled(False)
        duration_container.addWidget(self.duration_spin)
        form.addRow("Duración máxima", duration_container)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def _toggle_all_cameras(self, checked: bool) -> None:
        self.camera_list.setEnabled(not checked)

    def _toggle_duration(self, checked: bool) -> None:
        self.duration_spin.setEnabled(checked)

    def _on_accept(self) -> None:
        if self.all_checkbox.isChecked():
            self.selected_ids = [camera.id for camera in self._cameras]
        else:
            selected: List[int] = []
            for index in range(self.camera_list.count()):
                item = self.camera_list.item(index)
                if item.checkState() == Qt.Checked:
                    selected.append(int(item.data(Qt.UserRole)))
            self.selected_ids = selected

        if not self.selected_ids:
            return

        self.interval_seconds = self.interval_spin.value()
        if self.duration_checkbox.isChecked():
            self.duration_seconds = self.duration_spin.value() * 60
        else:
            self.duration_seconds = None

        self.accept()

    def get_selection(self) -> Tuple[List[int], int, int | None]:
        return self.selected_ids, self.interval_seconds, self.duration_seconds