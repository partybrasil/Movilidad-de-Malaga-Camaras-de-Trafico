"""Captura periódica de fotogramas para sesiones de timelapse."""

from __future__ import annotations

import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from PySide6.QtCore import QObject, QRunnable, QThreadPool, QTimer, Signal

import config
from .models import TimelapseSession


class FrameCaptureSignals(QObject):
    success = Signal(str, str, str)  # session_id, filename, timestamp
    error = Signal(str, str)  # session_id, error


class FrameCaptureTask(QRunnable):
    def __init__(self, session_id: str, image_url: str, output_path: Path):
        super().__init__()
        self.session_id = session_id
        self.image_url = image_url
        self.output_path = output_path
        self.signals = FrameCaptureSignals()

    def run(self) -> None:
        try:
            headers = config.IMAGE_REQUEST_HEADERS
            response = requests.get(
                self.image_url,
                timeout=config.IMAGE_TIMEOUT,
                headers=headers,
                stream=True,
            )
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "image" not in content_type:
                raise RuntimeError(f"Respuesta no es una imagen ({content_type})")

            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.output_path, "wb") as handle:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        handle.write(chunk)

            timestamp = datetime.utcnow().isoformat(timespec="seconds")
            self.signals.success.emit(
                self.session_id,
                self.output_path.name,
                timestamp,
            )
        except Exception as exc:  # noqa: BLE001 - cualquier error de red debe notificarse
            self.signals.error.emit(self.session_id, str(exc))


class TimelapseRecorder(QObject):
    session_updated = Signal(object)
    session_finished = Signal(object)
    recorder_error = Signal(str, str)

    def __init__(
        self,
        session: TimelapseSession,
        thread_pool: Optional[QThreadPool] = None,
    ) -> None:
        super().__init__()
        self.session = session
        self.thread_pool = thread_pool or QThreadPool.globalInstance()
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self._schedule_capture)
        self._running = False
        self._sequence = 0
        self._lock = threading.Lock()
        self._capture_inflight = False
        self._start_epoch = datetime.utcnow()

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self.session.frames_dir.mkdir(parents=True, exist_ok=True)
        self._start_epoch = datetime.utcnow()
        self._schedule_capture()
        self.timer.start(self.session.interval * 1000)

    def stop(self) -> None:
        if not self._running:
            return
        self.timer.stop()
        self._running = False
        self.session.mark_finished()
        self.session_finished.emit(self.session)

    def is_running(self) -> bool:
        return self._running

    def _schedule_capture(self) -> None:
        if not self._running:
            return
        if self.session.duration_limit:
            elapsed = (datetime.utcnow() - self._start_epoch).total_seconds()
            if elapsed >= self.session.duration_limit:
                self.stop()
                return

        with self._lock:
            if self._capture_inflight:
                return
            self._capture_inflight = True
            self._sequence += 1
            filename = f"frame_{self._sequence:05d}.{config.TIMELAPSE_FRAME_FORMAT}"
            task = FrameCaptureTask(
                session_id=self.session.session_id,
                image_url=self.session.image_url,
                output_path=self.session.frames_dir / filename,
            )
            task.signals.success.connect(self._on_frame_captured)
            task.signals.error.connect(self._on_capture_error)
            self.thread_pool.start(task)

    def _on_frame_captured(self, session_id: str, filename: str, captured_at: str) -> None:
        with self._lock:
            self._capture_inflight = False
        if session_id != self.session.session_id:
            return
        self.session.append_frame(filename, captured_at)
        self.session_updated.emit(self.session)

    def _on_capture_error(self, session_id: str, error_message: str) -> None:
        with self._lock:
            self._capture_inflight = False
        if session_id != self.session.session_id:
            return
        self.recorder_error.emit(session_id, error_message)