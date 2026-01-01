"""
Workers en segundo plano para tareas pesadas.

Este módulo contiene clases QObject diseñadas para ejecutarse en hilos separados (QThread)
y evitar congelar la interfaz de usuario durante operaciones bloqueantes.
"""

import logging
from pathlib import Path
from typing import List, Optional, Tuple
import tempfile
import json
import requests
import folium
from folium import plugins

from PySide6.QtCore import QObject, Signal

from src.models.camera import Camera
from src.utils.data_loader import DataLoader
from src.utils.coordinate_converter import get_converter
import config

TRAFFIC_CUTS_URL = "https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_cortesTrafico-4326.geojson"
CLOTHING_CONTAINERS_URL = "https://datosabiertos.malaga.eu/recursos/ambiente/contenedores/da_medioAmbiente_contenedoresRopa-4326.geojson"
CONSULATES_URL = "https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_consulados-4326.geojson"

# Mapping for flags (Name fragment -> ISO code)
COUNTRY_FLAGS = {
    'Costa Rica': 'cr', 'Ecuador': 'ec', 'Mónaco': 'mc', 'Turquía': 'tr', 
    'Panamá': 'pa', 'Paraguay': 'py', 'Arabia Saudi': 'sa', 'Dinamarca': 'dk', 
    'Armenia': 'am', 'Austria': 'at', 'Canadá': 'ca', 'Chile': 'cl', 
    'Eslovaquia': 'sk', 'Filipinas': 'ph', 'Finlandia': 'fi', 'Francia': 'fr', 
    'Hungría': 'hu', 'Luxemburgo': 'lu', 'Portugal': 'pt', 'Suecia': 'se', 
    'Ucrania': 'ua', 'Uruguay': 'uy', 'Alemania': 'de', 'Brasil': 'br', 
    'Albania': 'al', 'Reino Unido': 'gb', 'Polonia': 'pl', 'Italia': 'it'
}

logger = logging.getLogger(__name__)


class DataLoadWorker(QObject):
    """
    Worker para cargar datos en segundo plano.
    """
    finished = Signal(bool, list)  # success, cameras
    progress = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.data_loader = DataLoader()
        
    def run(self):
        """
        Ejecuta la carga de datos.
        """
        logger.info("Iniciando carga de datos en segundo plano...")
        self.progress.emit("Conectando con servidor de datos...")
        
        success = self.data_loader.load_data()
        
        if success:
            cameras = self.data_loader.get_cameras()
            logger.info(f"Carga en segundo plano completada: {len(cameras)} cámaras")
            self.finished.emit(True, cameras)
        else:
            logger.error("Fallo en carga de datos en segundo plano")
            self.finished.emit(False, [])


class MapGenerationWorker(QObject):
    """
    Worker para generar el mapa en segundo plano.
    """
    finished = Signal(Path, str)  # path_to_html, summary_html
    error = Signal(str)
    
    def __init__(self, cameras: List[Camera], show_districts: bool):
        super().__init__()
        self.cameras = cameras
        self.show_districts = show_districts
        self.converter = get_converter()
        
    def run(self):
        """
        Genera el mapa con Folium.
        """
        logger.info(f"Iniciando generación de mapa en segundo plano ({len(self.cameras)} cámaras)...")
        
        try:
            if not self.cameras:
                raise ValueError("No hay cámaras para procesar")

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
            
            # Contadores
            cameras_with_coords = 0
            cameras_without_coords = 0
            
            # Añadir marcadores
            for camera in self.cameras:
                if not camera.coordenadas:
                    cameras_without_coords += 1
                    continue
                
                x, y = camera.coordenadas
                
                # Convertir coordenadas
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
                
                # Popup HTML
                popup_html = self._create_popup_html(camera, lat, lon, color)
                
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
            
            # --- Añadir capa de Cortes de Tráfico ---
            try:
                self._add_traffic_cuts_layer(m)
            except Exception as e:
                logger.error(f"Error añadiendo capa de cortes de tráfico: {e}")

            # --- Añadir capa de Contenedores de Ropa ---
            try:
                self._add_clothing_containers_layer(m)
            except Exception as e:
                logger.error(f"Error añadiendo capa de contenedores de ropa: {e}")

            # --- Añadir capa de Consulados ---
            try:
                self._add_consulates_layer(m)
            except Exception as e:
                logger.error(f"Error añadiendo capa de consulados: {e}")

            # Añadir controles y scripts
            folium.LayerControl().add_to(m)
            
            if self.show_districts:
                legend_html = self._create_legend_html()
                m.get_root().html.add_child(folium.Element(legend_html))
            
            self._add_scripts(m)
            
            # Guardar mapa
            temp_dir = Path(tempfile.gettempdir())
            map_path = temp_dir / "malaga_camaras_mapa.html"
            m.save(str(map_path))
            
            # Generar resumen
            summary = self._create_summary_html(cameras_with_coords, cameras_without_coords, map_path)
            
            logger.info(f"Mapa generado exitosamente en segundo plano: {map_path}")
            self.finished.emit(map_path, summary)
            
        except Exception as e:
            logger.error(f"Error generando mapa en thread: {e}", exc_info=True)
            self.error.emit(str(e))

    def _add_traffic_cuts_layer(self, m):
        """Descarga y añade la capa de cortes de tráfico."""
        logger.info("Descargando datos de cortes de tráfico...")
        response = requests.get(TRAFFIC_CUTS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Grupo para cortes de tráfico
        cuts_group = folium.FeatureGroup(name="⚠️ Cortes de Tráfico", show=True)
        
        def style_function(feature):
            props = feature.get('properties', {})
            tipo = props.get('TIPOAFECTACION', '')
            
            color = 'red' if 'Corte' in tipo else 'orange'
            return {
                'fillColor': color,
                'color': color,
                'weight': 2,
                'fillOpacity': 0.6
            }
            
        def highlight_function(feature):
            return {
                'weight': 4,
                'fillOpacity': 0.8
            }

        folium.GeoJson(
            data,
            name="Cortes de Tráfico",
            style_function=style_function,
            highlight_function=highlight_function,
            tooltip=folium.GeoJsonTooltip(
                fields=['DIRECCION', 'TIPOAFECTACION', 'DESDE', 'HASTA'],
                aliases=['📍 Ubicación:', '⚠️ Tipo:', '📅 Desde:', '📅 Hasta:'],
                localize=True
            ),
            popup=folium.GeoJsonPopup(
                fields=['NOMBRE', 'DESCRIPCION', 'DIRECCION', 'TIPOAFECTACION', 'TIPOCORTE', 'DESDE', 'HASTA', 'NOTAS'],
                aliases=['Nombre', 'Descripción', 'Dirección', 'Afectación', 'Tipo', 'Inicio', 'Fin', 'Notas'],
                localize=True,
                max_width=300
            ),
            marker=folium.Marker(icon=folium.Icon(icon='exclamation-triangle', prefix='fa', color='red'))
        ).add_to(cuts_group)
        
        cuts_group.add_to(m)
        logger.info("Capa de cortes de tráfico añadida.")

    def _add_clothing_containers_layer(self, m):
        """Descarga y añade la capa de contenedores de ropa."""
        logger.info("Descargando datos de contenedores de ropa...")
        response = requests.get(CLOTHING_CONTAINERS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Grupo para contenedores
        containers_group = folium.FeatureGroup(name="👕 Contenedores de Ropa", show=False)
        
        folium.GeoJson(
            data,
            name="Contenedores de Ropa",
            tooltip=folium.GeoJsonTooltip(
                fields=['DIRECCION', 'NOMBRE'],
                aliases=['📍 Ubicación:', '📦 Tipo:'],
                localize=True
            ),
            popup=folium.GeoJsonPopup(
                fields=['NOMBRE', 'DIRECCION', 'DESCRIPCION', 'TITULARIDAD'],
                aliases=['Nombre', 'Dirección', 'Descripción', 'Titularidad'],
                localize=True,
                max_width=300
            ),
            marker=folium.Marker(icon=folium.Icon(icon='recycle', prefix='fa', color='green'))
        ).add_to(containers_group)
        
        containers_group.add_to(m)
        logger.info("Capa de contenedores de ropa añadida.")

    def _add_consulates_layer(self, m):
        """Descarga y añade la capa de consulados con banderas."""
        logger.info("Descargando datos de consulados...")
        response = requests.get(CONSULATES_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Grupo para consulados
        consulates_group = folium.FeatureGroup(name="🏳️ Consulados", show=False)
        
        for feature in data.get('features', []):
            try:
                props = feature.get('properties', {})
                geometry = feature.get('geometry', {})
                if not geometry or geometry.get('type') != 'Point':
                    continue
                    
                lat, lon = geometry.get('coordinates')[1], geometry.get('coordinates')[0]
                name = props.get('TOOLTIP', '') or props.get('NOMBRE', 'Consulado')
                
                # Determine flag
                iso_code = 'un' # United Nations / Default
                for key, code in COUNTRY_FLAGS.items():
                    if key.lower() in name.lower():
                        iso_code = code
                        break
                        
                # Custom Icon with Flag
                icon_url = f"https://flagcdn.com/w40/{iso_code}.png"
                
                popup_html = f"""
                <div style="font-family: Arial; min-width: 200px;">
                    <h4 style="margin: 0 0 8px 0;">{name}</h4>
                    <img src="{icon_url}" style="width: 30px; border: 1px solid #ccc; margin-bottom: 8px;">
                    <p style="margin: 4px 0;"><strong>Dirección:</strong><br>{props.get('DIRECCION', 'N/D')}</p>
                    <p style="margin: 4px 0;"><strong>Info:</strong><br>{props.get('FINALIDAD', '')}</p>
                </div>
                """
                
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=name,
                    icon=folium.CustomIcon(
                        icon_image=icon_url,
                        icon_size=(30, 20),
                        icon_anchor=(15, 10),
                        popup_anchor=(0, -10)
                    )
                ).add_to(consulates_group)
                
            except Exception as e:
                logger.warning(f"Error procesando consulado: {e}")
                continue
        
        consulates_group.add_to(m)
        logger.info("Capa de consulados añadida.")

    def _create_popup_html(self, camera: Camera, lat: float, lon: float, color: str) -> str:
        """Helper para crear el HTML del popup."""
        return f"""
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
                ID: {camera.id} | Coords: {lat:.5f}, {lon:.5f}
            </p>
        </div>
        """

    def _create_legend_html(self) -> str:
        """Helper para la leyenda."""
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
        
    def _add_scripts(self, m):
        """Añade scripts JS al mapa."""
        map_var_name = m.get_name()
        js_script = f"""
        <script>
            function openStreetView(lat, lon) {{
                var url = "https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=" + lat + "," + lon;
                window.open(url, '_blank');
            }}
            
            window.addEventListener('load', function() {{
                var mapInstance = {map_var_name};
                
                if (mapInstance) {{
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
                    
                    mapInstance.on('popupopen', function(e) {{
                        var popupNode = e.popup._contentNode;
                        var img = popupNode.querySelector('.camera-live-feed');
                        var select = popupNode.querySelector('.camera-interval-select');
                        
                        if (img && select) {{
                            var url = img.getAttribute('data-url');
                            var timerId = null;
                            
                            function refreshImage() {{
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
                            
                            select.addEventListener('change', updateTimer);
                            updateTimer();
                        }}
                    }});
                    
                    mapInstance.on('popupclose', function(e) {{
                        if (e.popup._cameraTimer) {{
                            clearInterval(e.popup._cameraTimer);
                            e.popup._cameraTimer = null;
                        }}
                    }});
                }}
            }});
        </script>
        """
        m.get_root().html.add_child(folium.Element(js_script))
        
    def _create_summary_html(self, with_coords, without_coords, path):
        """Helper para el resumen HTML."""
        return f"""
        <div style="padding: 20px; font-family: Arial, sans-serif;">
            <h3 style="color: #27ae60;">✓ Mapa generado exitosamente</h3>
            <p><strong>Cámaras procesadas:</strong> {with_coords}</p>
            <p><strong>Cámaras sin coordenadas:</strong> {without_coords}</p>
            <p style="margin-top: 15px;">
                El mapa ha sido generado correctamente. 
                Haz click en <strong>"Abrir en Navegador"</strong> para verlo.
            </p>
            <p style="color: #7f8c8d; font-size: 11px; margin-top: 20px;">
                Archivo: {path}
            </p>
        </div>
        """
