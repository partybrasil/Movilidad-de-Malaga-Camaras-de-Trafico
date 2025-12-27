"""
Ventana flotante independiente para mostrar una cámara de tráfico.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, 
    QMenu, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer, QPoint, QSize
from PySide6.QtGui import QPixmap, QAction, QContextMenuEvent
import logging
from datetime import datetime

from src.models.camera import Camera
import config

logger = logging.getLogger(__name__)

class FloatingCameraWindow(QMainWindow):
    """
    Ventana flotante y redimensionable para una cámara individual.
    """
    
    closed = Signal(int)  # camera_id
    
    def __init__(self, camera: Camera, image_loader, parent=None):
        super().__init__(parent)
        self.camera = camera
        self.image_loader = image_loader
        self.current_pixmap = None
        self.refresh_timer = QTimer(self)
        self.current_interval = config.IMAGE_REFRESH_INTERVAL
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._setup_ui()
        self._connect_signals()
        
        # Cargar imagen inicial e iniciar timer
        self._load_image(force_reload=True)
        self.refresh_timer.timeout.connect(self._auto_refresh)
        self.refresh_timer.start(self.current_interval * 1000)
        
        logger.info(f"Ventana flotante creada para cámara {camera.id}")
        
    def _setup_ui(self):
        """Configura la interfaz mínima."""
        self.setWindowTitle(f"📷 {self.camera.nombre}")
        self.setMinimumSize(320, 240)
        self.resize(320, 240)
        
        # Hacer que la ventana flote encima si es necesario, 
        # pero permitir que se mueva libremente.
        # self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.image_label = QLabel("Cargando...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setStyleSheet("background-color: black; color: white;")
        
        # Info overlay (opcional, se puede mostrar al pasar el mouse)
        self.info_label = QLabel(self.camera.nombre)
        self.info_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 150);
            color: white;
            padding: 5px;
            font-size: 9pt;
        """)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.hide() # Ocultar por defecto
        
        layout.addWidget(self.image_label)
        # layout.addWidget(self.info_label)
        
        self.setCentralWidget(central_widget)
        
    def _connect_signals(self):
        self.image_loader.image_loaded.connect(self._on_image_loaded)
        self.image_loader.image_error.connect(self._on_image_error)
        
    def _load_image(self, force_reload=False):
        if self.camera.url_imagen:
            self.image_loader.load_image(self.camera.id, self.camera.url_imagen, force_reload)
            
    def _auto_refresh(self):
        self._load_image(force_reload=True)
        
    def _on_image_loaded(self, camera_id: int, pixmap: QPixmap):
        if camera_id == self.camera.id:
            self.current_pixmap = pixmap
            self._update_display()
            
    def _on_image_error(self, camera_id: int, error_msg: str):
        if camera_id == self.camera.id:
            self.image_label.setText(f"❌ Error\n{error_msg}")
            
    def _update_display(self):
        if self.current_pixmap:
            scaled = self.current_pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
            
            # Actualizar tooltip con hora de actualización
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.setToolTip(f"{self.camera.nombre}\nActualizado: {timestamp}\nIntervalo: {self.current_interval}s")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_display()
        
    def contextMenuEvent(self, event: QContextMenuEvent):
        """Menú contextual para cambiar el intervalo."""
        menu = QMenu(self)
        
        # Información de la cámara
        info_action = QAction(f"📍 {self.camera.nombre}", self)
        info_action.setEnabled(False)
        menu.addAction(info_action)
        menu.addSeparator()
        
        # Submenú de intervalos
        interval_menu = menu.addMenu("⏱ Intervalo de actualización")
        
        for sec in config.FLOATING_WINDOW_REFRESH_INTERVALS:
            label = f"{sec} segundos" if sec < 60 else f"{sec // 60} minutos"
            action = QAction(label, self)
            action.setCheckable(True)
            if sec == self.current_interval:
                action.setChecked(True)
            
            # Usar una función local para capturar el valor de 'sec'
            def make_callback(s):
                return lambda: self._change_interval(s)
            
            action.triggered.connect(make_callback(sec))
            interval_menu.addAction(action)
        
        menu.addSeparator()
        
        # Otras acciones
        refresh_action = menu.addAction("🔄 Actualizar ahora")
        refresh_action.triggered.connect(lambda: self._load_image(force_reload=True))
        
        close_action = menu.addAction("✖ Cerrar")
        close_action.triggered.connect(self.close)
        
        menu.exec_(event.globalPos())
        
    def _change_interval(self, seconds: int):
        self.current_interval = seconds
        self.refresh_timer.stop()
        self.refresh_timer.start(seconds * 1000)
        logger.info(f"Intervalo cambiado a {seconds}s para cámara {self.camera.id}")
        self._load_image(force_reload=True)

    def closeEvent(self, event):
        self.refresh_timer.stop()
        try:
            self.image_loader.image_loaded.disconnect(self._on_image_loaded)
            self.image_loader.image_error.disconnect(self._on_image_error)
        except (TypeError, RuntimeError):
            pass
        self.closed.emit(self.camera.id)
        super().closeEvent(event)
