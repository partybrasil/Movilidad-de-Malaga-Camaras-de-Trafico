"""
Modelo de datos para las cámaras de tráfico.

Este módulo define la clase Camera que representa una cámara de tráfico
con toda su información asociada.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import re


@dataclass
class Camera:
    """
    Representa una cámara de tráfico de Málaga.
    
    Atributos:
        id: Identificador único de la cámara
        nombre: Nombre técnico de la cámara (ej: TV103-A-...)
        direccion: Descripción de la ubicación
        url_imagen: URL de la imagen en tiempo real
        url: URL de la web oficial de la cámara
        coordenadas: Tupla (x, y) con las coordenadas
        geometry_raw: String original del campo ukb_geometry
        acceso: Información de accesibilidad (PMR, etc)
        distrito: ID del distrito (si está disponible)
    """
    
    id: int
    nombre: str
    direccion: str
    url_imagen: str
    url: str
    coordenadas: Optional[Tuple[float, float]] = None
    geometry_raw: Optional[str] = None
    acceso: Optional[str] = None
    distrito: Optional[str] = None
    
    def __post_init__(self):
        """Procesa los datos después de la inicialización."""
        # Parsear coordenadas desde geometry_raw si existe
        if self.geometry_raw and not self.coordenadas:
            self.coordenadas = self._parse_geometry(self.geometry_raw)
    
    @staticmethod
    def _parse_geometry(geometry_str: str) -> Optional[Tuple[float, float]]:
        """
        Parsea el string de geometría POINT(x y) a tupla de coordenadas.
        
        Args:
            geometry_str: String en formato "POINT (x y)"
            
        Returns:
            Tupla (x, y) o None si no se puede parsear
        """
        if not geometry_str:
            return None
            
        # Patrón para extraer coordenadas de "POINT (x y)"
        pattern = r'POINT\s*\(\s*([-\d.]+)\s+([-\d.]+)\s*\)'
        match = re.search(pattern, geometry_str, re.IGNORECASE)
        
        if match:
            try:
                x = float(match.group(1))
                y = float(match.group(2))
                return (x, y)
            except ValueError:
                return None
        
        return None
    
    def get_distrito_display(self) -> str:
        """
        Retorna el distrito para mostrar en la UI.
        
        Returns:
            String con el distrito o "Sin distrito" si no está definido
        """
        if self.distrito and self.distrito.strip():
            return f"Distrito {self.distrito}"
        return "Sin distrito"
    
    def get_zona_from_direccion(self) -> str:
        """
        Extrae una zona/barrio aproximado desde la dirección.
        Útil para agrupar cuando no hay campo distrito.
        
        Returns:
            String con la zona extraída
        """
        if not self.direccion:
            return "Sin zona"
        
        # Buscar nombres de calles/avenidas principales
        direccion_upper = self.direccion.upper()
        
        # Patrones comunes de zonas
        zonas_conocidas = {
            "ALAMEDA": "Centro - Alameda",
            "LARIOS": "Centro",
            "MALAGUETA": "Malagueta",
            "PEDREGALEJOS": "Pedregalejo",
            "CARRETERA DE CADIZ": "Carretera de Cádiz",
            "PASEO MARITIMO": "Paseo Marítimo",
            "TEATINOS": "Teatinos",
            "CRUZ DE HUMILLADERO": "Cruz de Humilladero",
            "CAMPANILLAS": "Campanillas",
            "PUERTO": "Puerto",
            "CENTRO": "Centro",
            "ANDALUCIA": "Zona Andalucía",
        }
        
        for patron, zona in zonas_conocidas.items():
            if patron in direccion_upper:
                return zona
        
        # Si no coincide, retornar primeras palabras de la dirección
        palabras = self.direccion.split()[:3]
        return " ".join(palabras) if palabras else "Otra zona"
    
    def __str__(self) -> str:
        """Representación en string de la cámara."""
        return f"{self.nombre} - {self.direccion}"
    
    def __repr__(self) -> str:
        """Representación técnica de la cámara."""
        return (f"Camera(id={self.id}, nombre='{self.nombre}', "
                f"direccion='{self.direccion}')")
