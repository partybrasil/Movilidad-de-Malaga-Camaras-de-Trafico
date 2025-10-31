"""Biblioteca y gestor de sesiones de timelapse."""

from __future__ import annotations

from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

import config
from src.controllers.camera_controller import CameraController
from src.timelapse.player import TimelapsePlayerDialog
from src.timelapse.models import TimelapseSession
from .timelapse_start_dialog import TimelapseStartDialog


class TimelapseLibraryDialog(QDialog):
    def __init__(self, controller: CameraController, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Timelapses almacenados")
        self.resize(820, 520)
        self.controller = controller

        self._setup_ui()
        self._connect_signals()
        self._reload_table()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Cámara",
            "Inicio",
            "Duración",
            "Fotogramas",
            "Formatos",
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)

        self.new_btn = QPushButton("➕ Iniciar")
        self.new_btn.clicked.connect(self._on_new_session)
        buttons.addWidget(self.new_btn)

        self.stop_btn = QPushButton("⏹ Detener")
        self.stop_btn.clicked.connect(self._on_stop_session)
        buttons.addWidget(self.stop_btn)

        self.play_btn = QPushButton("▶ Reproducir")
        self.play_btn.clicked.connect(self._on_play_session)
        buttons.addWidget(self.play_btn)

        self.export_btn = QPushButton("💾 Exportar")
        self.export_btn.clicked.connect(self._on_export_session)
        buttons.addWidget(self.export_btn)

        self.delete_btn = QPushButton("🗑 Eliminar")
        self.delete_btn.clicked.connect(self._on_delete_session)
        buttons.addWidget(self.delete_btn)

        buttons.addStretch()

        self.refresh_btn = QPushButton("🔁 Actualizar")
        self.refresh_btn.clicked.connect(self._reload_table)
        buttons.addWidget(self.refresh_btn)

        layout.addLayout(buttons)
        self.setLayout(layout)

    def _connect_signals(self) -> None:
        self.controller.timelapse_sessions_changed.connect(lambda _: self._reload_table())
        self.controller.timelapse_session_started.connect(lambda _: self._reload_table())
        self.controller.timelapse_session_finished.connect(lambda _: self._reload_table())
        self.controller.timelapse_error.connect(self._on_error)
        self.controller.timelapse_export_completed.connect(self._on_export_completed)

    def _on_error(self, message: str) -> None:
        QMessageBox.warning(self, "Timelapse", message)

    def _on_export_completed(self, session_id: str, fmt: str, path: str) -> None:
        self.status_label.setText(f"Exportación completada: {session_id} → {fmt.upper()} ({path})")

    def _reload_table(self) -> None:
        sessions = self.controller.get_timelapse_sessions()
        self.table.setRowCount(0)
        active = 0
        for session in sessions:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(session.session_id))
            self.table.setItem(row, 1, QTableWidgetItem(session.camera_name))
            self.table.setItem(row, 2, QTableWidgetItem(session.started_at))
            self.table.setItem(row, 3, QTableWidgetItem(self._format_duration(session)))
            self.table.setItem(row, 4, QTableWidgetItem(str(session.frame_count)))
            formats = ", ".join(sorted({fmt.upper() for fmt in session.exported_formats})) or "-"
            self.table.setItem(row, 5, QTableWidgetItem(formats))
            if session.session_id in self.controller.get_active_timelapse_ids():
                active += 1

        self.status_label.setText(
            f"Sesiones totales: {len(sessions)} | Activas: {active} / {config.TIMELAPSE_MAX_ACTIVE_RECORDERS}"
        )
        if self.table.rowCount() > 0:
            self.table.selectRow(0)

    def _current_session(self) -> TimelapseSession | None:
        row = self.table.currentRow()
        if row < 0:
            return None
        session_id_item = self.table.item(row, 0)
        if not session_id_item:
            return None
        return self.controller.get_timelapse_session(session_id_item.text())

    def _on_new_session(self) -> None:
        dialog = TimelapseStartDialog(self.controller.get_all_cameras(), self)
        if dialog.exec() != QDialog.Accepted:
            return
        camera_ids, interval, duration = dialog.get_selection()
        try:
            self.controller.start_timelapse(camera_ids, interval, duration)
        except Exception as exc:  # noqa: BLE001 - mostrar error directo
            QMessageBox.critical(self, "No se pudo iniciar", str(exc))

    def _on_stop_session(self) -> None:
        session = self._current_session()
        if not session:
            return
        self.controller.stop_timelapse(session.session_id)

    def _on_play_session(self) -> None:
        session = self._current_session()
        if not session:
            return
        dialog = TimelapsePlayerDialog(session, self)
        dialog.exec()

    def _on_export_session(self) -> None:
        session = self._current_session()
        if not session:
            return
        formats = config.TIMELAPSE_EXPORT_FORMATS
        fmt, ok = QInputDialog.getItem(
            self,
            "Exportar timelapse",
            "Selecciona formato",
            [item.upper() for item in formats],
            0,
            False,
        )
        if not ok:
            return
        fmt = fmt.lower()

        suggested = session.base_dir / f"{session.session_id}.{fmt}"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar como",
            str(suggested),
            f"*.{fmt}",
        )
        if not file_path:
            return
        try:
            self.controller.export_timelapse(session.session_id, fmt, file_path)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Error de exportación", str(exc))

    def _on_delete_session(self) -> None:
        session = self._current_session()
        if not session:
            return
        if QMessageBox.question(
            self,
            "Eliminar timelapse",
            "¿Estás seguro de eliminar la sesión seleccionada? Se perderán los fotogramas.",
        ) == QMessageBox.Yes:
            self.controller.delete_timelapse(session.session_id)

    @staticmethod
    def _format_duration(session: TimelapseSession) -> str:
        seconds = session.duration_seconds()
        if not seconds:
            return "-"
        minutes, secs = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"