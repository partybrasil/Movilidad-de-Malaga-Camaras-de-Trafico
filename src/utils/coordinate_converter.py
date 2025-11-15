"""
Utilidades para conversión de coordenadas.

Este módulo maneja la conversión entre sistemas de coordenadas,
específicamente de EPSG:25830 (UTM zona 30N) a EPSG:4326 (WGS84 lat/lon).
"""

from typing import Optional, Tuple
from pyproj import Transformer
import logging

logger = logging.getLogger(__name__)


class CoordinateConverter:
    """
    Conversor de coordenadas entre diferentes sistemas.
    """
    
    def __init__(self, source_crs: str = "EPSG:25830", target_crs: str = "EPSG:4326"):
        """
        Inicializa el conversor de coordenadas.
        
        Args:
            source_crs: Sistema de coordenadas origen (por defecto EPSG:25830)
            target_crs: Sistema de coordenadas destino (por defecto EPSG:4326 - WGS84)
        """
        self.source_crs = source_crs
        self.target_crs = target_crs
        
        try:
            # Crear transformador
            # always_xy=True asegura que el orden sea (x, y) en lugar de (lat, lon)
            self.transformer = Transformer.from_crs(
                source_crs, 
                target_crs, 
                always_xy=True
            )
            logger.info(f"Conversor inicializado: {source_crs} → {target_crs}")
        except Exception as e:
            logger.error(f"Error inicializando conversor: {e}")
            self.transformer = None
    
    def convert(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        """
        Convierte coordenadas del sistema origen al destino.
        
        Args:
            x: Coordenada X en el sistema origen (Este en UTM)
            y: Coordenada Y en el sistema origen (Norte en UTM)
            
        Returns:
            Tupla (lon, lat) en WGS84 o None si hay error
        """
        if self.transformer is None:
            logger.error("Transformer no inicializado")
            return None
        
        try:
            # Transformar coordenadas
            # El resultado es (lon, lat) gracias a always_xy=True
            lon, lat = self.transformer.transform(x, y)
            return (lon, lat)
        except Exception as e:
            logger.error(f"Error convirtiendo coordenadas ({x}, {y}): {e}")
            return None
    
    def utm_to_latlon(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        """
        Convierte coordenadas UTM (EPSG:25830) a lat/lon (EPSG:4326).
        
        Args:
            x: Coordenada Este (UTM)
            y: Coordenada Norte (UTM)
            
        Returns:
            Tupla (lon, lat) en grados decimales o None si hay error
        """
        return self.convert(x, y)
    
    def is_valid_utm(self, x: float, y: float) -> bool:
        """
        Verifica si las coordenadas UTM son válidas para la zona 30N.
        
        Args:
            x: Coordenada Este
            y: Coordenada Norte
            
        Returns:
            True si las coordenadas parecen válidas
        """
        # Zona 30N: Este aproximadamente entre 166000-834000
        # Norte aproximadamente entre 0-9000000 (hemisferio norte)
        # Málaga está alrededor de x=370000-390000, y=4060000-4080000
        if x < 100000 or x > 900000:
            return False
        if y < 4000000 or y > 5000000:  # Rango razonable para sur de España
            return False
        return True


# Instancia global del conversor
_converter = None


def get_converter() -> CoordinateConverter:
    """
    Obtiene la instancia global del conversor.
    
    Returns:
        Instancia de CoordinateConverter
    """
    global _converter
    if _converter is None:
        _converter = CoordinateConverter()
    return _converter
