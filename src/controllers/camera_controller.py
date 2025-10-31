"""
Controlador principal de la aplicación.

Este módulo gestiona la lógica de negocio y coordina entre
el modelo de datos y las vistas.
"""

from PySide6.QtCore import QObject, Signal, QTimer
from typing import List, Optional, Set, Tuple
import logging

from src.models.camera import Camera
from src.utils.data_loader import DataLoader
from src.utils.image_loader import ImageLoader
from src.utils.preferences import FavoritesManager
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
    refresh_progress = Signal(int, int)  # (actual, total) para progreso de actualización
    favorites_updated = Signal(list)  # Lista de IDs favoritas
    favorite_toggled = Signal(int, bool)  # camera_id, estado final
    
    def __init__(self):
        """
        Inicializa el controlador.
        """
        super().__init__()
        
        self.data_loader = DataLoader()
        self.image_loader = ImageLoader()
        try:
            self.favorites_manager: Optional[FavoritesManager] = FavoritesManager()
        except OSError:
            logger.exception("No fue posible inicializar el almacenamiento de favoritos; se usará modo volátil")
            self.favorites_manager = None
        
        self.all_cameras: List[Camera] = []
        self.filtered_cameras: List[Camera] = []
        self.selected_cameras: List[int] = []  # IDs de cámaras seleccionadas
        self.favorite_camera_ids: Set[int] = set()
        
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
            self._initialize_favorites()
            
            self.loading_progress.emit(
                f"Cargadas {len(self.all_cameras)} cámaras correctamente"
            )
            
            logger.info(f"Datos cargados: {len(self.all_cameras)} cámaras")
        else:
            self.loading_progress.emit("Error al cargar datos")
            logger.error("Fallo en la carga de datos")
        
        self.data_loaded.emit(success)
        self.cameras_updated.emit(self.filtered_cameras)
        self.favorites_updated.emit(self.get_favorite_ids())
    
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
        total_cameras = len(self.filtered_cameras)
        logger.info(f"Refrescando {total_cameras} imágenes...")
        self.image_loader.clear_cache()
        
        for index, camera in enumerate(self.filtered_cameras, start=1):
            self.load_camera_image(camera, force_reload=True)
            # Emitir progreso
            self.refresh_progress.emit(index, total_cameras)
            logger.debug(f"Actualizando cámara {index}/{total_cameras}")
    
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

    # ------------------------------------------------------------------
    # Gestión de favoritos
    # ------------------------------------------------------------------

    def _initialize_favorites(self) -> None:
        """Carga favoritos persistidos y los sincroniza con los datos actuales."""
        stored_ids: List[int] = []
        if self.favorites_manager:
            try:
                stored_ids = self.favorites_manager.load_favorites()
            except OSError:
                logger.exception("No fue posible cargar favoritos persistidos")

        available_ids = {camera.id for camera in self.all_cameras}
        self.favorite_camera_ids = {
            camera_id for camera_id in stored_ids if camera_id in available_ids
        }

        if self.favorites_manager and len(self.favorite_camera_ids) != len(stored_ids):
            # Persistimos limpiar IDs que ya no existen
            self._persist_favorites()

    def get_favorite_ids(self) -> List[int]:
        """Retorna los IDs de cámaras favoritas ordenados."""
        return sorted(self.favorite_camera_ids)

    def get_favorite_cameras(self) -> List[Camera]:
        """Obtiene los objetos Camera marcados como favoritos."""
        favorite_map = {camera.id: camera for camera in self.all_cameras}
        return [favorite_map[camera_id] for camera_id in self.get_favorite_ids() if camera_id in favorite_map]

    def is_favorite(self, camera_id: int) -> bool:
        """Indica si una cámara está marcada como favorita."""
        return camera_id in self.favorite_camera_ids

    def can_add_favorite(self) -> bool:
        """Verifica si se puede añadir una nueva cámara favorita."""
        return len(self.favorite_camera_ids) < config.MAX_FAVORITES

    def add_favorite(self, camera_id: int) -> Tuple[bool, Optional[str]]:
        """Marca una cámara como favorita respetando el límite configurado."""
        if camera_id in self.favorite_camera_ids:
            return True, None

        if not self.can_add_favorite():
            message = (
                f"Solo puedes guardar {config.MAX_FAVORITES} favoritas. "
                "Desmarca una para añadir otra."
            )
            return False, message

        if not any(camera.id == camera_id for camera in self.all_cameras):
            return False, "La cámara seleccionada ya no está disponible."

        self.favorite_camera_ids.add(camera_id)
        self._persist_favorites()
        self.favorites_updated.emit(self.get_favorite_ids())
        self.favorite_toggled.emit(camera_id, True)
        logger.info("Cámara %s añadida a favoritos", camera_id)
        return True, None

    def remove_favorite(self, camera_id: int) -> None:
        """Elimina una cámara de la lista de favoritas."""
        if camera_id in self.favorite_camera_ids:
            self.favorite_camera_ids.remove(camera_id)
            self._persist_favorites()
            self.favorites_updated.emit(self.get_favorite_ids())
            self.favorite_toggled.emit(camera_id, False)
            logger.info("Cámara %s eliminada de favoritos", camera_id)

    def toggle_favorite(self, camera_id: int) -> Tuple[bool, bool, Optional[str]]:
        """Alterna el estado de favorito de una cámara."""
        if self.is_favorite(camera_id):
            self.remove_favorite(camera_id)
            return True, False, None

        success, message = self.add_favorite(camera_id)
        return success, success, message

    def _persist_favorites(self) -> None:
        """Guarda la lista de favoritos en el almacenamiento persistente."""
        if not self.favorites_manager:
            return

        try:
            self.favorites_manager.save_favorites(self.favorite_camera_ids)
        except OSError:
            logger.exception("No fue posible guardar los favoritos en disco")
