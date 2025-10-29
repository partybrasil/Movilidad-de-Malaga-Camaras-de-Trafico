"""
Ventana principal de la aplicación.

Este módulo define la interfaz principal con todos sus componentes:
barra lateral, encabezado, vistas lista/cuadrícula, filtros, etc.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QStackedWidget,
    QScrollArea, QGridLayout, QSplitter, QTextBrowser,
    QStatusBar, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
import logging

from src.controllers.camera_controller import CameraController
from src.views.camera_widget import CameraWidget, CameraListItem
from src.views.styles import get_theme
from src.models.camera import Camera
import config


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación Cámaras de Tráfico Málaga.
    """
    
    def __init__(self):
        """
        Inicializa la ventana principal.
        """
        super().__init__()
        
        self.controller = CameraController()
        self.camera_widgets = {}  # Mapeo camera_id -> widget
        self.current_view_mode = config.DEFAULT_VIEW_MODE
        self.current_theme = config.DEFAULT_THEME
        
        self._setup_ui()
        self._connect_signals()
        self._apply_theme()
        
        # Cargar datos iniciales
        self.controller.load_initial_data()
    
    def _setup_ui(self):
        """
        Configura toda la interfaz de usuario.
        """
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        
        # Widget central principal
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra lateral
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Área de contenido principal
        content_area = self._create_content_area()
        main_layout.addWidget(content_area, stretch=1)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo")
    
    def _create_sidebar(self) -> QWidget:
        """
        Crea la barra lateral con navegación.
        
        Returns:
            Widget de la barra lateral
        """
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo/Título
        title = QLabel("🚦 Málaga\nTráfico")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            padding: 20px;
            font-size: 16pt;
            font-weight: bold;
            color: white;
        """)
        layout.addWidget(title)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #34495e;")
        layout.addWidget(separator)
        
        # Botones de navegación
        self.btn_vista_lista = QPushButton("📋 Vista Lista")
        self.btn_vista_lista.clicked.connect(lambda: self._change_view("lista"))
        layout.addWidget(self.btn_vista_lista)
        
        self.btn_vista_cuadricula = QPushButton("🔲 Vista Cuadrícula")
        self.btn_vista_cuadricula.clicked.connect(lambda: self._change_view("cuadricula"))
        layout.addWidget(self.btn_vista_cuadricula)
        
        layout.addSpacing(10)
        
        self.btn_actualizar = QPushButton("🔄 Actualizar Todo")
        self.btn_actualizar.clicked.connect(self._refresh_all)
        layout.addWidget(self.btn_actualizar)
        
        self.btn_auto_refresh = QPushButton("⏱ Auto-refresco")
        self.btn_auto_refresh.setCheckable(True)
        self.btn_auto_refresh.clicked.connect(self._toggle_auto_refresh)
        layout.addWidget(self.btn_auto_refresh)
        
        layout.addSpacing(10)
        
        self.btn_tema = QPushButton("🌓 Cambiar Tema")
        self.btn_tema.clicked.connect(self._toggle_theme)
        layout.addWidget(self.btn_tema)
        
        layout.addSpacing(10)
        
        self.btn_acerca_de = QPushButton("ℹ Acerca de")
        self.btn_acerca_de.clicked.connect(self._show_about)
        layout.addWidget(self.btn_acerca_de)
        
        # Espaciador
        layout.addStretch()
        
        # Info footer
        footer = QLabel("v1.0.0\nDatos Abiertos\nMálaga")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            padding: 15px;
            font-size: 8pt;
            color: #95a5a6;
        """)
        layout.addWidget(footer)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def _create_content_area(self) -> QWidget:
        """
        Crea el área principal de contenido.
        
        Returns:
            Widget del área de contenido
        """
        content = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Encabezado
        header = self._create_header()
        layout.addWidget(header)
        
        # Área de filtros
        filters = self._create_filters()
        layout.addWidget(filters)
        
        # Área de visualización (stacked para cambiar entre vistas)
        self.stacked_widget = QStackedWidget()
        
        # Vista Lista
        self.list_view = self._create_list_view()
        self.stacked_widget.addWidget(self.list_view)
        
        # Vista Cuadrícula
        self.grid_view = self._create_grid_view()
        self.stacked_widget.addWidget(self.grid_view)
        
        layout.addWidget(self.stacked_widget, stretch=1)
        
        content.setLayout(layout)
        return content
    
    def _create_header(self) -> QWidget:
        """
        Crea el encabezado principal.
        
        Returns:
            Widget del encabezado
        """
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(80)
        
        layout = QHBoxLayout()
        
        # Título principal
        title_layout = QVBoxLayout()
        title = QLabel("Cámaras de Tráfico")
        subtitle = QLabel("Málaga - Visualización en Tiempo Real")
        subtitle.setStyleSheet("font-size: 10pt; font-weight: normal;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addLayout(title_layout)
        
        # Espaciador
        layout.addStretch()
        
        # Contador de cámaras
        self.camera_count_label = QLabel("0 cámaras")
        self.camera_count_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            padding: 10px;
            background-color: rgba(255,255,255,0.2);
            border-radius: 5px;
        """)
        layout.addWidget(self.camera_count_label)
        
        header.setLayout(layout)
        return header
    
    def _create_filters(self) -> QWidget:
        """
        Crea el área de filtros y búsqueda.
        
        Returns:
            Widget de filtros
        """
        filters = QWidget()
        filters.setStyleSheet("padding: 15px; background-color: white;")
        
        layout = QHBoxLayout()
        
        # Barra de búsqueda
        search_label = QLabel("🔍")
        layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre o dirección...")
        self.search_input.textChanged.connect(self._on_search_changed)
        layout.addWidget(self.search_input, stretch=2)
        
        layout.addSpacing(20)
        
        # Filtro por zona
        zone_label = QLabel("Zona:")
        layout.addWidget(zone_label)
        
        self.zone_combo = QComboBox()
        self.zone_combo.addItem("Todas")
        self.zone_combo.currentTextChanged.connect(self._on_zone_filter_changed)
        layout.addWidget(self.zone_combo, stretch=1)
        
        layout.addSpacing(20)
        
        # Botón limpiar filtros
        clear_btn = QPushButton("❌ Limpiar")
        clear_btn.setObjectName("secondary")
        clear_btn.clicked.connect(self._clear_filters)
        layout.addWidget(clear_btn)
        
        filters.setLayout(layout)
        return filters
    
    def _create_list_view(self) -> QWidget:
        """
        Crea la vista de lista de cámaras.
        
        Returns:
            Widget de vista lista
        """
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Contenedor de items
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(5)
        self.list_layout.setContentsMargins(10, 10, 10, 10)
        self.list_container.setLayout(self.list_layout)
        
        scroll.setWidget(self.list_container)
        
        return scroll
    
    def _create_grid_view(self) -> QWidget:
        """
        Crea la vista de cuadrícula de cámaras.
        
        Returns:
            Widget de vista cuadrícula
        """
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Contenedor de items en grid
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        self.grid_container.setLayout(self.grid_layout)
        
        scroll.setWidget(self.grid_container)
        
        return scroll
    
    def _connect_signals(self):
        """
        Conecta las señales del controlador.
        """
        self.controller.data_loaded.connect(self._on_data_loaded)
        self.controller.cameras_updated.connect(self._update_camera_display)
        self.controller.loading_progress.connect(self._update_status)
        self.controller.image_loader.image_loaded.connect(self._on_image_loaded)
        self.controller.image_loader.image_error.connect(self._on_image_error)
    
    def _on_data_loaded(self, success: bool):
        """
        Callback cuando se cargan los datos iniciales.
        
        Args:
            success: True si la carga fue exitosa
        """
        if success:
            # Poblar combo de zonas
            zonas = ["Todas"] + self.controller.get_zonas()
            self.zone_combo.clear()
            self.zone_combo.addItems(zonas)
            
            self.status_bar.showMessage("Datos cargados correctamente", 3000)
        else:
            QMessageBox.critical(
                self,
                "Error de Conexión",
                "No se pudieron cargar los datos de las cámaras.\n"
                "Verifica tu conexión a internet e inténtalo de nuevo."
            )
            self.status_bar.showMessage("Error al cargar datos")
    
    def _update_camera_display(self, cameras: list):
        """
        Actualiza la visualización de cámaras.
        
        Args:
            cameras: Lista de objetos Camera a mostrar
        """
        # Limpiar widgets existentes
        self._clear_camera_widgets()
        
        # Actualizar contador
        self.camera_count_label.setText(f"{len(cameras)} cámaras")
        
        if self.current_view_mode == "lista":
            self._populate_list_view(cameras)
        else:
            self._populate_grid_view(cameras)
        
        # Cargar imágenes
        for camera in cameras[:20]:  # Limitar inicial para rendimiento
            self.controller.load_camera_image(camera)
    
    def _populate_list_view(self, cameras: list):
        """
        Puebla la vista de lista con cámaras.
        
        Args:
            cameras: Lista de cámaras
        """
        for camera in cameras:
            item_widget = CameraListItem(camera)
            item_widget.camera_clicked.connect(self._show_camera_details)
            
            self.list_layout.addWidget(item_widget)
            self.camera_widgets[camera.id] = item_widget
        
        # Espaciador al final
        self.list_layout.addStretch()
    
    def _populate_grid_view(self, cameras: list):
        """
        Puebla la vista de cuadrícula con cámaras.
        
        Args:
            cameras: Lista de cámaras
        """
        cols = config.GRID_COLUMNS
        
        for idx, camera in enumerate(cameras):
            row = idx // cols
            col = idx % cols
            
            camera_widget = CameraWidget(camera)
            camera_widget.camera_clicked.connect(self._show_camera_details)
            camera_widget.image_reload_requested.connect(
                lambda cam_id: self.controller.load_camera_image(
                    self._get_camera_by_id(cam_id), 
                    force_reload=True
                )
            )
            
            self.grid_layout.addWidget(camera_widget, row, col)
            self.camera_widgets[camera.id] = camera_widget
    
    def _clear_camera_widgets(self):
        """
        Limpia todos los widgets de cámaras.
        """
        # Limpiar lista
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Limpiar grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.camera_widgets.clear()
    
    def _on_image_loaded(self, camera_id: int, pixmap):
        """
        Callback cuando una imagen se carga.
        
        Args:
            camera_id: ID de la cámara
            pixmap: Imagen cargada
        """
        if camera_id in self.camera_widgets:
            widget = self.camera_widgets[camera_id]
            
            if isinstance(widget, CameraWidget):
                widget.set_image(pixmap)
            elif isinstance(widget, CameraListItem):
                widget.set_thumbnail(pixmap)
    
    def _on_image_error(self, camera_id: int, error_msg: str):
        """
        Callback cuando falla la carga de una imagen.
        
        Args:
            camera_id: ID de la cámara
            error_msg: Mensaje de error
        """
        if camera_id in self.camera_widgets:
            widget = self.camera_widgets[camera_id]
            
            if isinstance(widget, CameraWidget):
                widget.set_error("Error al cargar")
    
    def _change_view(self, view_mode: str):
        """
        Cambia entre vista lista y cuadrícula.
        
        Args:
            view_mode: "lista" o "cuadricula"
        """
        self.current_view_mode = view_mode
        
        if view_mode == "lista":
            self.stacked_widget.setCurrentIndex(0)
        else:
            self.stacked_widget.setCurrentIndex(1)
        
        # Recargar cámaras en la nueva vista
        cameras = self.controller.get_filtered_cameras()
        self._update_camera_display(cameras)
        
        logger.info(f"Vista cambiada a: {view_mode}")
    
    def _on_search_changed(self, text: str):
        """
        Callback cuando cambia el texto de búsqueda.
        
        Args:
            text: Texto de búsqueda
        """
        self.controller.search_cameras(text)
    
    def _on_zone_filter_changed(self, zone: str):
        """
        Callback cuando cambia el filtro de zona.
        
        Args:
            zone: Zona seleccionada
        """
        if zone == "Todas":
            self.controller.filter_by_zona(None)
        else:
            self.controller.filter_by_zona(zone)
    
    def _clear_filters(self):
        """
        Limpia todos los filtros.
        """
        self.search_input.clear()
        self.zone_combo.setCurrentIndex(0)
        self.controller.filter_by_zona(None)
    
    def _refresh_all(self):
        """
        Refresca todas las imágenes.
        """
        self.status_bar.showMessage("Actualizando imágenes...")
        self.controller.refresh_all_images()
        self.status_bar.showMessage("Imágenes actualizadas", 2000)
    
    def _toggle_auto_refresh(self, checked: bool):
        """
        Activa/desactiva el refresco automático.
        
        Args:
            checked: Estado del botón
        """
        if checked:
            self.controller.start_auto_refresh()
            self.status_bar.showMessage("Auto-refresco activado", 2000)
        else:
            self.controller.stop_auto_refresh()
            self.status_bar.showMessage("Auto-refresco desactivado", 2000)
    
    def _toggle_theme(self):
        """
        Alterna entre tema claro y oscuro.
        """
        if self.current_theme == "claro":
            self.current_theme = "oscuro"
        else:
            self.current_theme = "claro"
        
        self._apply_theme()
    
    def _apply_theme(self):
        """
        Aplica el tema actual.
        """
        stylesheet = get_theme(self.current_theme)
        self.setStyleSheet(stylesheet)
        logger.info(f"Tema aplicado: {self.current_theme}")
    
    def _show_camera_details(self, camera_id: int):
        """
        Muestra los detalles de una cámara.
        
        Args:
            camera_id: ID de la cámara
        """
        camera = self._get_camera_by_id(camera_id)
        if not camera:
            return
        
        # Crear diálogo de detalles
        details_html = f"""
        <h2>{camera.nombre}</h2>
        <p><b>📍 Dirección:</b> {camera.direccion}</p>
        <p><b>🗺 Zona:</b> {camera.get_zona_from_direccion()}</p>
        """
        
        if camera.coordenadas:
            x, y = camera.coordenadas
            details_html += f"<p><b>📐 Coordenadas:</b> X={x:.2f}, Y={y:.2f}</p>"
        
        if camera.url:
            details_html += f'<p><b>🔗 Web:</b> <a href="{camera.url}">Ver en web oficial</a></p>'
        
        if camera.url_imagen:
            details_html += f'<p><b>🖼 Imagen:</b> <a href="{camera.url_imagen}">Enlace directo</a></p>'
        
        details_html += "<hr><p><i>💡 Integración de mapas disponible en futuras versiones</i></p>"
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Detalles de Cámara")
        msg.setTextFormat(Qt.RichText)
        msg.setText(details_html)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
    
    def _show_about(self):
        """
        Muestra el diálogo Acerca de.
        """
        about_text = """
        <h2>Cámaras de Tráfico Málaga</h2>
        <p><b>Versión:</b> 1.0.0</p>
        <p><b>Desarrollado con:</b> PySide6 (Qt for Python)</p>
        <hr>
        <p>Aplicación de visualización en tiempo real de las cámaras 
        de tráfico de Málaga usando datos abiertos oficiales.</p>
        <p><b>Fuente de datos:</b><br>
        <a href="https://datosabiertos.malaga.eu">
        Portal de Datos Abiertos del Ayuntamiento de Málaga
        </a></p>
        <hr>
        <p><i>Desarrollado como prototipo educativo</i></p>
        """
        
        QMessageBox.about(self, "Acerca de", about_text)
    
    def _update_status(self, message: str):
        """
        Actualiza la barra de estado.
        
        Args:
            message: Mensaje a mostrar
        """
        self.status_bar.showMessage(message)
    
    def _get_camera_by_id(self, camera_id: int) -> Camera:
        """
        Obtiene una cámara por su ID.
        
        Args:
            camera_id: ID de la cámara
            
        Returns:
            Objeto Camera o None
        """
        for camera in self.controller.get_all_cameras():
            if camera.id == camera_id:
                return camera
        return None
    
    def closeEvent(self, event):
        """
        Maneja el cierre de la ventana.
        """
        self.controller.stop_auto_refresh()
        logger.info("Aplicación cerrada")
        event.accept()
