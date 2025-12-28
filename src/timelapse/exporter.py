"""Exportación de sesiones de timelapse a distintos formatos."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import imageio.v2 as imageio

import config
from .models import TimelapseSession


class TimelapseExporter:
    """Convierte sesiones capturadas a formatos de video o animaciones."""

    @staticmethod
    def export(
        session: TimelapseSession,
        fmt: str,
        output_path: Optional[Path] = None,
    ) -> Path:
        fmt_lower = fmt.lower()
        if fmt_lower not in config.TIMELAPSE_EXPORT_FORMATS:
            raise ValueError(f"Formato no soportado: {fmt}")

        frames = session.sorted_frame_paths()
        if not frames:
            raise ValueError("La sesión no contiene fotogramas")

        target_path = output_path or (session.base_dir / f"{session.session_id}.{fmt_lower}")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        fps = TimelapseExporter._resolve_fps(session.interval)

        if fmt_lower == "gif":
            TimelapseExporter._export_gif(frames, target_path, session.interval)
        else:
            # Los formatos de video están deshabilitados en config.py por dependencias externas
            # pero mantenemos la lógica por si el usuario decide instalarlas manualmente.
            TimelapseExporter._export_video(frames, target_path, fps)

        session.register_export(fmt_lower)
        return target_path

    @staticmethod
    def _resolve_fps(interval: int) -> float:
        if interval <= 0:
            return float(config.TIMELAPSE_EXPORT_FPS)
        computed = 1.0 / interval
        if computed < 1.0:
            return 1.0
        if computed > config.TIMELAPSE_EXPORT_FPS:
            return float(config.TIMELAPSE_EXPORT_FPS)
        return float(computed)

    @staticmethod
    def _export_gif(frames: Iterable[Path], output_path: Path, interval: int) -> None:
        duration = max(interval, 0.1)
        images = [imageio.imread(frame) for frame in frames]
        imageio.mimsave(str(output_path), images, duration=duration)

    @staticmethod
    def _export_video(
        frames: Iterable[Path],
        output_path: Path,
        fps: float,
    ) -> None:
        with imageio.get_writer(str(output_path), fps=fps) as writer:
            for frame_path in frames:
                writer.append_data(imageio.imread(frame_path))