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
from typing import Optional

from src.controllers.camera_controller import CameraController
from src.views.camera_widget import CameraWidget, CameraListItem, CameraDetailDialog
from src.views.styles import get_theme, get_available_themes, get_text_color, get_textbox_background
from src.models.camera import Camera
from src.views.timelapse_library import TimelapseLibraryDialog
from src.views.theme_preview_dialog import ThemePreviewDialog
from src.timelapse.models import TimelapseSession
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
        self.camera_widgets_by_view = {
            "lista": {},
            "cuadricula": {},
            "favoritos": {},
        }
        self.current_view_mode = config.DEFAULT_VIEW_MODE
        self.current_theme = config.DEFAULT_THEME
        self.current_text_color = config.DEFAULT_TEXT_COLOR
        self.current_textbox_background = config.DEFAULT_TEXTBOX_BACKGROUND
        self.thumbnail_zoom_level = config.DEFAULT_THUMBNAIL_ZOOM  # Nivel de zoom actual (1-5)
        self.timelapse_dialog: TimelapseLibraryDialog | None = None
        
        self._setup_ui()
        self._connect_signals()
        self._apply_theme()
        self._update_timelapse_indicator(self.controller.get_timelapse_sessions())
        
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
        
        self.btn_vista_favoritos = QPushButton("⭐ Vista Favoritos")
        self.btn_vista_favoritos.clicked.connect(lambda: self._change_view("favoritos"))
        layout.addWidget(self.btn_vista_favoritos)
        
        layout.addSpacing(10)
        
        self.btn_actualizar = QPushButton("🔄 Actualizar Todo")
        self.btn_actualizar.clicked.connect(self._refresh_all)
        layout.addWidget(self.btn_actualizar)
        
        self.btn_auto_refresh = QPushButton("⏱ Auto-refresco")
        self.btn_auto_refresh.setCheckable(True)
        self.btn_auto_refresh.clicked.connect(self._toggle_auto_refresh)
        layout.addWidget(self.btn_auto_refresh)

        layout.addSpacing(10)

        self.btn_timelapse = QPushButton("🎞 Timelapse")
        self.btn_timelapse.clicked.connect(self._open_timelapse_library)
        layout.addWidget(self.btn_timelapse)

        layout.addSpacing(10)
        
        # Sección de Personalización
        personalization_label = QLabel("🎨 Personalización")
        personalization_label.setStyleSheet("font-weight: bold; color: #ecf0f1; font-size: 12pt; margin: 10px 0 5px 0;")
        layout.addWidget(personalization_label)
        
        # Botón de vista previa de temas
        self.btn_theme_preview = QPushButton("🔍 Vista Previa de Temas")
        self.btn_theme_preview.clicked.connect(self._show_theme_preview)
        layout.addWidget(self.btn_theme_preview)
        
        layout.addSpacing(5)
        
        # Selector de tema principal
        theme_label = QLabel("Tema:")
        theme_label.setStyleSheet("color: #ecf0f1; font-size: 9pt; margin-left: 5px;")
        layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Claro", "Oscuro", "Azul Profundo", "Verde Bosque", "Púrpura Real",
            "Rojo Cereza", "Naranja Atardecer", "Rosa Sakura", "Gris Corporativo",
            "Azul Hielo", "Verde Menta", "Ámbar Dorado", "Violeta Nocturno",
            "Turquesa Tropical", "Salmón Suave", "Lavanda Relajante", "Oliva Natural",
            "Chocolate Rico", "Slate Moderno", "Teal Océano", "Coral Vibrante"
        ])
        # Establecer el tema actual como seleccionado
        current_theme_index = max(0, config.AVAILABLE_THEMES.index(self.current_theme) if self.current_theme in config.AVAILABLE_THEMES else 0)
        self.theme_combo.setCurrentIndex(current_theme_index)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        layout.addWidget(self.theme_combo)
        
        layout.addSpacing(5)
        
        # Selector de color de texto
        text_color_label = QLabel("Color de texto:")
        text_color_label.setStyleSheet("color: #ecf0f1; font-size: 9pt; margin-left: 5px;")
        layout.addWidget(text_color_label)
        
        self.text_color_combo = QComboBox()
        self.text_color_combo.addItems([
            "Por defecto", "Negro", "Blanco", "Gris Oscuro", "Gris Claro", "Azul Oscuro",
            "Azul Claro", "Verde Oscuro", "Verde Claro", "Rojo Oscuro", "Rojo Claro",
            "Púrpura Oscuro", "Púrpura Claro", "Naranja Oscuro", "Naranja Claro",
            "Amarillo Oscuro", "Amarillo Claro", "Rosa Oscuro", "Rosa Claro",
            "Turquesa Oscuro", "Turquesa Claro", "Marrón Oscuro", "Marrón Claro"
        ])
        # Establecer el color actual como seleccionado
        current_text_index = max(0, config.TEXT_COLORS.index(self.current_text_color) if self.current_text_color in config.TEXT_COLORS else 0)
        self.text_color_combo.setCurrentIndex(current_text_index)
        self.text_color_combo.currentTextChanged.connect(self._on_text_color_changed)
        layout.addWidget(self.text_color_combo)
        
        layout.addSpacing(5)
        
        # Selector de fondo de caja de texto
        textbox_bg_label = QLabel("Fondo de cajas de texto:")
        textbox_bg_label.setStyleSheet("color: #ecf0f1; font-size: 9pt; margin-left: 5px;")
        layout.addWidget(textbox_bg_label)
        
        self.textbox_bg_combo = QComboBox()
        self.textbox_bg_combo.addItems([
            "Por defecto", "Blanco", "Gris Muy Claro", "Gris Claro", "Gris Medio", 
            "Gris Oscuro", "Negro", "Azul Muy Claro", "Azul Claro", "Verde Muy Claro",
            "Verde Claro", "Amarillo Muy Claro", "Amarillo Claro", "Rosa Muy Claro",
            "Rosa Claro", "Púrpura Muy Claro", "Púrpura Claro", "Naranja Muy Claro",
            "Naranja Claro", "Turquesa Muy Claro", "Turquesa Claro", "Crema", "Beige"
        ])
        # Establecer el fondo actual como seleccionado
        current_textbox_index = max(0, config.TEXTBOX_BACKGROUNDS.index(self.current_textbox_background) if self.current_textbox_background in config.TEXTBOX_BACKGROUNDS else 0)
        self.textbox_bg_combo.setCurrentIndex(current_textbox_index)
        self.textbox_bg_combo.currentTextChanged.connect(self._on_textbox_bg_changed)
        layout.addWidget(self.textbox_bg_combo)
        
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

        # Vista Favoritos
        self.favorites_view = self._create_favorites_view()
        self.stacked_widget.addWidget(self.favorites_view)
        
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
        
        # Indicador de auto-refresco
        self.auto_refresh_indicator = QLabel("⏸ Auto-refresco: Inactivo")
        self.auto_refresh_indicator.setStyleSheet("""
            font-size: 11pt;
            font-weight: bold;
            padding: 8px 12px;
            background-color: rgba(149, 165, 166, 0.3);
            border-radius: 5px;
            color: #7f8c8d;
            margin-right: 10px;
        """)
        layout.addWidget(self.auto_refresh_indicator)

        # Indicador de timelapse
        self.timelapse_indicator = QLabel("🎞 Timelapse: 0 activos / 0 guardados")
        self.timelapse_indicator.setStyleSheet("""
            font-size: 10pt;
            font-weight: bold;
            padding: 6px 10px;
            background-color: rgba(241, 196, 15, 0.2);
            border-radius: 5px;
            color: #f39c12;
            margin-right: 10px;
        """)
        layout.addWidget(self.timelapse_indicator)
        
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
        
        # Controles de zoom (solo para vista cuadrícula)
        self.zoom_controls = QWidget()
        zoom_layout = QHBoxLayout()
        zoom_layout.setContentsMargins(0, 0, 0, 0)
        zoom_layout.setSpacing(8)
        
        zoom_label = QLabel("🔍 Zoom:")
        zoom_layout.addWidget(zoom_label)
        
        # Botón zoom -
        self.zoom_out_btn = QPushButton("−")
        self.zoom_out_btn.setFixedSize(30, 30)
        self.zoom_out_btn.setObjectName("zoom")
        self.zoom_out_btn.setStyleSheet("""
            QPushButton#zoom {
                font-size: 18pt;
                font-weight: bold;
                border-radius: 15px;
                background-color: #ecf0f1;
            }
            QPushButton#zoom:hover {
                background-color: #3498db;
                color: white;
            }
            QPushButton#zoom:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.zoom_out_btn.clicked.connect(self._zoom_out)
        zoom_layout.addWidget(self.zoom_out_btn)
        
        # Indicador de nivel de zoom
        self.zoom_indicator = QLabel(f"{self.thumbnail_zoom_level}/5")
        self.zoom_indicator.setStyleSheet("""
            font-weight: bold;
            font-size: 10pt;
            padding: 4px 10px;
            background-color: #ecf0f1;
            border-radius: 3px;
        """)
        zoom_layout.addWidget(self.zoom_indicator)
        
        # Botón zoom +
        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setFixedSize(30, 30)
        self.zoom_in_btn.setObjectName("zoom")
        self.zoom_in_btn.setStyleSheet("""
            QPushButton#zoom {
                font-size: 18pt;
                font-weight: bold;
                border-radius: 15px;
                background-color: #ecf0f1;
            }
            QPushButton#zoom:hover {
                background-color: #3498db;
                color: white;
            }
            QPushButton#zoom:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.zoom_in_btn.clicked.connect(self._zoom_in)
        zoom_layout.addWidget(self.zoom_in_btn)
        
        self.zoom_controls.setLayout(zoom_layout)
        layout.addWidget(self.zoom_controls)
        
        # Ocultar controles de zoom inicialmente si no estamos en vista cuadrícula
        self.zoom_controls.setVisible(self.current_view_mode == "cuadricula")
        
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
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Contenedor de items en grid
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        self.grid_container.setLayout(self.grid_layout)
        
        scroll.setWidget(self.grid_container)
        
        return scroll

    def _create_favorites_view(self) -> QWidget:
        """Crea la vista de cámaras favoritas en formato cuadrícula."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.favorites_container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(15, 15, 15, 15)
        container_layout.setSpacing(10)

        self.favorites_placeholder = QLabel(
            "Añade cámaras desde la ⭐ en los detalles para verlas aquí."
        )
        self.favorites_placeholder.setAlignment(Qt.AlignCenter)
        self.favorites_placeholder.setStyleSheet(
            "color: #7f8c8d; font-style: italic;"
        )
        container_layout.addWidget(self.favorites_placeholder)

        self.favorites_grid_widget = QWidget()
        self.favorites_layout = QGridLayout()
        self.favorites_layout.setSpacing(15)
        self.favorites_layout.setContentsMargins(0, 0, 0, 0)
        self.favorites_grid_widget.setLayout(self.favorites_layout)
        container_layout.addWidget(self.favorites_grid_widget)

        self.favorites_container.setLayout(container_layout)
        scroll.setWidget(self.favorites_container)

        self.favorites_grid_widget.hide()

        return scroll
    
    def _connect_signals(self):
        """
        Conecta las señales del controlador.
        """
        self.controller.data_loaded.connect(self._on_data_loaded)
        self.controller.cameras_updated.connect(self._update_camera_display)
        self.controller.loading_progress.connect(self._update_status)
        self.controller.refresh_progress.connect(self._on_refresh_progress)
        self.controller.image_loader.image_loaded.connect(self._on_image_loaded)
        self.controller.image_loader.image_error.connect(self._on_image_error)
        self.controller.favorites_updated.connect(self._on_favorites_updated)
        self.controller.favorite_toggled.connect(self._on_favorite_toggled)
        self.controller.timelapse_sessions_changed.connect(self._on_timelapse_sessions_changed)
        self.controller.timelapse_session_started.connect(self._on_timelapse_started)
        self.controller.timelapse_session_finished.connect(self._on_timelapse_finished)
        self.controller.timelapse_error.connect(self._on_timelapse_error)
        self.controller.timelapse_export_completed.connect(self._on_timelapse_exported)
    
    def _open_timelapse_library(self):
        """Abre el diálogo de gestión de timelapses."""
        if self.timelapse_dialog and self.timelapse_dialog.isVisible():
            self.timelapse_dialog.raise_()
            self.timelapse_dialog.activateWindow()
            return

        self.timelapse_dialog = TimelapseLibraryDialog(self.controller, self)
        self.timelapse_dialog.finished.connect(self._on_timelapse_dialog_closed)
        self.timelapse_dialog.show()

    def _on_timelapse_dialog_closed(self, _result: int):
        """Restablece el estado cuando se cierra el diálogo de timelapse."""
        self.timelapse_dialog = None

    def _on_timelapse_sessions_changed(self, sessions: list[TimelapseSession]):
        """Actualiza indicadores cuando cambian las sesiones."""
        self._update_timelapse_indicator(sessions)

    def _on_timelapse_started(self, session: TimelapseSession):
        """Maneja el inicio de una nueva sesión de timelapse."""
        self.status_bar.showMessage(
            f"Timelapse iniciado: {session.camera_name}",
            4000,
        )
        self._update_timelapse_indicator()

    def _on_timelapse_finished(self, session: TimelapseSession):
        """Maneja la finalización de una sesión de timelapse."""
        self.status_bar.showMessage(
            f"Timelapse finalizado: {session.camera_name}",
            4000,
        )
        self._update_timelapse_indicator()

    def _on_timelapse_error(self, message: str):
        """Notifica errores ocurridos durante la captura de timelapse."""
        self.status_bar.showMessage(f"Timelapse: {message}", 5000)
        QMessageBox.warning(self, "Timelapse", message)
        self._update_timelapse_indicator()

    def _on_timelapse_exported(self, session_id: str, fmt: str, path: str):
        """Informa sobre exportaciones completadas."""
        self.status_bar.showMessage(
            f"Exportado timelapse {session_id} → {fmt.upper()} ({path})",
            6000,
        )
        self._update_timelapse_indicator()

    def _update_timelapse_indicator(self, sessions: list[TimelapseSession] | None = None):
        """Refresca los contadores asociados a timelapses activos y guardados."""
        sessions_list = sessions if sessions is not None else self.controller.get_timelapse_sessions()
        active_count = len(self.controller.get_active_timelapse_ids())
        total_count = len(sessions_list)

        self.timelapse_indicator.setText(
            f"🎞 Timelapse: {active_count} activos / {total_count} guardados"
        )

        if active_count:
            self.btn_timelapse.setText(f"🎞 Timelapse ({active_count})")
        else:
            self.btn_timelapse.setText("🎞 Timelapse")

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
        if self.current_view_mode == "favoritos":
            favorites = self.controller.get_favorite_cameras()
            self._populate_favorites_view(favorites)
            count = len(favorites)
            label = "favoritas" if count != 1 else "favorita"
            self.camera_count_label.setText(f"{count} {label}")
            return

        view_key = self.current_view_mode
        self._clear_camera_widgets(view_key)

        # Actualizar contador general
        self.camera_count_label.setText(f"{len(cameras)} cámaras")

        if view_key == "lista":
            self._populate_list_view(cameras)
        else:
            self._populate_grid_view(cameras)

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
            self.camera_widgets_by_view["lista"][camera.id] = item_widget

        self.list_layout.addStretch()
    
    def _populate_grid_view(self, cameras: list):
        """
        Puebla la vista de cuadrícula con cámaras.
        
        Args:
            cameras: Lista de cámaras
        """
        cols = self._calculate_grid_columns(self.grid_view)
        thumbnail_size = config.THUMBNAIL_SIZES[self.thumbnail_zoom_level]

        for idx, camera in enumerate(cameras):
            row = idx // cols
            col = idx % cols

            camera_widget = CameraWidget(camera, thumbnail_size=thumbnail_size)
            camera_widget.camera_clicked.connect(self._show_camera_details)
            camera_widget.image_reload_requested.connect(self._request_image_reload)

            self.grid_layout.addWidget(camera_widget, row, col)
            self.camera_widgets_by_view["cuadricula"][camera.id] = camera_widget

    def _populate_favorites_view(self, cameras: list[Camera]):
        """Genera la cuadrícula de cámaras favoritas."""
        self._clear_camera_widgets("favoritos")

        if not cameras:
            return

        self.favorites_placeholder.hide()
        self.favorites_grid_widget.show()

        cols = self._calculate_grid_columns(self.favorites_view)
        if cols < 1:
            cols = 1

        thumbnail_size = config.THUMBNAIL_SIZES[self.thumbnail_zoom_level]

        for idx, camera in enumerate(cameras):
            row = idx // cols
            col = idx % cols

            camera_widget = CameraWidget(camera, thumbnail_size=thumbnail_size)
            camera_widget.camera_clicked.connect(self._show_camera_details)
            camera_widget.image_reload_requested.connect(self._request_image_reload)

            self.favorites_layout.addWidget(camera_widget, row, col)
            self.camera_widgets_by_view["favoritos"][camera.id] = camera_widget
            # Cargar imagen siempre: pocas cámaras y asegura miniaturas frescas
            self.controller.load_camera_image(camera)
    
    def _request_image_reload(self, camera_id: int):
        """Solicita recargar la imagen de una cámara concreta."""
        camera = self._get_camera_by_id(camera_id)
        if camera:
            self.controller.load_camera_image(camera, force_reload=True)

    def _relayout_grid(self, view_key: str, layout: QGridLayout, scroll_area: QScrollArea):
        """Reorganiza los widgets existentes según el ancho disponible."""
        widgets_map = self.camera_widgets_by_view.get(view_key, {})
        if not widgets_map:
            if view_key == "favoritos":
                self.favorites_placeholder.show()
                self.favorites_grid_widget.hide()
            return

        while layout.count():
            layout.takeAt(0)

        columns = self._calculate_grid_columns(scroll_area)
        columns = max(columns, 1)

        if view_key == "favoritos":
            self.favorites_placeholder.hide()
            self.favorites_grid_widget.show()

        for idx, widget in enumerate(widgets_map.values()):
            row = idx // columns
            col = idx % columns
            layout.addWidget(widget, row, col)

    def _clear_camera_widgets(self, view: str | None = None):
        """Limpia los widgets asociados a la vista indicada."""
        targets = [view] if view else ["lista", "cuadricula", "favoritos"]

        for target in targets:
            if target == "lista":
                while self.list_layout.count():
                    item = self.list_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                self.camera_widgets_by_view["lista"].clear()
            elif target == "cuadricula":
                while self.grid_layout.count():
                    item = self.grid_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                self.camera_widgets_by_view["cuadricula"].clear()
            elif target == "favoritos":
                while self.favorites_layout.count():
                    item = self.favorites_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                self.camera_widgets_by_view["favoritos"].clear()
                self.favorites_grid_widget.hide()
                self.favorites_placeholder.show()
    
    def _on_image_loaded(self, camera_id: int, pixmap):
        """
        Callback cuando una imagen se carga.
        
        Args:
            camera_id: ID de la cámara
            pixmap: Imagen cargada
        """
        for widgets in self.camera_widgets_by_view.values():
            widget = widgets.get(camera_id)
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
        for widgets in self.camera_widgets_by_view.values():
            widget = widgets.get(camera_id)
            if isinstance(widget, CameraWidget):
                widget.set_error("Error al cargar")

    def _on_favorites_updated(self, favorite_ids: list[int]):
        """Actualiza la UI cuando cambia la lista de favoritos."""
        count = len(favorite_ids)
        if count:
            self.btn_vista_favoritos.setText(f"⭐ Vista Favoritos ({count})")
        else:
            self.btn_vista_favoritos.setText("⭐ Vista Favoritos")

        favorites = self.controller.get_favorite_cameras()
        self._populate_favorites_view(favorites)

        if self.current_view_mode == "favoritos":
            label = "favoritas" if count != 1 else "favorita"
            self.camera_count_label.setText(f"{count} {label}")

    def _on_favorite_toggled(self, camera_id: int, is_favorite: bool):
        """Muestra retroalimentación cuando cambia el estado de favorito."""
        camera = self._get_camera_by_id(camera_id)
        if not camera:
            return
        action = "añadida a favoritos" if is_favorite else "retirada de favoritos"
        self.status_bar.showMessage(f"{camera.nombre} {action}", 3000)
    
    def _on_refresh_progress(self, current: int, total: int):
        """
        Callback cuando se actualiza el progreso de refresco.
        
        Args:
            current: Número de cámara actual
            total: Total de cámaras a actualizar
        """
        if current < total:
            self.status_bar.showMessage(f"Actualizando Cámara {current}/{total}...")
        else:
            self.status_bar.showMessage("✓ Todas las Cámaras han sido Actualizadas", 5000)
            logger.info("Actualización completa de todas las cámaras")
    
    def _change_view(self, view_mode: str):
        """Cambia entre las vistas lista, cuadrícula y favoritos."""
        self.current_view_mode = view_mode

        if view_mode == "lista":
            self.stacked_widget.setCurrentIndex(0)
            self.zoom_controls.setVisible(False)
            cameras = self.controller.get_filtered_cameras()
            self._update_camera_display(cameras)
        elif view_mode == "cuadricula":
            self.stacked_widget.setCurrentIndex(1)
            self.zoom_controls.setVisible(True)
            cameras = self.controller.get_filtered_cameras()
            self._update_camera_display(cameras)
        elif view_mode == "favoritos":
            self.stacked_widget.setCurrentIndex(2)
            self.zoom_controls.setVisible(True)
            favorites = self.controller.get_favorite_cameras()
            self._populate_favorites_view(favorites)
            count = len(favorites)
            label = "favoritas" if count != 1 else "favorita"
            self.camera_count_label.setText(f"{count} {label}")
        else:
            logger.warning("Vista desconocida solicitada: %s", view_mode)
            return

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
    
    def _zoom_in(self):
        """
        Aumenta el tamaño de las miniaturas.
        """
        if self.thumbnail_zoom_level < 5:
            self.thumbnail_zoom_level += 1
            self._update_zoom()
            logger.info(f"Zoom aumentado a nivel {self.thumbnail_zoom_level}")
    
    def _zoom_out(self):
        """
        Disminuye el tamaño de las miniaturas.
        """
        if self.thumbnail_zoom_level > 1:
            self.thumbnail_zoom_level -= 1
            self._update_zoom()
            logger.info(f"Zoom disminuido a nivel {self.thumbnail_zoom_level}")
    
    def _update_zoom(self):
        """
        Actualiza el zoom de las miniaturas y reorganiza la cuadrícula.
        """
        # Actualizar indicador
        self.zoom_indicator.setText(f"{self.thumbnail_zoom_level}/5")
        
        # Actualizar estado de botones
        self.zoom_out_btn.setEnabled(self.thumbnail_zoom_level > 1)
        self.zoom_in_btn.setEnabled(self.thumbnail_zoom_level < 5)
        
        if self.current_view_mode == "cuadricula":
            cameras = self.controller.get_filtered_cameras()
            self._update_camera_display(cameras)
        elif self.current_view_mode == "favoritos":
            favorites = self.controller.get_favorite_cameras()
            self._populate_favorites_view(favorites)
    
    def _calculate_grid_columns(self, scroll_area: Optional[QWidget] = None) -> int:
        """Calcula el número óptimo de columnas para una cuadrícula dada."""
        thumbnail_width, _ = config.THUMBNAIL_SIZES[self.thumbnail_zoom_level]
        target = scroll_area or self.grid_view

        if hasattr(target, "viewport"):
            available_width = target.viewport().width() - 30
        else:
            available_width = target.width() - 30

        available_width = max(available_width, thumbnail_width + 30)

        spacing = 15
        widget_total_width = thumbnail_width + 30

        columns = max(1, min(6, available_width // (widget_total_width + spacing)))

        logger.debug(
            "Calculadas %s columnas para ancho %spx con miniaturas de %spx",
            columns,
            available_width,
            thumbnail_width,
        )
        return columns
    
    def _refresh_all(self):
        """
        Refresca todas las imágenes.
        """
        total_cameras = len(self.controller.get_filtered_cameras())
        self.status_bar.showMessage(f"Iniciando actualización de {total_cameras} cámaras...")
        self.controller.refresh_all_images()
    
    def _toggle_auto_refresh(self, checked: bool):
        """
        Activa/desactiva el refresco automático.
        
        Args:
            checked: Estado del botón
        """
        if checked:
            self.controller.start_auto_refresh()
            self.status_bar.showMessage("Auto-refresco activado", 2000)
            # Actualizar indicador visual
            self.auto_refresh_indicator.setText("▶ Auto-refresco: Activo")
            self.auto_refresh_indicator.setStyleSheet("""
                font-size: 11pt;
                font-weight: bold;
                padding: 8px 12px;
                background-color: rgba(39, 174, 96, 0.3);
                border-radius: 5px;
                color: #27ae60;
                margin-right: 10px;
            """)
        else:
            self.controller.stop_auto_refresh()
            self.status_bar.showMessage("Auto-refresco desactivado", 2000)
            # Actualizar indicador visual
            self.auto_refresh_indicator.setText("⏸ Auto-refresco: Inactivo")
            self.auto_refresh_indicator.setStyleSheet("""
                font-size: 11pt;
                font-weight: bold;
                padding: 8px 12px;
                background-color: rgba(149, 165, 166, 0.3);
                border-radius: 5px;
                color: #7f8c8d;
                margin-right: 10px;
            """)
    
    def _on_theme_changed(self, theme_display_name: str):
        """
        Maneja el cambio de tema principal.
        """
        # Mapear nombre mostrado a nombre interno
        theme_map = {
            "Claro": "claro",
            "Oscuro": "oscuro",
            "Azul Profundo": "azul_profundo",
            "Verde Bosque": "verde_bosque",
            "Púrpura Real": "purpura_real",
            "Rojo Cereza": "rojo_cereza",
            "Naranja Atardecer": "naranja_atardecer",
            "Rosa Sakura": "rosa_sakura",
            "Gris Corporativo": "gris_corporativo",
            "Azul Hielo": "azul_hielo",
            "Verde Menta": "verde_menta",
            "Ámbar Dorado": "ambar_dorado",
            "Violeta Nocturno": "violeta_nocturno",
            "Turquesa Tropical": "turquesa_tropical",
            "Salmón Suave": "salmon_suave",
            "Lavanda Relajante": "lavanda_relajante",
            "Oliva Natural": "oliva_natural",
            "Chocolate Rico": "chocolate_rico",
            "Slate Moderno": "slate_moderno",
            "Teal Océano": "teal_oceano",
            "Coral Vibrante": "coral_vibrante"
        }
        
        self.current_theme = theme_map.get(theme_display_name, "claro")
        self._apply_theme()
        logger.info(f"Tema cambiado a: {self.current_theme}")
    
    def _on_text_color_changed(self, color_display_name: str):
        """
        Maneja el cambio de color de texto.
        """
        # Mapear nombre mostrado a nombre interno
        color_map = {
            "Por defecto": "default",
            "Negro": "negro",
            "Blanco": "blanco",
            "Gris Oscuro": "gris_oscuro",
            "Gris Claro": "gris_claro",
            "Azul Oscuro": "azul_oscuro",
            "Azul Claro": "azul_claro",
            "Verde Oscuro": "verde_oscuro",
            "Verde Claro": "verde_claro",
            "Rojo Oscuro": "rojo_oscuro",
            "Rojo Claro": "rojo_claro",
            "Púrpura Oscuro": "purpura_oscuro",
            "Púrpura Claro": "purpura_claro",
            "Naranja Oscuro": "naranja_oscuro",
            "Naranja Claro": "naranja_claro",
            "Amarillo Oscuro": "amarillo_oscuro",
            "Amarillo Claro": "amarillo_claro",
            "Rosa Oscuro": "rosa_oscuro",
            "Rosa Claro": "rosa_claro",
            "Turquesa Oscuro": "turquesa_oscuro",
            "Turquesa Claro": "turquesa_claro",
            "Marrón Oscuro": "marron_oscuro",
            "Marrón Claro": "marron_claro"
        }
        
        self.current_text_color = color_map.get(color_display_name, "default")
        self._apply_theme()
        logger.info(f"Color de texto cambiado a: {self.current_text_color}")
    
    def _on_textbox_bg_changed(self, bg_display_name: str):
        """
        Maneja el cambio de fondo de cajas de texto.
        """
        # Mapear nombre mostrado a nombre interno
        bg_map = {
            "Por defecto": "default",
            "Blanco": "blanco",
            "Gris Muy Claro": "gris_muy_claro",
            "Gris Claro": "gris_claro",
            "Gris Medio": "gris_medio",
            "Gris Oscuro": "gris_oscuro",
            "Negro": "negro",
            "Azul Muy Claro": "azul_muy_claro",
            "Azul Claro": "azul_claro",
            "Verde Muy Claro": "verde_muy_claro",
            "Verde Claro": "verde_claro",
            "Amarillo Muy Claro": "amarillo_muy_claro",
            "Amarillo Claro": "amarillo_claro",
            "Rosa Muy Claro": "rosa_muy_claro",
            "Rosa Claro": "rosa_claro",
            "Púrpura Muy Claro": "purpura_muy_claro",
            "Púrpura Claro": "purpura_claro",
            "Naranja Muy Claro": "naranja_muy_claro",
            "Naranja Claro": "naranja_claro",
            "Turquesa Muy Claro": "turquesa_muy_claro",
            "Turquesa Claro": "turquesa_claro",
            "Crema": "crema",
            "Beige": "beige"
        }
        
        self.current_textbox_background = bg_map.get(bg_display_name, "default")
        self._apply_theme()
        logger.info(f"Fondo de cajas de texto cambiado a: {self.current_textbox_background}")
    
    def _show_theme_preview(self):
        """
        Muestra el diálogo de vista previa de temas.
        """
        dialog = ThemePreviewDialog(self.current_theme, self)
        dialog.theme_applied.connect(self._apply_theme_from_preview)
        dialog.exec()
    
    def _apply_theme_from_preview(self, theme_name: str):
        """
        Aplica un tema seleccionado desde la vista previa.
        """
        self.current_theme = theme_name
        
        # Actualizar el combo box del tema
        theme_map = {
            "claro": "Claro",
            "oscuro": "Oscuro",
            "azul_profundo": "Azul Profundo",
            "verde_bosque": "Verde Bosque",
            "purpura_real": "Púrpura Real",
            "rojo_cereza": "Rojo Cereza",
            "naranja_atardecer": "Naranja Atardecer",
            "rosa_sakura": "Rosa Sakura",
            "gris_corporativo": "Gris Corporativo",
            "azul_hielo": "Azul Hielo",
            "verde_menta": "Verde Menta",
            "ambar_dorado": "Ámbar Dorado",
            "violeta_nocturno": "Violeta Nocturno",
            "turquesa_tropical": "Turquesa Tropical",
            "salmon_suave": "Salmón Suave",
            "lavanda_relajante": "Lavanda Relajante",
            "oliva_natural": "Oliva Natural",
            "chocolate_rico": "Chocolate Rico",
            "slate_moderno": "Slate Moderno",
            "teal_oceano": "Teal Océano",
            "coral_vibrante": "Coral Vibrante"
        }
        
        display_name = theme_map.get(theme_name, "Claro")
        try:
            index = [self.theme_combo.itemText(i) for i in range(self.theme_combo.count())].index(display_name)
            self.theme_combo.setCurrentIndex(index)
        except ValueError:
            logger.warning(f"No se pudo encontrar el tema {display_name} en el combo box")
        
        self._apply_theme()
        logger.info(f"Tema aplicado desde vista previa: {theme_name}")
    
    def _toggle_theme(self):
        """
        Alterna entre tema claro y oscuro (método mantenido por compatibilidad).
        """
        if self.current_theme == "claro":
            self.current_theme = "oscuro"
            self.theme_combo.setCurrentIndex(1)
        else:
            self.current_theme = "claro"
            self.theme_combo.setCurrentIndex(0)
        
        self._apply_theme()
    
    def _apply_theme(self):
        """
        Aplica el tema actual con personalizaciones.
        """
        stylesheet = get_theme(
            theme_name=self.current_theme,
            text_color=self.current_text_color,
            textbox_bg=self.current_textbox_background
        )
        self.setStyleSheet(stylesheet)
        logger.info(f"Tema aplicado: {self.current_theme} con texto: {self.current_text_color} y fondo: {self.current_textbox_background}")
    
    def _show_camera_details(self, camera_id: int):
        """
        Muestra los detalles de una cámara en un diálogo dedicado.
        
        Args:
            camera_id: ID de la cámara
        """
        camera = self._get_camera_by_id(camera_id)
        if not camera:
            return
        
        # Crear y mostrar diálogo de detalle con controles
        detail_dialog = CameraDetailDialog(
            camera, 
            self.controller.image_loader,
            self.controller,
            self
        )
        detail_dialog.exec()
    
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

    def resizeEvent(self, event):
        """Ajusta las cuadrículas cuando cambia el tamaño de la ventana."""
        super().resizeEvent(event)
        if self.current_view_mode == "cuadricula":
            self._relayout_grid("cuadricula", self.grid_layout, self.grid_view)
        elif self.current_view_mode == "favoritos":
            self._relayout_grid("favoritos", self.favorites_layout, self.favorites_view)
