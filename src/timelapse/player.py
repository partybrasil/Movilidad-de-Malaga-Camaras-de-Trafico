"""Reproductor de sesiones de timelapse dentro de la aplicación."""

from __future__ import annotations

from datetime import datetime, timedelta
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

import config
from .models import TimelapseSession


def _format_timestamp(text: str) -> str:
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return text
    return dt.strftime("%d/%m/%Y %H:%M:%S")


class TimelapsePlayerDialog(QDialog):
    def __init__(self, session: TimelapseSession, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Reproductor - {session.camera_name}")
        self.session = session
        self.frames = session.frames
        self.current_index = 0
        self.speed_factor = 1.0
        self._current_pixmap: QPixmap | None = None
        self._scrubbing = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._next_frame)

        self._setup_ui()
        self._update_controls_state()
        if self.frames:
            self._show_frame(0)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.viewer = QLabel("Sin fotogramas disponibles")
        self.viewer.setAlignment(Qt.AlignCenter)
        self.viewer.setMinimumSize(640, 360)
        self.viewer.setStyleSheet("background-color: #1c2833; color: white; border-radius: 8px;")
        layout.addWidget(self.viewer)

        self.overlay = QLabel(self.viewer)
        self.overlay.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.6); color: white;"
            "border-radius: 4px; padding: 4px 8px;"
        )
        self.overlay.move(16, 16)
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.overlay.hide()

        slider_layout = QHBoxLayout()
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setMinimum(0)
        if self.frames:
            self.position_slider.setMaximum(len(self.frames) - 1)
        self.position_slider.valueChanged.connect(self._on_slider_changed)
        self.position_slider.sliderPressed.connect(self._on_slider_pressed)
        self.position_slider.sliderReleased.connect(self._on_slider_released)
        slider_layout.addWidget(self.position_slider)
        layout.addLayout(slider_layout)

        controls = QHBoxLayout()
        controls.setSpacing(8)

        self.play_btn = QPushButton("▶ Reproducir")
        self.play_btn.clicked.connect(self._toggle_playback)
        controls.addWidget(self.play_btn)

        self.step_back_btn = QPushButton("⏮")
        self.step_back_btn.clicked.connect(lambda: self._step_frame(-1))
        controls.addWidget(self.step_back_btn)

        self.step_forward_btn = QPushButton("⏭")
        self.step_forward_btn.clicked.connect(lambda: self._step_frame(1))
        controls.addWidget(self.step_forward_btn)

        controls.addStretch()

        self.speed_combo = QComboBox()
        for speed in config.TIMELAPSE_PLAYBACK_SPEEDS:
            self.speed_combo.addItem(f"{speed}x", speed)
        default_index = self.speed_combo.findData(1.0)
        if default_index >= 0:
            self.speed_combo.setCurrentIndex(default_index)
        self.speed_combo.currentIndexChanged.connect(self._on_speed_changed)
        controls.addWidget(QLabel("Velocidad:"))
        controls.addWidget(self.speed_combo)

        layout.addLayout(controls)

        info_layout = QHBoxLayout()
        info_layout.setSpacing(8)
        self.frame_info = QLabel("Fotograma 0/0")
        self.time_info = QLabel("")
        info_layout.addWidget(self.frame_info)
        info_layout.addStretch()
        info_layout.addWidget(self.time_info)
        layout.addLayout(info_layout)

        footer = QHBoxLayout()
        footer.addStretch()
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        layout.addLayout(footer)

        self.setLayout(layout)

    def _toggle_playback(self) -> None:
        if not self.frames:
            return
        if self.timer.isActive():
            self.timer.stop()
            self.play_btn.setText("▶ Reproducir")
        else:
            self._apply_timer_interval()
            self.timer.start()
            self.play_btn.setText("⏸ Pausar")

    def _apply_timer_interval(self) -> None:
        interval_ms = max(int(self.session.interval * 1000 / self.speed_factor), 50)
        self.timer.setInterval(interval_ms)

    def _next_frame(self) -> None:
        if not self.frames:
            return
        next_index = (self.current_index + 1) % len(self.frames)
        self._show_frame(next_index)

    def _step_frame(self, step: int) -> None:
        if not self.frames:
            return
        self.timer.stop()
        self.play_btn.setText("▶ Reproducir")
        next_index = (self.current_index + step) % len(self.frames)
        self._show_frame(next_index)

    def _show_frame(self, index: int) -> None:
        if not self.frames:
            return
        if index < 0 or index >= len(self.frames):
            return
        frame = self.frames[index]
        frame_path = self.session.frames_dir / frame.filename
        if not frame_path.exists():
            self.time_info.setText("Fotograma faltante")
            return

        pixmap = QPixmap(str(frame_path))
        if pixmap.isNull():
            self.time_info.setText("Error al cargar fotograma")
            return

        self._current_pixmap = pixmap
        self.current_index = index
        self._update_viewer_pixmap()

        self.position_slider.blockSignals(True)
        self.position_slider.setValue(index)
        self.position_slider.blockSignals(False)

        self.frame_info.setText(f"Fotograma {index + 1}/{len(self.frames)}")
        self.overlay.setText(_format_timestamp(frame.captured_at))
        self.overlay.adjustSize()
        self.overlay.show()

        start_dt = datetime.fromisoformat(self.session.started_at)
        elapsed = timedelta(seconds=self.session.interval * index)
        self.time_info.setText(
            f"Inicio: {_format_timestamp(self.session.started_at)} | +{elapsed}"
        )

    def _update_viewer_pixmap(self) -> None:
        if not self._current_pixmap:
            return
        scaled = self._current_pixmap.scaled(
            self.viewer.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.viewer.setPixmap(scaled)
        self.overlay.move(16, 16)

    def resizeEvent(self, event) -> None:  # noqa: N802 - firmado por Qt
        super().resizeEvent(event)
        self._update_viewer_pixmap()

    def _on_speed_changed(self) -> None:
        self.speed_factor = float(self.speed_combo.currentData())
        if self.timer.isActive():
            self._apply_timer_interval()

    def _on_slider_changed(self, value: int) -> None:
        if self._scrubbing:
            return
        self._show_frame(value)

    def _on_slider_pressed(self) -> None:
        self._scrubbing = True
        self.timer.stop()
        self.play_btn.setText("▶ Reproducir")

    def _on_slider_released(self) -> None:
        self._scrubbing = False
        self._show_frame(self.position_slider.value())

    def _update_controls_state(self) -> None:
        has_frames = bool(self.frames)
        for control in [
            self.play_btn,
            self.step_back_btn,
            self.step_forward_btn,
            self.position_slider,
            self.speed_combo,
        ]:
            control.setEnabled(has_frames)
        if not has_frames:
            self.frame_info.setText("Sin fotogramas")
            self.time_info.setText("")