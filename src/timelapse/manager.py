"""Gestión integral de sesiones de timelapse."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

from PySide6.QtCore import QObject, QThreadPool, Signal

import config
from src.models.camera import Camera

from .exporter import TimelapseExporter
from .models import TimelapseSession
from .recorder import TimelapseRecorder


def _slugify(text: str) -> str:
    normalized = [c.lower() if c.isalnum() else "-" for c in text]
    slug = "".join(normalized)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "camara"


class TimelapseManager(QObject):
    sessions_changed = Signal(list)
    session_started = Signal(object)
    session_finished = Signal(object)
    session_error = Signal(str)
    export_completed = Signal(str, str, str)
    export_failed = Signal(str, str)

    def __init__(self) -> None:
        super().__init__()
        self.thread_pool = QThreadPool.globalInstance()
        self.sessions: Dict[str, TimelapseSession] = {}
        self.recorders: Dict[str, TimelapseRecorder] = {}
        config.TIMELAPSE_ROOT.mkdir(parents=True, exist_ok=True)
        self._load_index()

    # ------------------------------------------------------------------
    # Sesiones
    # ------------------------------------------------------------------

    def list_sessions(self) -> List[TimelapseSession]:
        return sorted(
            self.sessions.values(),
            key=lambda session: session.started_at,
            reverse=True,
        )

    def get_session(self, session_id: str) -> Optional[TimelapseSession]:
        return self.sessions.get(session_id)

    def start_timelapse(
        self,
        cameras: Sequence[Camera],
        interval: Optional[int] = None,
        duration_limit: Optional[int] = None,
    ) -> List[TimelapseSession]:
        if not cameras:
            raise ValueError("Debe seleccionar al menos una cámara")

        active = len(self._active_recorders())
        if active + len(cameras) > config.TIMELAPSE_MAX_ACTIVE_RECORDERS:
            raise RuntimeError("Se alcanzó el límite de grabaciones simultáneas")

        interval_seconds = interval or config.TIMELAPSE_DEFAULT_INTERVAL

        created_sessions: List[TimelapseSession] = []
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

        for camera in cameras:
            if not camera.url_imagen:
                raise ValueError(f"La cámara {camera.nombre} no dispone de imagen para capturar")
            session_id = f"{camera.id}-{timestamp}-{len(created_sessions)+1}"
            camera_slug = _slugify(camera.nombre or str(camera.id))
            date_folder = datetime.utcnow().strftime("%Y-%m-%d")
            base_dir = config.TIMELAPSE_ROOT / camera_slug / date_folder / f"session-{session_id}"
            session = TimelapseSession(
                session_id=session_id,
                camera_id=camera.id,
                camera_name=camera.nombre,
                camera_address=camera.direccion,
                image_url=camera.url_imagen,
                interval=interval_seconds,
                started_at=datetime.utcnow().isoformat(timespec="seconds"),
                base_path=str(base_dir),
                duration_limit=duration_limit,
            )

            recorder = TimelapseRecorder(session=session, thread_pool=self.thread_pool)
            recorder.session_updated.connect(self._on_session_updated)
            recorder.session_finished.connect(self._on_session_finished)
            recorder.recorder_error.connect(self._on_session_error)

            self.sessions[session.session_id] = session
            self.recorders[session.session_id] = recorder
            self._persist_session(session)

            recorder.start()
            created_sessions.append(session)
            self.session_started.emit(session)

        self._persist_index()
        self._emit_sessions_changed()
        return created_sessions

    def stop_timelapse(self, session_id: str) -> None:
        recorder = self.recorders.get(session_id)
        if recorder:
            recorder.stop()

    def stop_all(self) -> None:
        for session_id in list(self.recorders.keys()):
            self.stop_timelapse(session_id)

    def delete_session(self, session_id: str) -> None:
        session = self.sessions.get(session_id)
        if not session:
            return

        if session_id in self.recorders:
            self.stop_timelapse(session_id)
            self.recorders.pop(session_id, None)

        base_dir = Path(session.base_path)
        if base_dir.exists():
            for child in sorted(base_dir.glob("**/*"), reverse=True):
                if child.is_file():
                    child.unlink(missing_ok=True)
                elif child.is_dir():
                    child.rmdir()
            if base_dir.exists():
                base_dir.rmdir()

        self.sessions.pop(session_id, None)
        self._persist_index()
        self._emit_sessions_changed()

    def _active_recorders(self) -> List[TimelapseRecorder]:
        return [recorder for recorder in self.recorders.values() if recorder.is_running()]

    def active_session_ids(self) -> List[str]:
        return [session_id for session_id, recorder in self.recorders.items() if recorder.is_running()]

    # ------------------------------------------------------------------
    # Exportación
    # ------------------------------------------------------------------

    def export_session(
        self,
        session_id: str,
        fmt: str,
        output_path: Optional[Path] = None,
    ) -> Path:
        session = self.get_session(session_id)
        if not session:
            raise ValueError("Sesión no encontrada")
        recorder = self.recorders.get(session_id)
        if recorder and recorder.is_running():
            raise RuntimeError("Debes detener la grabación antes de exportar")

        path = TimelapseExporter.export(session, fmt, output_path)
        self._persist_session(session)
        self._persist_index()
        self.export_completed.emit(session_id, fmt, str(path))
        self._emit_sessions_changed()
        return path

    def export_multiple(
        self,
        session_ids: Iterable[str],
        fmt: str,
        output_dir: Optional[Path] = None,
    ) -> List[Path]:
        targets: List[Path] = []
        for session_id in session_ids:
            session = self.get_session(session_id)
            if not session:
                continue
            target_path = None
            if output_dir:
                name = Path(session.base_path).name
                target_path = output_dir / f"{name}.{fmt.lower()}"
            targets.append(self.export_session(session_id, fmt, target_path))
        return targets

    # ------------------------------------------------------------------
    # Eventos de recorder
    # ------------------------------------------------------------------

    def _on_session_updated(self, session: TimelapseSession) -> None:
        self._persist_session(session)
        self._persist_index()
        self._emit_sessions_changed()

    def _on_session_finished(self, session: TimelapseSession) -> None:
        self._persist_session(session)
        self._persist_index()
        self.recorders.pop(session.session_id, None)
        self.session_finished.emit(session)
        self._emit_sessions_changed()

    def _on_session_error(self, session_id: str, message: str) -> None:
        self.session_error.emit(f"{session_id}: {message}")

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------

    def _load_index(self) -> None:
        if not config.TIMELAPSE_INDEX_FILE.exists():
            return
        try:
            with open(config.TIMELAPSE_INDEX_FILE, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError:
            data = {}

        for entry in data.get("sessions", []):
            session = TimelapseSession.from_dict(entry)
            self.sessions[session.session_id] = session

    def _persist_session(self, session: TimelapseSession) -> None:
        session_file = Path(session.base_path) / "session.json"
        session_file.parent.mkdir(parents=True, exist_ok=True)
        with open(session_file, "w", encoding="utf-8") as handle:
            json.dump(session.to_dict(), handle, ensure_ascii=False, indent=2)

    def _persist_index(self) -> None:
        payload = {
            "generated_at": datetime.utcnow().isoformat(timespec="seconds"),
            "sessions": [session.to_dict() for session in self.sessions.values()],
        }
        with open(config.TIMELAPSE_INDEX_FILE, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)

    def _emit_sessions_changed(self) -> None:
        self.sessions_changed.emit(self.list_sessions())