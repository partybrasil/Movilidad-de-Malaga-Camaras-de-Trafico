"""
Vista de mapa interactivo para visualización de cámaras.

Este módulo proporciona una vista de mapa con integración de folium
para mostrar las cámaras de tráfico con separaciones por distrito.
"""

from pathlib import Path
from typing import List, Optional, Dict
import tempfile
import logging

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QCheckBox, QTextBrowser
)
from PySide6.QtCore import Qt, Signal, QUrl, QThread
from PySide6.QtGui import QDesktopServices

from src.workers import MapGenerationWorker

import folium
import folium

from src.models.camera import Camera
from src.utils.coordinate_converter import get_converter
import config


logger = logging.getLogger(__name__)


class MapView(QWidget):
    """
    Vista de mapa interactivo con cámaras y distritos.
    """
    
    # Señales
    camera_clicked = Signal(int)  # ID de la cámara clickeada
    
    def __init__(self):
        """
        Inicializa la vista de mapa.
        """
        super().__init__()
        
        self.cameras: List[Camera] = []
        self.filtered_cameras: List[Camera] = []
        self.map_html_path: Optional[Path] = None
        self.converter = get_converter()
        
        # Distritos seleccionados (para filtrar)
        self.selected_districts: set = set()
        
        # Threads
        self.worker_thread = None
        self.worker = None
        
        self._setup_ui()
        logger.info("MapView inicializada")
    
    def _setup_ui(self):
        """
        Configura la interfaz de usuario.
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Barra de controles superior
        controls_layout = QHBoxLayout()
        
        # Título
        title = QLabel("🗺️ Mapa Interactivo de Cámaras")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; margin-bottom: 10px;")
        controls_layout.addWidget(title)
        
        controls_layout.addStretch()
        
        # Botón para regenerar mapa
        self.btn_refresh_map = QPushButton("🔄 Actualizar Mapa")
        self.btn_refresh_map.clicked.connect(self._generate_map)
        self.btn_refresh_map.setToolTip("Regenerar el mapa con los datos actuales")
        controls_layout.addWidget(self.btn_refresh_map)
        
        # Botón para abrir en navegador
        self.btn_open_browser = QPushButton("🌐 Abrir en Navegador")
        self.btn_open_browser.clicked.connect(self._open_in_browser)
        self.btn_open_browser.setToolTip("Abrir el mapa en el navegador web predeterminado")
        self.btn_open_browser.setEnabled(False)
        controls_layout.addWidget(self.btn_open_browser)
        
        layout.addLayout(controls_layout)
        
        # Filtros de distrito
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filtrar por distrito:")
        filter_label.setStyleSheet("font-weight: bold;")
        filter_layout.addWidget(filter_label)
        
        self.district_filter = QComboBox()
        self.district_filter.addItem("Todos los distritos", None)
        for district_id, color in config.DISTRICT_COLORS.items():
            self.district_filter.addItem(f"Distrito {district_id}", district_id)
        self.district_filter.currentIndexChanged.connect(self._on_district_filter_changed)
        filter_layout.addWidget(self.district_filter)
        
        filter_layout.addStretch()
        
        # Checkbox para mostrar límites de distritos
        self.show_districts_checkbox = QCheckBox("Mostrar límites de distritos")
        self.show_districts_checkbox.setChecked(True)
        self.show_districts_checkbox.stateChanged.connect(self._on_show_districts_changed)
        filter_layout.addWidget(self.show_districts_checkbox)
        
        layout.addLayout(filter_layout)
        
        # Área de información / preview
        info_frame = QTextBrowser()
        info_frame.setObjectName("mapInfoFrame")
        info_frame.setOpenExternalLinks(True)
        info_frame.setHtml(self._get_initial_info_html())
        self.info_frame = info_frame
        layout.addWidget(info_frame, stretch=1)
        
        # Contador de cámaras
        self.camera_count_label = QLabel("Cámaras en el mapa: 0")
        self.camera_count_label.setStyleSheet("padding: 5px; font-style: italic;")
        layout.addWidget(self.camera_count_label)
        
        self.setLayout(layout)
    
    def _get_initial_info_html(self) -> str:
        """
        Genera el HTML informativo inicial.
        
        Returns:
            HTML con información inicial
        """
        return """
        <div style="padding: 20px; font-family: Arial, sans-serif;">
            <h2>🗺️ Vista de Mapa Interactivo</h2>
            <p>Esta vista muestra todas las cámaras de tráfico en un mapa interactivo de Málaga.</p>
            
            <h3>Características:</h3>
            <ul>
                <li><strong>Pins de cámaras</strong>: Cada cámara se representa con un pin en su ubicación exacta</li>
                <li><strong>Colores por distrito</strong>: Los pins están coloreados según el distrito al que pertenecen</li>
                <li><strong>Información al hacer click</strong>: Click en un pin para ver detalles de la cámara</li>
                <li><strong>Filtrado por distrito</strong>: Usa el filtro superior para ver solo cámaras de un distrito</li>
                <li><strong>Clustering inteligente</strong>: Las cámaras cercanas se agrupan automáticamente</li>
                <li><strong>Street View</strong>: Haz click derecho en cualquier lugar o usa el enlace en los popups para ver la calle</li>
            </ul>
            
            <h3>Cómo usar:</h3>
            <ol>
                <li>Haz click en <strong>"Actualizar Mapa"</strong> para generar el mapa con los datos actuales</li>
                <li>Haz click en <strong>"Abrir en Navegador"</strong> para ver el mapa completo e interactivo</li>
                <li>Usa los filtros para personalizar la visualización</li>
                <li>En el navegador, haz click en los pins para ver detalles de cada cámara</li>
            </ol>
            
            <p style="color: #666; margin-top: 20px;">
                <em>Nota: El mapa se genera con Folium y se abre en tu navegador web para mejor interactividad.</em>
            </p>
        </div>
        """
    
    def set_cameras(self, cameras: List[Camera]):
        """
        Establece la lista de cámaras a mostrar.
        
        Args:
            cameras: Lista de objetos Camera
        """
        self.cameras = cameras
        self.filtered_cameras = cameras.copy()
        
        # Actualizar contador
        self._update_camera_count()
        
        logger.info(f"MapView: {len(cameras)} cámaras establecidas")
    
    def _update_camera_count(self):
        """
        Actualiza el contador de cámaras visible.
        """
        count = len(self.filtered_cameras)
        self.camera_count_label.setText(f"Cámaras en el mapa: {count}")
    
    def _on_district_filter_changed(self):
        """
        Maneja el cambio en el filtro de distrito.
        """
        district_id = self.district_filter.currentData()
        
        if district_id is None:
            # Mostrar todas
            self.filtered_cameras = self.cameras.copy()
        else:
            # Filtrar por distrito
            self.filtered_cameras = [
                cam for cam in self.cameras 
                if cam.distrito == district_id
            ]
        
        self._update_camera_count()
        logger.info(f"Filtro distrito: {district_id}, cámaras: {len(self.filtered_cameras)}")
    
    def _on_show_districts_changed(self):
        """
        Maneja el cambio en el checkbox de mostrar distritos.
        """
        # Forzar regeneración del mapa si se desea
        pass
    
    def _generate_map(self):
        """
        Genera el mapa interactivo en segundo plano.
        """
        if not self.filtered_cameras:
            logger.warning("No hay cámaras para mostrar en el mapa")
            self.info_frame.setHtml("""
                <div style="padding: 20px; color: #e74c3c;">
                    <h3>⚠️ No hay cámaras para mostrar</h3>
                    <p>Asegúrate de que los datos se hayan cargado correctamente.</p>
                </div>
            """)
            return
            
        self.btn_refresh_map.setEnabled(False)
        self.info_frame.setHtml("""
            <div style="padding: 20px; text-align: center;">
                <h3>🔄 Generando mapa...</h3>
                <p>Por favor espere, esto puede tardar unos segundos.</p>
                <p>Procesando {} cámaras.</p>
            </div>
        """.format(len(self.filtered_cameras)))
        
        # Crear thread y worker
        self.worker_thread = QThread()
        self.worker = MapGenerationWorker(
            self.filtered_cameras, 
            self.show_districts_checkbox.isChecked()
        )
        self.worker.moveToThread(self.worker_thread)
        
        # Conectar señales
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_map_generated)
        self.worker.error.connect(self._on_map_error)
        
        # Limpieza
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker_thread.quit)
        self.worker.error.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.finished.connect(self._on_thread_finished)
        
        # Iniciar
        self.worker_thread.start()
        
    def _on_map_generated(self, map_path: Path, summary_html: str):
        """Callback éxito generación mapa."""
        self.map_html_path = map_path
        self.info_frame.setHtml(summary_html)
        self.btn_open_browser.setEnabled(True)
        self.btn_refresh_map.setEnabled(True)
        
    def _on_map_error(self, error_msg: str):
        """Callback error generación mapa."""
        self.info_frame.setHtml(f"""
            <div style="padding: 20px; color: #e74c3c;">
                <h3>❌ Error generando mapa</h3>
                <p>{error_msg}</p>
            </div>
        """)
        self.btn_refresh_map.setEnabled(True)
        
    def _on_thread_finished(self):
        """Limpieza."""
        self.worker_thread = None
        self.worker = None
    
    def _create_legend_html(self) -> str:
        """
        Crea el HTML para la leyenda de distritos.
        
        Returns:
            HTML de la leyenda
        """
        legend_items = []
        for district_id, color in sorted(config.DISTRICT_COLORS.items()):
            legend_items.append(
                f'<div><span style="background: {color}; width: 15px; height: 15px; '
                f'display: inline-block; margin-right: 5px; border-radius: 3px;"></span>'
                f'Distrito {district_id}</div>'
            )
        
        return f"""
        <div style="
            position: fixed; 
            bottom: 50px; 
            right: 50px; 
            width: 200px; 
            background: white; 
            border: 2px solid #ccc; 
            border-radius: 5px; 
            padding: 10px;
            font-family: Arial, sans-serif;
            font-size: 12px;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        ">
            <h4 style="margin: 0 0 10px 0; font-size: 14px;">📍 Distritos</h4>
            {''.join(legend_items)}
        </div>
        """
    
    def _open_in_browser(self):
        """
        Abre el mapa generado en el navegador web predeterminado.
        """
        if not self.map_html_path or not self.map_html_path.exists():
            logger.warning("No hay mapa generado para abrir")
            return
        
        try:
            url = QUrl.fromLocalFile(str(self.map_html_path.absolute()))
            QDesktopServices.openUrl(url)
            logger.info(f"Mapa abierto en navegador: {self.map_html_path}")
        except Exception as e:
            logger.error(f"Error abriendo mapa en navegador: {e}", exc_info=True)
