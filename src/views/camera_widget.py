"""
Widget para mostrar información de una cámara individual.

Este módulo define el widget que muestra la miniatura, nombre
y datos de una cámara de tráfico.
"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QPainter, QColor
import logging

from src.models.camera import Camera
import config


logger = logging.getLogger(__name__)


class CameraWidget(QWidget):
    """
    Widget personalizado para mostrar una cámara.
    """
    
    # Señales
    camera_clicked = Signal(int)  # camera_id
    image_reload_requested = Signal(int)  # camera_id
    
    def __init__(self, camera: Camera, parent=None):
        """
        Inicializa el widget de cámara.
        
        Args:
            camera: Objeto Camera a mostrar
            parent: Widget padre
        """
        super().__init__(parent)
        self.camera = camera
        self.current_pixmap = None
        
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
        self.image_label.setMinimumSize(QSize(300, 225))
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
