
import logging
import requests
import folium
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VerifyLayer")

BIKE_LANES_URL = "https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_carrilesBici-4326.geojson"

def test_fetches_and_creates_layer():
    logger.info("Testing fetch of Bike Lanes...")
    try:
        response = requests.get(BIKE_LANES_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        feature_count = len(data.get('features', []))
        logger.info(f"Fetched {feature_count} Bike Lane features.")
        
        m = folium.Map(location=[36.721274, -4.421399], zoom_start=13)
        
        bike_group = folium.FeatureGroup(name="🚲 Carriles Bici", show=False)
        
        folium.GeoJson(
            data,
            name="Carriles Bici",
            style_function=lambda feature: {
                'color': '#3498db',
                'weight': 3,
                'opacity': 0.8
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['NOMBRE', 'DESCRIPCION'],
                aliases=['Tramo:', 'Info:'],
                localize=True
            ),
            popup=folium.GeoJsonPopup(
                fields=['NOMBRE', 'DESCRIPCION', 'LONGITUDTOTAL'],
                aliases=['Tramo', 'Descripción', 'Longitud (m)'],
                localize=True,
                max_width=300
            )
        ).add_to(bike_group)
        
        bike_group.add_to(m)
        logger.info("Layer added successfully.")
        
        output_file = "test_bike_lanes_map.html"
        m.save(output_file)
        logger.info(f"Map saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_fetches_and_creates_layer()
