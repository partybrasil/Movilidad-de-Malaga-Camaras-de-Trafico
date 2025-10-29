"""
Controlador principal de la aplicación.

Este módulo gestiona la lógica de negocio y coordina entre
el modelo de datos y las vistas.
"""

from PySide6.QtCore import QObject, Signal, QTimer
from typing import List, Optional
import logging

from src.models.camera import Camera
from src.utils.data_loader import DataLoader
from src.utils.image_loader import ImageLoader
import config


logger = logging.getLogger(__name__)


class CameraController(QObject):
    """
    Controlador principal para gestionar cámaras de tráfico.
    """
    
    # Señales
    data_loaded = Signal(bool)  # True si carga exitosa
    cameras_updated = Signal(list)  # Lista de cámaras a mostrar
    loading_progress = Signal(str)  # Mensaje de progreso
    
    def __init__(self):
        """
        Inicializa el controlador.
        """
        super().__init__()
        
        self.data_loader = DataLoader()
        self.image_loader = ImageLoader()
        
        self.all_cameras: List[Camera] = []
        self.filtered_cameras: List[Camera] = []
        self.selected_cameras: List[int] = []  # IDs de cámaras seleccionadas
        
        # Timer para actualización automática
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self._auto_refresh_images)
        
        logger.info("CameraController inicializado")
    
    def load_initial_data(self):
        """
        Carga los datos iniciales desde el CSV.
        """
        self.loading_progress.emit("Descargando datos de cámaras...")
        
        success = self.data_loader.load_data()
        
        if success:
            self.all_cameras = self.data_loader.get_cameras()
            self.filtered_cameras = self.all_cameras.copy()
            
            self.loading_progress.emit(
                f"Cargadas {len(self.all_cameras)} cámaras correctamente"
            )
            
            logger.info(f"Datos cargados: {len(self.all_cameras)} cámaras")
        else:
            self.loading_progress.emit("Error al cargar datos")
            logger.error("Fallo en la carga de datos")
        
        self.data_loaded.emit(success)
        self.cameras_updated.emit(self.filtered_cameras)
    
    def get_all_cameras(self) -> List[Camera]:
        """
        Retorna todas las cámaras cargadas.
        
        Returns:
            Lista completa de cámaras
        """
        return self.all_cameras
    
    def get_filtered_cameras(self) -> List[Camera]:
        """
        Retorna las cámaras actualmente filtradas.
        
        Returns:
            Lista de cámaras filtradas
        """
        return self.filtered_cameras
    
    def search_cameras(self, query: str):
        """
        Busca cámaras por texto.
        
        Args:
            query: Texto a buscar en nombre y dirección
        """
        if not query.strip():
            self.filtered_cameras = self.all_cameras.copy()
        else:
            self.filtered_cameras = self.data_loader.search_cameras(query)
        
        self.cameras_updated.emit(self.filtered_cameras)
        logger.info(f"Búsqueda '{query}': {len(self.filtered_cameras)} resultados")
    
    def filter_by_distrito(self, distrito: Optional[str]):
        """
        Filtra cámaras por distrito.
        
        Args:
            distrito: ID del distrito o None para mostrar todas
        """
        if distrito is None or distrito == "Todos":
            self.filtered_cameras = self.all_cameras.copy()
        else:
            self.filtered_cameras = self.data_loader.get_cameras_by_distrito(distrito)
        
        self.cameras_updated.emit(self.filtered_cameras)
        logger.info(f"Filtro distrito '{distrito}': {len(self.filtered_cameras)} cámaras")
    
    def filter_by_zona(self, zona: Optional[str]):
        """
        Filtra cámaras por zona extraída de la dirección.
        
        Args:
            zona: Nombre de la zona o None para mostrar todas
        """
        if zona is None or zona == "Todas":
            self.filtered_cameras = self.all_cameras.copy()
        else:
            self.filtered_cameras = [
                cam for cam in self.all_cameras
                if cam.get_zona_from_direccion() == zona
            ]
        
        self.cameras_updated.emit(self.filtered_cameras)
        logger.info(f"Filtro zona '{zona}': {len(self.filtered_cameras)} cámaras")
    
    def get_distritos(self) -> List[str]:
        """
        Obtiene lista de distritos disponibles.
        
        Returns:
            Lista de IDs de distritos
        """
        return self.data_loader.get_distritos()
    
    def get_zonas(self) -> List[str]:
        """
        Obtiene lista de zonas disponibles.
        
        Returns:
            Lista de nombres de zonas
        """
        return self.data_loader.get_zonas()
    
    def load_camera_image(self, camera: Camera, force_reload: bool = False):
        """
        Carga la imagen de una cámara.
        
        Args:
            camera: Objeto Camera
            force_reload: Si True, ignora caché y recarga
        """
        if camera.url_imagen:
            self.image_loader.load_image(camera.id, camera.url_imagen, force_reload)
    
    def start_auto_refresh(self, interval_seconds: int = None):
        """
        Inicia la actualización automática de imágenes.
        
        Args:
            interval_seconds: Intervalo en segundos (usa config por defecto si None)
        """
        if interval_seconds is None:
            interval_seconds = config.IMAGE_REFRESH_INTERVAL
        
        self.auto_refresh_timer.start(interval_seconds * 1000)
        logger.info(f"Auto-refresco iniciado: cada {interval_seconds}s")
    
    def stop_auto_refresh(self):
        """
        Detiene la actualización automática de imágenes.
        """
        self.auto_refresh_timer.stop()
        logger.info("Auto-refresco detenido")
    
    def _auto_refresh_images(self):
        """
        Callback para refrescar imágenes automáticamente.
        """
        logger.debug("Refrescando imágenes automáticamente...")
        # Recargar imágenes de cámaras visibles
        for camera in self.filtered_cameras[:10]:  # Limitar a 10 por rendimiento
            self.load_camera_image(camera, force_reload=True)
    
    def refresh_all_images(self):
        """
        Refresca todas las imágenes de las cámaras filtradas.
        """
        logger.info(f"Refrescando {len(self.filtered_cameras)} imágenes...")
        self.image_loader.clear_cache()
        
        for camera in self.filtered_cameras:
            self.load_camera_image(camera, force_reload=True)
    
    def select_camera(self, camera_id: int):
        """
        Marca una cámara como seleccionada.
        
        Args:
            camera_id: ID de la cámara
        """
        if camera_id not in self.selected_cameras:
            self.selected_cameras.append(camera_id)
    
    def deselect_camera(self, camera_id: int):
        """
        Desmarca una cámara seleccionada.
        
        Args:
            camera_id: ID de la cámara
        """
        if camera_id in self.selected_cameras:
            self.selected_cameras.remove(camera_id)
    
    def clear_selection(self):
        """
        Limpia la selección de cámaras.
        """
        self.selected_cameras.clear()
    
    def get_selected_cameras(self) -> List[Camera]:
        """
        Obtiene las cámaras actualmente seleccionadas.
        
        Returns:
            Lista de objetos Camera seleccionados
        """
        return [
            cam for cam in self.all_cameras
            if cam.id in self.selected_cameras
        ]
