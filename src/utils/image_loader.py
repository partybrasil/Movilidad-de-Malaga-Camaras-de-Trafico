"""
Módulo para cargar imágenes de las cámaras de forma asíncrona.

Este módulo gestiona la descarga y caché de imágenes de las cámaras
sin bloquear la interfaz gráfica.
"""

import requests
from PySide6.QtCore import QObject, QRunnable, Signal, QThreadPool
from PySide6.QtGui import QPixmap, QImage
from typing import Optional, Dict
import logging
from io import BytesIO

import config


logger = logging.getLogger(__name__)


class ImageLoaderSignals(QObject):
    """
    Señales para comunicar resultados de carga de imágenes.
    """
    finished = Signal(int, QPixmap)  # camera_id, imagen
    error = Signal(int, str)  # camera_id, mensaje de error


class ImageLoadTask(QRunnable):
    """
    Tarea para cargar una imagen en un hilo separado.
    """
    
    def __init__(self, camera_id: int, image_url: str):
        """
        Inicializa la tarea de carga.
        
        Args:
            camera_id: ID de la cámara
            image_url: URL de la imagen a cargar
        """
        super().__init__()
        self.camera_id = camera_id
        self.image_url = image_url
        self.signals = ImageLoaderSignals()
    
    def run(self):
        """
        Ejecuta la descarga de la imagen.
        """
        try:
            logger.debug(f"[Cámara {self.camera_id}] Iniciando descarga de imagen")
            logger.debug(f"[Cámara {self.camera_id}] URL: {self.image_url}")
            
            # Validar URL
            if not self.image_url or not self.image_url.strip():
                error_msg = "URL de imagen vacía"
                logger.error(f"[Cámara {self.camera_id}] {error_msg}")
                self.signals.error.emit(self.camera_id, error_msg)
                return
            
            # Descargar imagen
            logger.debug(f"[Cámara {self.camera_id}] Realizando petición HTTP...")
            
            # Headers completos para simular navegador
            headers = config.IMAGE_REQUEST_HEADERS if hasattr(config, 'IMAGE_REQUEST_HEADERS') else {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Referer': 'https://movilidad.malaga.eu/'
            }
            
            response = requests.get(
                self.image_url, 
                timeout=config.IMAGE_TIMEOUT,
                stream=True,
                headers=headers,
                allow_redirects=True
            )
            
            logger.debug(f"[Cámara {self.camera_id}] Status: {response.status_code}")
            logger.debug(f"[Cámara {self.camera_id}] Content-Type: {response.headers.get('content-type', 'N/A')}")
            logger.debug(f"[Cámara {self.camera_id}] Content-Length: {response.headers.get('content-length', 'N/A')}")
            
            response.raise_for_status()
            
            # Verificar que sea una imagen
            content_type = response.headers.get('content-type', '')
            logger.debug(f"[Cámara {self.camera_id}] Content-Type recibido: {content_type}")
            
            # Si no es una imagen, puede ser HTML (error del servidor)
            if 'text/html' in content_type.lower():
                error_msg = "Servidor devolvió HTML en lugar de imagen (posible bloqueo o error)"
                logger.error(f"[Cámara {self.camera_id}] {error_msg}")
                logger.debug(f"[Cámara {self.camera_id}] Contenido HTML: {content[:500].decode('utf-8', errors='ignore')}")
                self.signals.error.emit(self.camera_id, "Sin acceso")
                return
            
            if 'image' not in content_type.lower() and content_type:
                logger.warning(f"[Cámara {self.camera_id}] Content-Type no es imagen: {content_type}")
            
            # Obtener contenido
            content = response.content
            logger.debug(f"[Cámara {self.camera_id}] Descargados {len(content)} bytes")
            
            if len(content) == 0:
                error_msg = "Imagen vacía (0 bytes)"
                logger.error(f"[Cámara {self.camera_id}] {error_msg}")
                self.signals.error.emit(self.camera_id, error_msg)
                return
            
            # Convertir a QPixmap
            image_data = BytesIO(content)
            qimage = QImage()
            
            logger.debug(f"[Cámara {self.camera_id}] Cargando en QImage...")
            if qimage.loadFromData(image_data.getvalue()):
                logger.debug(f"[Cámara {self.camera_id}] QImage cargada: {qimage.width()}x{qimage.height()}")
                pixmap = QPixmap.fromImage(qimage)
                logger.info(f"[Cámara {self.camera_id}] ✓ Imagen cargada exitosamente")
                self.signals.finished.emit(self.camera_id, pixmap)
            else:
                error_msg = "QImage.loadFromData() falló"
                logger.error(f"[Cámara {self.camera_id}] {error_msg}")
                logger.debug(f"[Cámara {self.camera_id}] Primeros 100 bytes: {content[:100]}")
                self.signals.error.emit(self.camera_id, error_msg)
            
        except requests.Timeout as e:
            error_msg = f"Timeout ({config.IMAGE_TIMEOUT}s)"
            logger.warning(f"[Cámara {self.camera_id}] {error_msg}")
            self.signals.error.emit(self.camera_id, error_msg)
            
        except requests.RequestException as e:
            error_msg = f"Error HTTP: {str(e)}"
            logger.warning(f"[Cámara {self.camera_id}] {error_msg}")
            self.signals.error.emit(self.camera_id, error_msg)
            
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            logger.error(f"[Cámara {self.camera_id}] {error_msg}", exc_info=True)
            self.signals.error.emit(self.camera_id, error_msg)


class ImageLoader(QObject):
    """
    Gestor de carga de imágenes con caché y descarga asíncrona.
    """
    
    # Señales
    image_loaded = Signal(int, QPixmap)  # camera_id, imagen
    image_error = Signal(int, str)  # camera_id, error
    
    def __init__(self):
        """
        Inicializa el gestor de imágenes.
        """
        super().__init__()
        self.thread_pool = QThreadPool()
        self.cache: Dict[int, QPixmap] = {}
        self.max_cache_size = config.CACHE_MAX_SIZE if config.ENABLE_IMAGE_CACHE else 0
        
        logger.info(f"ImageLoader inicializado. Pool threads: {self.thread_pool.maxThreadCount()}")
    
    def load_image(self, camera_id: int, image_url: str, force_reload: bool = False):
        """
        Carga una imagen de forma asíncrona.
        
        Args:
            camera_id: ID de la cámara
            image_url: URL de la imagen
            force_reload: Si True, ignora la caché y recarga
        """
        logger.debug(f"load_image() llamado para cámara {camera_id}")
        logger.debug(f"  URL: {image_url}")
        logger.debug(f"  Force reload: {force_reload}")
        logger.debug(f"  En caché: {camera_id in self.cache}")
        
        # Verificar caché si no es recarga forzada
        if not force_reload and camera_id in self.cache:
            logger.debug(f"Imagen {camera_id} obtenida desde caché")
            self.image_loaded.emit(camera_id, self.cache[camera_id])
            return
        
        # Crear tarea de carga
        logger.debug(f"Creando ImageLoadTask para cámara {camera_id}")
        task = ImageLoadTask(camera_id, image_url)
        task.signals.finished.connect(self._on_image_loaded)
        task.signals.error.connect(self._on_image_error)
        
        # Ejecutar en el pool de threads
        logger.debug(f"Añadiendo tarea al thread pool (active: {self.thread_pool.activeThreadCount()})")
        self.thread_pool.start(task)
    
    def _on_image_loaded(self, camera_id: int, pixmap: QPixmap):
        """
        Callback cuando una imagen se carga correctamente.
        
        Args:
            camera_id: ID de la cámara
            pixmap: Imagen cargada
        """
        # Añadir a caché
        if self.max_cache_size > 0:
            if len(self.cache) >= self.max_cache_size:
                # Eliminar el primer elemento (FIFO simple)
                first_key = next(iter(self.cache))
                del self.cache[first_key]
            
            self.cache[camera_id] = pixmap
        
        # Emitir señal
        self.image_loaded.emit(camera_id, pixmap)
    
    def _on_image_error(self, camera_id: int, error_msg: str):
        """
        Callback cuando falla la carga de una imagen.
        
        Args:
            camera_id: ID de la cámara
            error_msg: Mensaje de error
        """
        self.image_error.emit(camera_id, error_msg)
    
    def clear_cache(self):
        """
        Limpia la caché de imágenes.
        """
        self.cache.clear()
        logger.info("Caché de imágenes limpiada")
    
    def get_cache_size(self) -> int:
        """
        Retorna el tamaño actual de la caché.
        
        Returns:
            Número de imágenes en caché
        """
        return len(self.cache)
