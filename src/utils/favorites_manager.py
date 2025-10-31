"""
Gestor de favoritos para las cámaras de tráfico.

Este módulo gestiona la persistencia de las cámaras favoritas del usuario.
"""

import json
import logging
from pathlib import Path
from typing import Set

import config


logger = logging.getLogger(__name__)


class FavoritesManager:
    """
    Gestiona el almacenamiento persistente de cámaras favoritas.
    """
    
    def __init__(self):
        """
        Inicializa el gestor de favoritos.
        """
        self.favorites_file = Path(config.FAVORITES_FILE)
        self.favorites: Set[int] = set()
        self._load_favorites()
    
    def _load_favorites(self):
        """
        Carga los favoritos desde el archivo JSON.
        """
        if self.favorites_file.exists():
            try:
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.favorites = set(data.get('favorites', []))
                    logger.info(f"Favoritos cargados: {len(self.favorites)} cámaras")
            except Exception as e:
                logger.error(f"Error al cargar favoritos: {e}")
                self.favorites = set()
        else:
            logger.info("No existe archivo de favoritos, iniciando con conjunto vacío")
    
    def _save_favorites(self):
        """
        Guarda los favoritos en el archivo JSON.
        """
        try:
            data = {'favorites': list(self.favorites)}
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Favoritos guardados: {len(self.favorites)} cámaras")
        except Exception as e:
            logger.error(f"Error al guardar favoritos: {e}")
    
    def add_favorite(self, camera_id: int) -> bool:
        """
        Añade una cámara a favoritos.
        
        Args:
            camera_id: ID de la cámara
            
        Returns:
            True si se añadió correctamente, False si se alcanzó el límite
        """
        if len(self.favorites) >= config.MAX_FAVORITES and camera_id not in self.favorites:
            logger.warning(f"Límite de favoritos alcanzado ({config.MAX_FAVORITES})")
            return False
        
        self.favorites.add(camera_id)
        self._save_favorites()
        logger.info(f"Cámara {camera_id} añadida a favoritos")
        return True
    
    def remove_favorite(self, camera_id: int):
        """
        Elimina una cámara de favoritos.
        
        Args:
            camera_id: ID de la cámara
        """
        if camera_id in self.favorites:
            self.favorites.discard(camera_id)
            self._save_favorites()
            logger.info(f"Cámara {camera_id} eliminada de favoritos")
    
    def is_favorite(self, camera_id: int) -> bool:
        """
        Verifica si una cámara es favorita.
        
        Args:
            camera_id: ID de la cámara
            
        Returns:
            True si es favorita
        """
        return camera_id in self.favorites
    
    def get_favorites(self) -> Set[int]:
        """
        Retorna el conjunto de IDs favoritos.
        
        Returns:
            Conjunto de IDs de cámaras favoritas
        """
        return self.favorites.copy()
    
    def get_favorites_count(self) -> int:
        """
        Retorna el número de favoritos actuales.
        
        Returns:
            Número de favoritos
        """
        return len(self.favorites)
    
    def can_add_more(self) -> bool:
        """
        Verifica si se pueden añadir más favoritos.
        
        Returns:
            True si se puede añadir más
        """
        return len(self.favorites) < config.MAX_FAVORITES
