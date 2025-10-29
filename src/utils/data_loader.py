"""
Módulo para cargar y procesar datos del CSV de cámaras de tráfico.

Este módulo se encarga de descargar, parsear y convertir los datos
del CSV oficial en objetos Camera.
"""

import pandas as pd
import requests
from typing import List, Optional
import logging
from io import StringIO

from src.models.camera import Camera
import config


logger = logging.getLogger(__name__)


class DataLoader:
    """
    Clase para cargar datos de cámaras desde el CSV oficial.
    """
    
    def __init__(self, csv_url: str = config.CSV_URL):
        """
        Inicializa el cargador de datos.
        
        Args:
            csv_url: URL del CSV a descargar
        """
        self.csv_url = csv_url
        self.dataframe: Optional[pd.DataFrame] = None
        self.cameras: List[Camera] = []
    
    def load_data(self) -> bool:
        """
        Descarga y carga los datos del CSV.
        
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        try:
            logger.info("=" * 80)
            logger.info(f"INICIANDO DESCARGA DE DATOS")
            logger.info(f"URL: {self.csv_url}")
            logger.info("=" * 80)
            
            # Descargar CSV
            logger.debug("Realizando petición HTTP GET...")
            response = requests.get(self.csv_url, timeout=30)
            logger.debug(f"Status Code: {response.status_code}")
            logger.debug(f"Headers: {dict(response.headers)}")
            
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            logger.debug(f"Tamaño respuesta: {len(response.text)} caracteres")
            logger.debug(f"Primeras 200 caracteres: {response.text[:200]}")
            
            # Leer CSV con pandas
            csv_data = StringIO(response.text)
            self.dataframe = pd.read_csv(csv_data, encoding='utf-8')
            
            logger.info(f"✓ CSV cargado correctamente: {len(self.dataframe)} registros")
            logger.debug(f"Columnas disponibles: {list(self.dataframe.columns)}")
            
            # Mostrar muestra de datos
            if len(self.dataframe) > 0:
                logger.debug("Primera fila del CSV:")
                logger.debug(f"{self.dataframe.iloc[0].to_dict()}")
            
            # Convertir a objetos Camera
            self._parse_cameras()
            
            logger.info("=" * 80)
            return True
            
        except requests.RequestException as e:
            logger.error(f"✗ Error descargando CSV: {e}", exc_info=True)
            return False
        except pd.errors.ParserError as e:
            logger.error(f"✗ Error parseando CSV: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"✗ Error inesperado cargando datos: {e}", exc_info=True)
            return False
    
    def _parse_cameras(self):
        """
        Convierte el DataFrame en lista de objetos Camera.
        """
        if self.dataframe is None:
            logger.warning("DataFrame es None, no se pueden parsear cámaras")
            return
        
        self.cameras = []
        cols = config.CSV_COLUMNS
        
        logger.info(f"Iniciando parseo de {len(self.dataframe)} filas...")
        logger.debug(f"Configuración de columnas: {cols}")
        
        cameras_con_imagen = 0
        cameras_sin_imagen = 0
        
        for idx, row in self.dataframe.iterrows():
            try:
                # Obtener valores con valores por defecto si no existen
                nombre = self._get_value(row, cols["nombre"], f"Cámara {idx}")
                direccion = self._get_value(row, cols["direccion"], "Sin dirección")
                url_imagen = self._get_value(row, cols["url_imagen"], "")
                url = self._get_value(row, cols["url"], "")
                geometry = self._get_value(row, cols["geometry"], None)
                acceso = self._get_value(row, cols["acceso"], None)
                distrito = self._get_value(row, cols["distrito"], None)
                
                # Log detallado de las primeras 3 cámaras
                if idx < 3:
                    logger.debug(f"\n--- Cámara {idx} ---")
                    logger.debug(f"  Nombre: {nombre}")
                    logger.debug(f"  Dirección: {direccion}")
                    logger.debug(f"  URL Imagen: {url_imagen}")
                    logger.debug(f"  URL Web: {url}")
                    logger.debug(f"  Geometry: {geometry}")
                
                # Verificar URL de imagen
                if url_imagen and url_imagen.strip():
                    cameras_con_imagen += 1
                else:
                    cameras_sin_imagen += 1
                    logger.warning(f"Cámara {idx} ({nombre}) NO tiene URL de imagen")
                
                # Crear objeto Camera
                camera = Camera(
                    id=idx,
                    nombre=nombre,
                    direccion=direccion,
                    url_imagen=url_imagen,
                    url=url,
                    geometry_raw=geometry,
                    acceso=acceso,
                    distrito=distrito
                )
                
                self.cameras.append(camera)
                
            except Exception as e:
                logger.error(f"Error procesando fila {idx}: {e}", exc_info=True)
                continue
        
        logger.info(f"✓ Procesadas {len(self.cameras)} cámaras correctamente")
        logger.info(f"  - Con imagen: {cameras_con_imagen}")
        logger.info(f"  - Sin imagen: {cameras_sin_imagen}")
    
    @staticmethod
    def _get_value(row: pd.Series, column: str, default=None):
        """
        Obtiene un valor de una fila del DataFrame de forma segura.
        
        Args:
            row: Fila del DataFrame
            column: Nombre de la columna
            default: Valor por defecto si no existe o es NaN
            
        Returns:
            Valor de la columna o valor por defecto
        """
        if column not in row.index:
            return default
        
        value = row[column]
        
        # Manejar valores NaN
        if pd.isna(value):
            return default
        
        return value
    
    def get_cameras(self) -> List[Camera]:
        """
        Retorna la lista de cámaras cargadas.
        
        Returns:
            Lista de objetos Camera
        """
        return self.cameras
    
    def get_cameras_by_distrito(self, distrito: str) -> List[Camera]:
        """
        Filtra cámaras por distrito.
        
        Args:
            distrito: ID del distrito a filtrar
            
        Returns:
            Lista de cámaras del distrito especificado
        """
        return [cam for cam in self.cameras if cam.distrito == distrito]
    
    def get_distritos(self) -> List[str]:
        """
        Obtiene lista única de distritos.
        
        Returns:
            Lista de IDs de distritos únicos
        """
        distritos = set()
        for cam in self.cameras:
            if cam.distrito:
                distritos.add(cam.distrito)
        return sorted(list(distritos))
    
    def get_zonas(self) -> List[str]:
        """
        Obtiene lista de zonas extraídas de las direcciones.
        Útil cuando no hay campo distrito.
        
        Returns:
            Lista de zonas únicas
        """
        zonas = set()
        for cam in self.cameras:
            zona = cam.get_zona_from_direccion()
            zonas.add(zona)
        return sorted(list(zonas))
    
    def search_cameras(self, query: str) -> List[Camera]:
        """
        Busca cámaras por nombre o dirección.
        
        Args:
            query: Texto a buscar
            
        Returns:
            Lista de cámaras que coinciden con la búsqueda
        """
        query_lower = query.lower()
        return [
            cam for cam in self.cameras
            if query_lower in cam.nombre.lower() or 
               query_lower in cam.direccion.lower()
        ]
