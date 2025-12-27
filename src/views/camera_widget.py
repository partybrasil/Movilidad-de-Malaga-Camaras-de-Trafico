"""
Widget para mostrar información de una cámara individual.

Este módulo define el widget que muestra la miniatura, nombre
y datos de una cámara de tráfico.
"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QDialog, QGroupBox, QComboBox,
    QMessageBox
)
from PySide6.QtCore import Qt, Signal, QSize, QTimer
from PySide6.QtGui import QPixmap, QPainter, QColor
import logging

from src.models.camera import Camera
import config

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:  # Solo para anotaciones de tipo, evita importaciones circulares en tiempo de ejecución
    from src.controllers.camera_controller import CameraController


logger = logging.getLogger(__name__)


class CameraWidget(QWidget):
    """
    Widget personalizado para mostrar una cámara.
    """
    
    # Señales
    camera_clicked = Signal(int)  # camera_id
    image_reload_requested = Signal(int)  # camera_id
    undock_requested = Signal(int)  # camera_id

    
    def __init__(self, camera: Camera, thumbnail_size: tuple = None, parent=None):
        """
        Inicializa el widget de cámara.
        
        Args:
            camera: Objeto Camera a mostrar
            thumbnail_size: Tupla (ancho, alto) para el tamaño de la miniatura
            parent: Widget padre
        """
        super().__init__(parent)
        self.camera = camera
        self.current_pixmap = None
        self.thumbnail_size = thumbnail_size or config.THUMBNAIL_SIZE
        
        self._setup_ui()
    
    def _setup_ui(self):
        """
        Configura la interfaz del widget.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        
        # Etiqueta de imagen
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        width, height = self.thumbnail_size
        self.image_label.setMinimumSize(QSize(width, height))
        self.image_label.setMaximumSize(QSize(width, height))
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                border: 2px solid #2c3e50;
                border-radius: 4px;
                color: white;
            }
        """)
        self.image_label.setText("Cargando imagen...")
        layout.addWidget(self.image_label)
        
        # Información de la cámara
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        # Nombre
        self.name_label = QLabel(self.camera.nombre)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        self.name_label.setWordWrap(True)
        info_layout.addWidget(self.name_label)
        
        # Dirección
        self.address_label = QLabel(self.camera.direccion)
        self.address_label.setWordWrap(True)
        self.address_label.setStyleSheet("color: gray;")
        info_layout.addWidget(self.address_label)
        
        # Distrito/Zona
        zona = self.camera.get_zona_from_direccion()
        self.zone_label = QLabel(f"📍 {zona}")
        self.zone_label.setStyleSheet("font-size: 9pt; color: #3498db;")
        info_layout.addWidget(self.zone_label)
        
        layout.addLayout(info_layout)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(4)
        
        # Botón refrescar
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setObjectName("secondary")
        self.refresh_btn.clicked.connect(self._on_refresh_clicked)
        buttons_layout.addWidget(self.refresh_btn)
        
        # Botón ver detalles
        self.details_btn = QPushButton("👁 Ver detalles")
        self.details_btn.clicked.connect(self._on_details_clicked)
        buttons_layout.addWidget(self.details_btn)
        
        # Botón desacoplar
        self.undock_btn = QPushButton("🔓 Desacoplar")
        self.undock_btn.clicked.connect(self._on_undock_clicked)
        self.undock_btn.setToolTip("Abrir en ventana independiente")
        buttons_layout.addWidget(self.undock_btn)
        
        layout.addLayout(buttons_layout)

        
        self.setLayout(layout)
        
        # Estilo del widget completo
        self.setStyleSheet("""
            CameraWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
            }
            CameraWidget:hover {
                border: 2px solid #3498db;
            }
        """)
    
    def set_image(self, pixmap: QPixmap):
        """
        Establece la imagen de la cámara.
        
        Args:
            pixmap: Imagen a mostrar
        """
        if pixmap and not pixmap.isNull():
            self.current_pixmap = pixmap
            # Escalar manteniendo aspecto
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("❌ Error cargando imagen")
    
    def set_loading(self):
        """
        Muestra estado de carga.
        """
        self.image_label.clear()
        self.image_label.setText("⏳ Cargando...")
    
    def set_error(self, error_msg: str = "Error"):
        """
        Muestra estado de error.
        
        Args:
            error_msg: Mensaje de error a mostrar
        """
        self.image_label.clear()
        self.image_label.setText(f"❌ {error_msg}")
    
    def _on_refresh_clicked(self):
        """
        Callback cuando se hace clic en refrescar.
        """
        self.set_loading()
        self.image_reload_requested.emit(self.camera.id)
    
    def _on_details_clicked(self):
        """
        Callback cuando se hace clic en ver detalles.
        """
        self.camera_clicked.emit(self.camera.id)
    
    def _on_undock_clicked(self):
        """
        Callback cuando se hace clic en desacoplar.
        """
        self.undock_requested.emit(self.camera.id)

    
    def resizeEvent(self, event):
        """
        Maneja el redimensionamiento del widget.
        """
        super().resizeEvent(event)
        
        # Reescalar imagen si existe
        if self.current_pixmap:
            scaled_pixmap = self.current_pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)


class CameraListItem(QWidget):
    """
    Widget compacto para lista de cámaras.
    """
    
    # Señales
    camera_clicked = Signal(int)  # camera_id
    undock_requested = Signal(int)  # camera_id

    
    def __init__(self, camera: Camera, parent=None):
        """
        Inicializa el item de lista.
        
        Args:
            camera: Objeto Camera a mostrar
            parent: Widget padre
        """
        super().__init__(parent)
        self.camera = camera
        
        self._setup_ui()
    
    def _setup_ui(self):
        """
        Configura la interfaz del item.
        """
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Thumbnail pequeño
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(80, 60)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_label.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                border-radius: 3px;
                color: white;
            }
        """)
        self.thumbnail_label.setText("📷")
        layout.addWidget(self.thumbnail_label)
        
        # Información
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        self.name_label = QLabel(self.camera.nombre)
        self.name_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(self.name_label)
        
        self.address_label = QLabel(self.camera.direccion)
        self.address_label.setStyleSheet("color: gray; font-size: 9pt;")
        info_layout.addWidget(self.address_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Botón desacoplar compacto
        self.undock_btn = QPushButton("🔓")
        self.undock_btn.setFixedSize(34, 34)
        self.undock_btn.setToolTip("Desacoplar cámara")
        self.undock_btn.clicked.connect(self._on_undock_clicked)
        layout.addWidget(self.undock_btn)

        
        self.setLayout(layout)
        
        # Hacer clickeable
        self.setCursor(Qt.PointingHandCursor)
    
    def set_thumbnail(self, pixmap: QPixmap):
        """
        Establece la miniatura.
        
        Args:
            pixmap: Imagen miniatura
        """
        if pixmap and not pixmap.isNull():
            scaled = pixmap.scaled(
                self.thumbnail_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.thumbnail_label.setPixmap(scaled)
    
    def mousePressEvent(self, event):
        """
        Maneja el clic en el item.
        """
        if event.button() == Qt.LeftButton:
            self.camera_clicked.emit(self.camera.id)
    
    def _on_undock_clicked(self):
        """
        Callback para desacoplar desde la lista.
        """
        self.undock_requested.emit(self.camera.id)



class CameraDetailDialog(QDialog):
    """
    Diálogo para mostrar una cámara individual con controles.
    """
    
    # Señales
    image_reload_requested = Signal()
    undock_requested = Signal(int)

    
    def __init__(self, camera: Camera, image_loader, controller: "CameraController", parent=None):
        """
        Inicializa el diálogo de detalle.
        
        Args:
            camera: Objeto Camera a mostrar
            image_loader: Instancia de ImageLoader para cargar imágenes
            controller: Controlador principal para gestionar favoritos
            parent: Widget padre
        """
        super().__init__(parent)
        self.camera = camera
        self.image_loader = image_loader
        self.controller = controller
        self.current_pixmap = None
        self.is_paused = False
        self.auto_refresh_timer = QTimer()
        self.current_refresh_interval = config.IMAGE_REFRESH_INTERVAL  # Guardar intervalo actual
        self.is_favorite = self.controller.is_favorite(self.camera.id)
        self.favorite_btn: Optional[QPushButton] = None
        
        self._setup_ui()
        self._connect_signals()
        
        # Cargar imagen inicial
        self._load_image()
        
        # Iniciar auto-refresh por defecto
        self.auto_refresh_timer.timeout.connect(self._auto_refresh)
        self.auto_refresh_timer.start(self.current_refresh_interval * 1000)
    
    def _setup_ui(self):
        """
        Configura la interfaz del diálogo.
        """
        self.setWindowTitle(f"Cámara - {self.camera.nombre}")
        self.setMinimumSize(800, 700)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Información de la cámara
        info_group = QGroupBox("📍 Información")
        info_layout = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        self.name_label = QLabel(f"<b>{self.camera.nombre}</b>")
        self.name_label.setWordWrap(True)
        header_layout.addWidget(self.name_label, stretch=1)

        self.favorite_btn = QPushButton()
        self.favorite_btn.setCheckable(True)
        self.favorite_btn.setFlat(True)
        self.favorite_btn.setCursor(Qt.PointingHandCursor)
        self.favorite_btn.setFixedSize(34, 34)
        self.favorite_btn.clicked.connect(self._on_favorite_clicked)
        header_layout.addWidget(self.favorite_btn)
        info_layout.addLayout(header_layout)
        self._update_favorite_button()
        
        self.address_label = QLabel(f"Dirección: {self.camera.direccion}")
        self.address_label.setWordWrap(True)
        info_layout.addWidget(self.address_label)
        
        zona = self.camera.get_zona_from_direccion()
        self.zone_label = QLabel(f"Zona: {zona}")
        info_layout.addWidget(self.zone_label)
        
        if self.camera.coordenadas:
            x, y = self.camera.coordenadas
            self.coords_label = QLabel(f"Coordenadas: X={x:.2f}, Y={y:.2f}")
            info_layout.addWidget(self.coords_label)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Imagen de la cámara
        image_group = QGroupBox("📹 Vista en Tiempo Real")
        image_layout = QVBoxLayout()
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(QSize(640, 480))
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                border: 2px solid #2c3e50;
                border-radius: 4px;
                color: white;
            }
        """)
        self.image_label.setText("⏳ Cargando imagen...")
        image_layout.addWidget(self.image_label)
        
        # Estado de actualización
        self.status_label = QLabel("Estado: Cargando...")
        self.status_label.setStyleSheet("color: gray; font-size: 9pt;")
        self.status_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.status_label)
        
        image_group.setLayout(image_layout)
        layout.addWidget(image_group, stretch=1)
        
        # Controles
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # Botón actualizar manualmente
        self.refresh_btn = QPushButton("🔄 Actualizar Ahora")
        self.refresh_btn.clicked.connect(self._manual_refresh)
        controls_layout.addWidget(self.refresh_btn)
        
        # Botón pausar/reanudar
        self.pause_btn = QPushButton("⏸ Pausar Auto-refresh")
        self.pause_btn.setCheckable(True)
        self.pause_btn.clicked.connect(self._toggle_pause)
        controls_layout.addWidget(self.pause_btn)
        
        # Selector de intervalo de actualización
        interval_label = QLabel("⏱ Intervalo:")
        controls_layout.addWidget(interval_label)
        
        self.interval_combo = QComboBox()
        self.interval_combo.addItem("1 segundo", 1)
        self.interval_combo.addItem("3 segundos", 3)
        self.interval_combo.addItem("5 segundos", 5)
        self.interval_combo.addItem("10 segundos", 10)

        self.interval_combo.addItem("15 segundos", 15)
        self.interval_combo.addItem("30 segundos", 30)
        self.interval_combo.addItem("1 minuto", 60)
        self.interval_combo.addItem("2 minutos", 120)
        self.interval_combo.addItem("5 minutos", 300)
        
        # Seleccionar el intervalo por defecto
        default_index = self.interval_combo.findData(config.IMAGE_REFRESH_INTERVAL)
        if default_index >= 0:
            self.interval_combo.setCurrentIndex(default_index)
        else:
            self.interval_combo.setCurrentIndex(3)  # 30 segundos por defecto
        
        self.interval_combo.currentIndexChanged.connect(self._on_interval_changed)
        controls_layout.addWidget(self.interval_combo)
        
        # Botón guardar imagen
        self.save_btn = QPushButton("💾 Guardar Imagen")
        self.save_btn.clicked.connect(self._save_image)
        self.save_btn.setEnabled(False)
        controls_layout.addWidget(self.save_btn)
        
        # Botón abrir en navegador
        if self.camera.url:
            self.browser_btn = QPushButton("🌐 Ver en Web")
            self.browser_btn.clicked.connect(self._open_in_browser)
            controls_layout.addWidget(self.browser_btn)
        
        # Botón desacoplar
        self.undock_btn = QPushButton("🔓 Desacoplar")
        self.undock_btn.clicked.connect(self._on_undock_clicked)
        self.undock_btn.setToolTip("Abrir en ventana independiente")
        controls_layout.addWidget(self.undock_btn)
        
        layout.addLayout(controls_layout)

        
        # Botón cerrar
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_btn = QPushButton("✖ Cerrar")
        close_btn.setObjectName("secondary")
        close_btn.clicked.connect(self.close)
        close_layout.addWidget(close_btn)
        layout.addLayout(close_layout)
        
        self.setLayout(layout)
    
    def _connect_signals(self):
        """
        Conecta las señales del image loader.
        """
        self.image_loader.image_loaded.connect(self._on_image_loaded)
        self.image_loader.image_error.connect(self._on_image_error)
        self.controller.favorite_toggled.connect(self._on_favorite_toggled)

    def _update_favorite_button(self):
        """Actualiza el aspecto de la estrella de favoritos."""
        if not self.favorite_btn:
            return

        if self.is_favorite:
            self.favorite_btn.setText("★")
            self.favorite_btn.setChecked(True)
            self.favorite_btn.setStyleSheet(
                "font-size: 20pt; color: #f1c40f; border: none;"
            )
            self.favorite_btn.setToolTip("Quitar de favoritos")
        else:
            self.favorite_btn.setText("☆")
            self.favorite_btn.setChecked(False)
            self.favorite_btn.setStyleSheet(
                "font-size: 20pt; color: #f1c40f; border: none;"
            )
            self.favorite_btn.setToolTip("Marcar como favorita")

    def _on_favorite_clicked(self):
        """Alterna el estado de favorito de la cámara actual."""
        success, is_favorite, message = self.controller.toggle_favorite(self.camera.id)
        if not success:
            QMessageBox.warning(
                self,
                "Límite de favoritos",
                message or "No ha sido posible actualizar tus favoritos."
            )
            # Revertir estado visual al actual registrado
            self._update_favorite_button()
            return

        self.is_favorite = is_favorite
        self._update_favorite_button()

    def _on_favorite_toggled(self, camera_id: int, is_favorite: bool):
        """Sincroniza la estrella cuando el estado cambia desde otro componente."""
        if camera_id == self.camera.id:
            self.is_favorite = is_favorite
            self._update_favorite_button()
    
    def _load_image(self, force_reload=False):
        """
        Carga la imagen de la cámara.
        
        Args:
            force_reload: Si True, fuerza la recarga ignorando caché
        """
        if self.camera.url_imagen:
            self.status_label.setText("Estado: Cargando...")
            self.image_loader.load_image(self.camera.id, self.camera.url_imagen, force_reload)
    
    def _manual_refresh(self):
        """
        Actualiza la imagen manualmente.
        """
        logger.info(f"Actualización manual de cámara {self.camera.id}")
        self.image_label.setText("⏳ Actualizando...")
        self._load_image(force_reload=True)
    
    def _auto_refresh(self):
        """
        Actualización automática por timer.
        """
        if not self.is_paused:
            logger.debug(f"Auto-refresh de cámara {self.camera.id}")
            self._load_image(force_reload=True)
    
    def _toggle_pause(self, checked):
        """
        Pausa o reanuda el auto-refresh.
        
        Args:
            checked: Estado del botón
        """
        self.is_paused = checked
        
        if checked:
            self.pause_btn.setText("▶ Reanudar Auto-refresh")
            self.status_label.setText("Estado: Auto-refresh pausado")
            self.interval_combo.setEnabled(False)  # Deshabilitar selector cuando está pausado
            logger.info(f"Auto-refresh pausado para cámara {self.camera.id}")
        else:
            self.pause_btn.setText("⏸ Pausar Auto-refresh")
            self.status_label.setText("Estado: Auto-refresh activo")
            self.interval_combo.setEnabled(True)  # Habilitar selector cuando está activo
            logger.info(f"Auto-refresh reanudado para cámara {self.camera.id}")
            # Refrescar inmediatamente al reanudar
            self._load_image(force_reload=True)
    
    def _on_interval_changed(self, index):
        """
        Maneja el cambio de intervalo de actualización.
        
        Args:
            index: Índice seleccionado en el combo
        """
        new_interval = self.interval_combo.currentData()
        if new_interval and new_interval != self.current_refresh_interval:
            self.current_refresh_interval = new_interval
            
            # Reiniciar el timer con el nuevo intervalo
            if self.auto_refresh_timer.isActive():
                self.auto_refresh_timer.stop()
                self.auto_refresh_timer.start(self.current_refresh_interval * 1000)
            
            logger.info(f"Intervalo de auto-refresh cambiado a {new_interval} segundos para cámara {self.camera.id}")
            self.status_label.setText(f"Estado: Auto-refresh cada {self._format_interval(new_interval)}")
    
    def _format_interval(self, seconds):
        """
        Formatea el intervalo en segundos a un texto legible.
        
        Args:
            seconds: Segundos del intervalo
            
        Returns:
            String formateado (ej: "30s", "1m", "2m")
        """
        if seconds < 60:
            return f"{seconds}s"
        else:
            minutes = seconds // 60
            return f"{minutes}m"
    
    def _save_image(self):
        """
        Guarda la imagen actual en el disco.
        """
        if self.current_pixmap and not self.current_pixmap.isNull():
            from PySide6.QtWidgets import QFileDialog
            from datetime import datetime
            
            # Nombre de archivo sugerido
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            suggested_name = f"camara_{self.camera.id}_{timestamp}.jpg"
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Imagen",
                suggested_name,
                "Imágenes (*.jpg *.jpeg *.png)"
            )
            
            if file_path:
                if self.current_pixmap.save(file_path):
                    self.status_label.setText(f"Estado: Imagen guardada en {file_path}")
                    logger.info(f"Imagen guardada: {file_path}")
                else:
                    self.status_label.setText("Estado: Error al guardar imagen")
                    logger.error("Error al guardar imagen")
    
    def _open_in_browser(self):
        """
        Abre la URL de la cámara en el navegador web.
        """
        if self.camera.url:
            from PySide6.QtGui import QDesktopServices
            from PySide6.QtCore import QUrl
            QDesktopServices.openUrl(QUrl(self.camera.url))
            logger.info(f"Abriendo URL en navegador: {self.camera.url}")
    
    def _on_undock_clicked(self):
        """
        Callback cuando se hace clic en desacoplar.
        """
        self.undock_requested.emit(self.camera.id)
        # self.close() # Opcional: cerrar el diálogo al desacoplar

    
    def _on_image_loaded(self, camera_id: int, pixmap: QPixmap):
        """
        Callback cuando se carga la imagen.
        
        Args:
            camera_id: ID de la cámara
            pixmap: Imagen cargada
        """
        if camera_id == self.camera.id:
            if pixmap and not pixmap.isNull():
                self.current_pixmap = pixmap
                
                # Escalar manteniendo aspecto
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                
                from datetime import datetime
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                if self.is_paused:
                    self.status_label.setText(f"Estado: Pausado | Última actualización: {timestamp}")
                else:
                    interval_text = self._format_interval(self.current_refresh_interval)
                    self.status_label.setText(f"Estado: Activo (cada {interval_text}) | Última actualización: {timestamp}")
                
                self.save_btn.setEnabled(True)
                logger.debug(f"Imagen cargada para cámara {camera_id}")
    
    def _on_image_error(self, camera_id: int, error_msg: str):
        """
        Callback cuando falla la carga.
        
        Args:
            camera_id: ID de la cámara
            error_msg: Mensaje de error
        """
        if camera_id == self.camera.id:
            self.image_label.setText(f"❌ Error: {error_msg}")
            self.status_label.setText(f"Estado: Error - {error_msg}")
            self.save_btn.setEnabled(False)
            logger.error(f"Error cargando imagen cámara {camera_id}: {error_msg}")
    
    def resizeEvent(self, event):
        """
        Maneja el redimensionamiento del diálogo.
        """
        super().resizeEvent(event)
        
        # Reescalar imagen si existe
        if self.current_pixmap:
            scaled_pixmap = self.current_pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
    
    def closeEvent(self, event):
        """
        Maneja el cierre del diálogo.
        """
        # Detener el timer al cerrar
        self.auto_refresh_timer.stop()
        try:
            self.controller.favorite_toggled.disconnect(self._on_favorite_toggled)
        except TypeError:
            pass
        logger.info(f"Cerrando vista detalle de cámara {self.camera.id}")
        event.accept()
