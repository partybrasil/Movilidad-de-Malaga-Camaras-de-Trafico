
import logging
import requests
import folium
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VerifyLayer")

CLOTHING_CONTAINERS_URL = "https://datosabiertos.malaga.eu/recursos/ambiente/contenedores/da_medioAmbiente_contenedoresRopa-4326.geojson"

def test_fetches_and_creates_layer():
    logger.info("Testing fetch of Clothing Containers...")
    try:
        response = requests.get(CLOTHING_CONTAINERS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Fetched {len(data.get('features', []))} Clothing Container features.")
        
        m = folium.Map(location=[36.721274, -4.421399], zoom_start=13)
        
        # Logic copied from workers.py
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
        logger.info("Layer added successfully.")
        
        output_file = "test_clothing_containers_map.html"
        m.save(output_file)
        logger.info(f"Map saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_fetches_and_creates_layer()
