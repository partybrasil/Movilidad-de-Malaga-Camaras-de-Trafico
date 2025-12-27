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
from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtGui import QDesktopServices

import folium
from folium import plugins

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
        Genera el mapa interactivo con folium.
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
        
        try:
            # Crear mapa centrado en Málaga
            m = folium.Map(
                location=[config.MAP_CENTER_LAT, config.MAP_CENTER_LON],
                zoom_start=config.MAP_DEFAULT_ZOOM,
                tiles=config.MAP_TILE_LAYER
            )
            
            # Añadir capa de clustering para mejor performance
            marker_cluster = plugins.MarkerCluster(
                name="Cámaras de Tráfico",
                overlay=True,
                control=True,
                icon_create_function=None
            ).add_to(m)
            
            # Contador de cámaras procesadas
            cameras_with_coords = 0
            cameras_without_coords = 0
            
            # Añadir marcadores para cada cámara
            for camera in self.filtered_cameras:
                if not camera.coordenadas:
                    cameras_without_coords += 1
                    continue
                
                x, y = camera.coordenadas
                
                # Convertir coordenadas UTM a lat/lon
                coords = self.converter.convert(x, y)
                if not coords:
                    cameras_without_coords += 1
                    continue
                
                lon, lat = coords
                cameras_with_coords += 1
                
                # Determinar color según distrito
                color = config.DISTRICT_COLORS.get(
                    camera.distrito if camera.distrito else "0",
                    "#95a5a6"  # Gris por defecto
                )
                
                # Crear popup con información de la cámara
                popup_html = f"""
                <div style="width: 300px; font-family: Arial, sans-serif;">
                    <h4 style="margin: 0 0 10px 0; color: {color};">📹 {camera.nombre}</h4>
                    
                    <!-- Mini Player & Controls -->
                    <div class="camera-player" style="margin-bottom: 10px;">
                        <img src="{camera.url_imagen}" 
                             class="camera-live-feed" 
                             data-url="{camera.url_imagen}"
                             style="width: 100%; border-radius: 4px; border: 1px solid #ddd; min-height: 150px; background: #f0f0f0;">
                        
                        <div style="margin-top: 8px; display: flex; align-items: center; justify-content: space-between; background: #f1f2f6; padding: 6px 10px; border-radius: 4px;">
                            <span style="font-size: 12px; font-weight: bold; color: #2c3e50;">⏱️ Actualizar:</span>
                            <select class="camera-interval-select" style="font-size: 12px; padding: 2px 5px; border: 1px solid #bdc3c7; border-radius: 3px;">
                                <option value="1">1 s</option>
                                <option value="3">3 s</option>
                                <option value="5" selected>5 s</option>
                                <option value="10">10 s</option>
                                <option value="15">15 s</option>
                                <option value="20">20 s</option>
                            </select>
                        </div>
                    </div>

                    <p style="margin: 5px 0;"><strong>Ubicación:</strong><br>{camera.direccion}</p>
                    <p style="margin: 5px 0;"><strong>Distrito:</strong> {camera.get_distrito_display()}</p>
                    {'<p style="margin: 5px 0;"><strong>Acceso:</strong> ' + camera.acceso + '</p>' if camera.acceso else ''}
                    <p style="margin: 10px 0 5px 0;">
                        <a href="{camera.url}" target="_blank" style="color: #3498db;">🔗 Ver en web oficial</a>
                    </p>
                    <p style="margin: 5px 0;">
                        <a href="{config.STREET_VIEW_URL_TEMPLATE.format(lat=lat, lon=lon)}" target="_blank" style="color: #e67e22; font-weight: bold;">
                            🚶 Ver en Street View
                        </a>
                    </p>
                    <p style="margin-top: 10px; font-size: 10px; color: #7f8c8d;">
                        ID: {camera.id} | Coords: {x:.0f}, {y:.0f}
                    </p>
                </div>
                """
                
                # Crear marcador
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=320),
                    tooltip=f"{camera.nombre}",
                    icon=folium.Icon(
                        color='blue' if not camera.distrito else 'red',
                        icon='video-camera',
                        prefix='fa'
                    )
                ).add_to(marker_cluster)
            
            # Añadir capas adicionales
            folium.LayerControl().add_to(m)
            
            # Añadir leyenda de distritos si está habilitado
            if self.show_districts_checkbox.isChecked():
                legend_html = self._create_legend_html()
                m.get_root().html.add_child(folium.Element(legend_html))
            
            # --- Integración de Scripts (Street View + Auto Refresh) ---
            map_var_name = m.get_name()
            js_script = f"""
            <script>
                function openStreetView(lat, lon) {{
                    var url = "https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=" + lat + "," + lon;
                    window.open(url, '_blank');
                }}
                
                // Esperar a que el mapa esté listo
                window.addEventListener('load', function() {{
                    // Obtener instancia del mapa
                    var mapInstance = {map_var_name};
                    
                    if (mapInstance) {{
                        // --- Click Derecho Street View ---
                        mapInstance.on('contextmenu', function(e) {{
                            var lat = e.latlng.lat;
                            var lon = e.latlng.lng;
                            
                            var content = '<div style="font-family: Arial; padding: 8px; cursor: pointer; text-align: center;">' +
                                          '<div style="color: #e67e22; font-weight: bold; margin-bottom: 4px;">🚶 Street View</div>' +
                                          '<button onclick="openStreetView(' + lat + ',' + lon + ')" ' +
                                          'style="background: #34495e; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer;">' +
                                          'Ver aquí</button></div>';
                                          
                            L.popup()
                                .setLatLng(e.latlng)
                                .setContent(content)
                                .openOn(mapInstance);
                        }});
                        
                        // --- Auto Refresh de Cámaras ---
                        mapInstance.on('popupopen', function(e) {{
                            var popupNode = e.popup._contentNode;
                            var img = popupNode.querySelector('.camera-live-feed');
                            var select = popupNode.querySelector('.camera-interval-select');
                            
                            if (img && select) {{
                                var url = img.getAttribute('data-url');
                                var timerId = null;
                                
                                function refreshImage() {{
                                    // Añadir timestamp para evitar caché
                                    var uniqueUrl = url + (url.indexOf('?') >= 0 ? '&' : '?') + '_t=' + new Date().getTime();
                                    img.src = uniqueUrl;
                                }}
                                
                                function updateTimer() {{
                                    if (timerId) clearInterval(timerId);
                                    var intervalSec = parseInt(select.value);
                                    if (intervalSec > 0) {{
                                        timerId = setInterval(refreshImage, intervalSec * 1000);
                                    }}
                                    e.popup._cameraTimer = timerId;
                                }}
                                
                                // Escuchar cambios
                                select.addEventListener('change', updateTimer);
                                
                                // Iniciar inmediatamente
                                updateTimer();
                            }}
                        }});
                        
                        mapInstance.on('popupclose', function(e) {{
                            // Limpiar timer si existe
                            if (e.popup._cameraTimer) {{
                                clearInterval(e.popup._cameraTimer);
                                e.popup._cameraTimer = null;
                            }}
                        }});
                        
                        console.log("Map enhancements initialized (Street View + Camera Player)");
                    }}
                }});
            </script>
            """
            m.get_root().html.add_child(folium.Element(js_script))
            
            # Guardar mapa en archivo temporal
            temp_dir = Path(tempfile.gettempdir())
            self.map_html_path = temp_dir / "malaga_camaras_mapa.html"
            m.save(str(self.map_html_path))
            
            # Habilitar botón de abrir en navegador
            self.btn_open_browser.setEnabled(True)
            
            # Actualizar info frame
            self.info_frame.setHtml(f"""
                <div style="padding: 20px; font-family: Arial, sans-serif;">
                    <h3 style="color: #27ae60;">✓ Mapa generado exitosamente</h3>
                    <p><strong>Cámaras procesadas:</strong> {cameras_with_coords}</p>
                    <p><strong>Cámaras sin coordenadas:</strong> {cameras_without_coords}</p>
                    <p style="margin-top: 15px;">
                        El mapa ha sido generado correctamente. 
                        Haz click en <strong>"Abrir en Navegador"</strong> para verlo.
                    </p>
                    <p style="color: #7f8c8d; font-size: 11px; margin-top: 20px;">
                        Archivo: {self.map_html_path}
                    </p>
                </div>
            """)
            
            logger.info(f"Mapa generado: {cameras_with_coords} cámaras, guardado en {self.map_html_path}")
            
        except Exception as e:
            logger.error(f"Error generando mapa: {e}", exc_info=True)
            self.info_frame.setHtml(f"""
                <div style="padding: 20px; color: #e74c3c;">
                    <h3>❌ Error generando mapa</h3>
                    <p>{str(e)}</p>
                </div>
            """)
    
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
