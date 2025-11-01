"""Gestión persistente de preferencias de usuario.

Este módulo implementa utilidades ligeras para almacenar y recuperar
preferencias relacionadas con la aplicación de cámaras, incluyendo la
lista de cámaras favoritas. Se prioriza la portabilidad usando únicamente
biblioteca estándar.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List
import json
import logging
import os
import platform

import config


logger = logging.getLogger(__name__)


class FavoritesManager:
    """Gestiona la persistencia de cámaras favoritas."""

    def __init__(self, base_dir: Path | None = None, file_name: str | None = None) -> None:
        self._base_dir = base_dir or self._default_base_dir()
        self._file_name = file_name or config.FAVORITES_FILE_NAME
        self._storage_path = self._base_dir / self._file_name

        try:
            self._base_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:  # pragma: no cover - entorno dependiente
            logger.error("No se pudo crear el directorio de preferencias %s: %s", self._base_dir, exc)
            raise

    @staticmethod
    def _default_base_dir() -> Path:
        """Calcula un directorio adecuado según el sistema operativo."""
        system = platform.system()

        if system == "Windows":
            appdata = os.getenv("APPDATA")
            base = Path(appdata) if appdata else Path.home() / "AppData" / "Roaming"
        elif system == "Darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            xdg_config = os.getenv("XDG_CONFIG_HOME")
            base = Path(xdg_config) if xdg_config else Path.home() / ".config"

        return base / config.APP_DATA_DIR_NAME

    @property
    def storage_path(self) -> Path:
        """Ruta final del archivo de preferencias."""
        return self._storage_path

    def load_favorites(self) -> List[int]:
        """Carga la lista de identificadores de cámaras favoritas."""
        if not self._storage_path.exists():
            return []

        try:
            data = json.loads(self._storage_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Preferencias corruptas, reiniciando archivo %s: %s", self._storage_path, exc)
            return []

        if not isinstance(data, list):
            logger.warning("Formato inesperado en archivo de favoritos, se ignora: %s", data)
            return []

        favorites: List[int] = []
        for item in data:
            try:
                favorites.append(int(item))
            except (TypeError, ValueError):
                logger.debug("Identificador no convertible a int en favoritos: %s", item)
                continue

        return favorites

    def save_favorites(self, favorites: Iterable[int]) -> None:
        """Persiste la lista de identificadores de cámaras favoritas."""
        ordered = sorted({int(camera_id) for camera_id in favorites})
        try:
            self._storage_path.write_text(json.dumps(ordered, ensure_ascii=True), encoding="utf-8")
        except OSError as exc:  # pragma: no cover - dependiente del sistema
            logger.error("No se pudo escribir favoritos en %s: %s", self._storage_path, exc)
            raise

    def clear(self) -> None:
        """Elimina el archivo de favoritos si existe."""
        try:
            if self._storage_path.exists():
                self._storage_path.unlink()
        except OSError as exc:
            logger.error("No se pudo eliminar el archivo de favoritos %s: %s", self._storage_path, exc)
            raise
