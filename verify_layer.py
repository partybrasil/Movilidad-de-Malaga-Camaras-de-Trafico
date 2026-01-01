
import logging
import requests
import folium
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VerifyLayer")

TRAFFIC_CUTS_URL = "https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_cortesTrafico-4326.geojson"

def test_fetches_and_creates_layer():
    logger.info("Testing fetch...")
    try:
        response = requests.get(TRAFFIC_CUTS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Fetched {len(data.get('features', []))} features.")
        
        m = folium.Map(location=[36.721274, -4.421399], zoom_start=13)
        
        # Logic copied from workers.py
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
        logger.info("Layer added successfully.")
        
        output_file = "test_traffic_cuts_map.html"
        m.save(output_file)
        logger.info(f"Map saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_fetches_and_creates_layer()
