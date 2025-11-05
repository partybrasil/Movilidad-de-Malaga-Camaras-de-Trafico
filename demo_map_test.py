#!/usr/bin/env python3
"""
Script de prueba para la funcionalidad de mapa interactivo.

Este script genera un mapa de prueba con cámaras simuladas
para demostrar la funcionalidad sin necesidad de ejecutar la GUI completa.
"""

import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from src.models.camera import Camera
from src.utils.coordinate_converter import get_converter
import folium
from folium import plugins
import config


def main():
    """
    Genera un mapa de prueba con cámaras simuladas.
    """
    print("=" * 80)
    print("DEMO: Vista de Mapa Interactivo - Cámaras de Tráfico Málaga")
    print("=" * 80)
    print()
    
    # Crear cámaras de prueba basadas en ubicaciones reales de Málaga
    test_cameras = [
        Camera(
            id=1,
            nombre="TV103-A-Centro",
            direccion="Alameda Principal - Centro Histórico",
            url_imagen="https://movilidad.malaga.eu/img/cam1.jpg",
            url="https://movilidad.malaga.eu/camaras/1",
            coordenadas=(374500, 4065200),  # UTM zona 30N (Centro)
            distrito="1",
            acceso="PMR"
        ),
        Camera(
            id=2,
            nombre="TV104-B-Malagueta",
            direccion="Paseo Marítimo Pablo Ruiz Picasso",
            url_imagen="https://movilidad.malaga.eu/img/cam2.jpg",
            url="https://movilidad.malaga.eu/camaras/2",
            coordenadas=(375800, 4064800),  # Malagueta
            distrito="2",
            acceso="PMR"
        ),
        Camera(
            id=3,
            nombre="TV105-C-Puerto",
            direccion="Muelle Heredia - Puerto de Málaga",
            url_imagen="https://movilidad.malaga.eu/img/cam3.jpg",
            url="https://movilidad.malaga.eu/camaras/3",
            coordenadas=(374200, 4064500),  # Puerto
            distrito="1",
            acceso=None
        ),
        Camera(
            id=4,
            nombre="TV106-D-Teatinos",
            direccion="Campus de Teatinos - Universidad",
            url_imagen="https://movilidad.malaga.eu/img/cam4.jpg",
            url="https://movilidad.malaga.eu/camaras/4",
            coordenadas=(369000, 4069000),  # Teatinos
            distrito="11",
            acceso="PMR"
        ),
        Camera(
            id=5,
            nombre="TV107-E-Carretera-Cadiz",
            direccion="Carretera de Cádiz - Zona Oeste",
            url_imagen="https://movilidad.malaga.eu/img/cam5.jpg",
            url="https://movilidad.malaga.eu/camaras/5",
            coordenadas=(368500, 4063000),  # Carretera de Cádiz
            distrito="7",
            acceso="PMR"
        ),
    ]
    
    print(f"📹 Cámaras de prueba creadas: {len(test_cameras)}")
    for cam in test_cameras:
        print(f"   • {cam.nombre} (Distrito {cam.distrito})")
    print()
    
    # Inicializar conversor de coordenadas
    converter = get_converter()
    print("🔄 Conversor de coordenadas EPSG:25830 → WGS84 inicializado")
    print()
    
    # Crear mapa centrado en Málaga
    m = folium.Map(
        location=[config.MAP_CENTER_LAT, config.MAP_CENTER_LON],
        zoom_start=config.MAP_DEFAULT_ZOOM,
        tiles=config.MAP_TILE_LAYER,
        control_scale=True
    )
    print(f"🗺️  Mapa base creado: Centro ({config.MAP_CENTER_LAT}, {config.MAP_CENTER_LON})")
    
    # Añadir título al mapa
    title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 400px; height: 80px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:16px; padding: 10px; border-radius: 5px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.3);">
            <h3 style="margin: 0; color: #e74c3c;">🚦 Cámaras de Tráfico - Málaga</h3>
            <p style="margin: 5px 0 0 0; font-size: 12px; color: #7f8c8d;">
                Vista de Mapa Interactivo • Click en los pins para más info
            </p>
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Añadir clustering para mejor performance
    marker_cluster = plugins.MarkerCluster(
        name="Cámaras de Tráfico",
        overlay=True,
        control=True
    ).add_to(m)
    print("📍 Sistema de clustering añadido")
    print()
    
    # Añadir marcadores para cada cámara
    cameras_added = 0
    print("📌 Procesando cámaras:")
    
    for camera in test_cameras:
        if not camera.coordenadas:
            print(f"   ⚠️  Cámara {camera.id} sin coordenadas, omitida")
            continue
        
        x, y = camera.coordenadas
        
        # Convertir coordenadas UTM a lat/lon
        coords = converter.convert(x, y)
        if not coords:
            print(f"   ❌ Error convirtiendo coordenadas de cámara {camera.id}")
            continue
        
        lon, lat = coords
        
        # Determinar color según distrito
        color = config.DISTRICT_COLORS.get(
            camera.distrito if camera.distrito else "0",
            "#95a5a6"  # Gris por defecto
        )
        
        # Crear popup con información detallada
        popup_html = f"""
        <div style="width: 280px; font-family: Arial, sans-serif;">
            <h4 style="margin: 0 0 10px 0; color: {color}; border-bottom: 2px solid {color}; padding-bottom: 5px;">
                📹 {camera.nombre}
            </h4>
            <p style="margin: 8px 0;"><strong>📍 Ubicación:</strong><br>{camera.direccion}</p>
            <p style="margin: 8px 0;"><strong>🏛️ Distrito:</strong> {camera.get_distrito_display()}</p>
            {'<p style="margin: 8px 0;"><strong>♿ Acceso:</strong> ' + camera.acceso + '</p>' if camera.acceso else ''}
            
            <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #ecf0f1;">
                <p style="margin: 5px 0;">
                    <a href="{camera.url}" target="_blank" 
                       style="color: #3498db; text-decoration: none; font-weight: bold;">
                        🔗 Ver en web oficial →
                    </a>
                </p>
                <p style="margin: 5px 0;">
                    <a href="{camera.url_imagen}" target="_blank" 
                       style="color: #3498db; text-decoration: none; font-weight: bold;">
                        📷 Ver imagen actual →
                    </a>
                </p>
            </div>
            
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #ecf0f1; 
                        font-size: 10px; color: #95a5a6;">
                <strong>Datos técnicos:</strong><br>
                ID: {camera.id} | UTM: {x:.0f}, {y:.0f}<br>
                WGS84: {lat:.6f}°N, {lon:.6f}°W
            </div>
        </div>
        """
        
        # Crear marcador con icono personalizado
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"<strong>{camera.nombre}</strong><br>{camera.direccion}",
            icon=folium.Icon(
                color='red',
                icon='video-camera',
                prefix='fa'
            )
        ).add_to(marker_cluster)
        
        cameras_added += 1
        print(f"   ✓ {camera.nombre}")
        print(f"      UTM({x:.0f}, {y:.0f}) → WGS84({lat:.6f}, {lon:.6f})")
    
    print()
    print(f"✅ {cameras_added} marcadores añadidos al mapa")
    print()
    
    # Añadir leyenda de distritos
    legend_items = []
    for district_id, color in sorted(config.DISTRICT_COLORS.items()):
        legend_items.append(
            f'<div style="margin: 3px 0;">'
            f'<span style="background: {color}; width: 15px; height: 15px; '
            f'display: inline-block; margin-right: 8px; border-radius: 3px; '
            f'border: 1px solid #ddd;"></span>'
            f'<span style="font-size: 13px;">Distrito {district_id}</span>'
            f'</div>'
        )
    
    legend_html = f"""
    <div style="
        position: fixed; 
        bottom: 50px; 
        right: 50px; 
        width: 180px; 
        background: white; 
        border: 2px solid #ccc; 
        border-radius: 8px; 
        padding: 12px;
        font-family: Arial, sans-serif;
        z-index: 1000;
        box-shadow: 0 3px 15px rgba(0,0,0,0.3);
    ">
        <h4 style="margin: 0 0 12px 0; font-size: 15px; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px;">
            📍 Leyenda de Distritos
        </h4>
        {''.join(legend_items)}
        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #ecf0f1; font-size: 10px; color: #7f8c8d;">
            {len(config.DISTRICT_COLORS)} distritos de Málaga
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    print("🎨 Leyenda de distritos añadida")
    
    # Añadir control de capas
    folium.LayerControl().add_to(m)
    
    # Guardar mapa
    output_path = Path(__file__).parent / "demo_mapa_camaras.html"
    m.save(str(output_path))
    
    print()
    print("=" * 80)
    print("✨ MAPA GENERADO EXITOSAMENTE")
    print("=" * 80)
    print(f"📁 Archivo: {output_path}")
    print(f"📊 Tamaño: {output_path.stat().st_size:,} bytes")
    print()
    print("🌐 Para visualizar el mapa:")
    print(f"   1. Abre en tu navegador: file://{output_path.absolute()}")
    print("   2. O ejecuta: xdg-open demo_mapa_camaras.html")
    print()
    print("📝 Características del mapa:")
    print("   • Pins interactivos con información detallada")
    print("   • Colores por distrito")
    print("   • Clustering automático")
    print("   • Popups con enlaces a cámara y datos técnicos")
    print("   • Leyenda de distritos")
    print("   • Control de capas")
    print()
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Ejecución interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
