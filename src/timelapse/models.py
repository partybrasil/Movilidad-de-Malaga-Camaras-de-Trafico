"""Modelos y estructuras de datos para la gestión de timelapses."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


@dataclass
class TimelapseFrame:
    """Representa un fotograma capturado en una sesión."""

    filename: str
    captured_at: str

    def to_dict(self) -> Dict[str, str]:
        return {"filename": self.filename, "captured_at": self.captured_at}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimelapseFrame":
        return cls(
            filename=data.get("filename", ""),
            captured_at=data.get("captured_at", _now_iso()),
        )


@dataclass
class TimelapseSession:
    """Información persistida de una sesión de timelapse."""

    session_id: str
    camera_id: int
    camera_name: str
    camera_address: str
    image_url: str
    interval: int
    started_at: str
    base_path: str
    status: str = "recording"
    ended_at: Optional[str] = None
    frame_count: int = 0
    frames: List[TimelapseFrame] = field(default_factory=list)
    duration_limit: Optional[int] = None
    exported_formats: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "camera_id": self.camera_id,
            "camera_name": self.camera_name,
            "camera_address": self.camera_address,
            "image_url": self.image_url,
            "interval": self.interval,
            "started_at": self.started_at,
            "base_path": self.base_path,
            "status": self.status,
            "ended_at": self.ended_at,
            "frame_count": self.frame_count,
            "frames": [frame.to_dict() for frame in self.frames],
            "duration_limit": self.duration_limit,
            "exported_formats": self.exported_formats,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimelapseSession":
        frames_raw = data.get("frames", [])
        return cls(
            session_id=data.get("session_id", ""),
            camera_id=int(data.get("camera_id", 0)),
            camera_name=data.get("camera_name", ""),
            camera_address=data.get("camera_address", ""),
            image_url=data.get("image_url", ""),
            interval=int(data.get("interval", 1)),
            started_at=data.get("started_at", _now_iso()),
            base_path=data.get("base_path", ""),
            status=data.get("status", "recording"),
            ended_at=data.get("ended_at"),
            frame_count=int(data.get("frame_count", 0)),
            frames=[TimelapseFrame.from_dict(frame) for frame in frames_raw],
            duration_limit=data.get("duration_limit"),
            exported_formats=list(data.get("exported_formats", [])),
        )

    @property
    def base_dir(self) -> Path:
        return Path(self.base_path)

    @property
    def frames_dir(self) -> Path:
        return self.base_dir / "frames"

    def append_frame(self, filename: str, captured_at: str) -> None:
        self.frames.append(TimelapseFrame(filename=filename, captured_at=captured_at))
        self.frame_count = len(self.frames)

    def mark_finished(self) -> None:
        if not self.ended_at:
            self.ended_at = _now_iso()
        self.status = "finished"

    def duration_seconds(self) -> int:
        if not self.frames:
            return 0
        if self.ended_at:
            end_dt = datetime.fromisoformat(self.ended_at)
        else:
            end_dt = datetime.utcnow()
        start_dt = datetime.fromisoformat(self.started_at)
        return int((end_dt - start_dt).total_seconds())

    def has_format(self, fmt: str) -> bool:
        return fmt.lower() in {f.lower() for f in self.exported_formats}

    def register_export(self, fmt: str) -> None:
        fmt_lower = fmt.lower()
        if fmt_lower not in {f.lower() for f in self.exported_formats}:
            self.exported_formats.append(fmt_lower)

    def sorted_frame_paths(self) -> List[Path]:
        return [self.frames_dir / frame.filename for frame in self.frames]