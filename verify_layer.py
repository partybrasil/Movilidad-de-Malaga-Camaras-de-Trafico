
import logging
import requests
import folium
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VerifyLayer")

CONSULATES_URL = "https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_consulados-4326.geojson"

COUNTRY_FLAGS = {
    'Costa Rica': 'cr', 'Ecuador': 'ec', 'Mónaco': 'mc', 'Turquía': 'tr', 
    'Panamá': 'pa', 'Paraguay': 'py', 'Arabia Saudi': 'sa', 'Dinamarca': 'dk', 
    'Armenia': 'am', 'Austria': 'at', 'Canadá': 'ca', 'Chile': 'cl', 
    'Eslovaquia': 'sk', 'Filipinas': 'ph', 'Finlandia': 'fi', 'Francia': 'fr', 
    'Hungría': 'hu', 'Luxemburgo': 'lu', 'Portugal': 'pt', 'Suecia': 'se', 
    'Ucrania': 'ua', 'Uruguay': 'uy', 'Alemania': 'de', 'Brasil': 'br', 
    'Albania': 'al', 'Reino Unido': 'gb', 'Polonia': 'pl', 'Italia': 'it'
}

def test_fetches_and_creates_layer():
    logger.info("Testing fetch of Consulates...")
    try:
        response = requests.get(CONSULATES_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        feature_count = len(data.get('features', []))
        logger.info(f"Fetched {feature_count} Consulates features.")
        
        m = folium.Map(location=[36.721274, -4.421399], zoom_start=13)
        
        consulates_group = folium.FeatureGroup(name="🏳️ Consulados", show=False)
        
        processed_count = 0
        for feature in data.get('features', []):
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
            
            # Count how many we successfully mapped
            if iso_code != 'un':
                processed_count += 1
                
            icon_url = f"https://flagcdn.com/w40/{iso_code}.png"
            
            # Partial check logic
            folium.Marker(
                location=[lat, lon],
                tooltip=name
            ).add_to(consulates_group)
        
        consulates_group.add_to(m)
        logger.info(f"Layer added successfully. Mapped flags for {processed_count}/{feature_count} consulates.")
        
        output_file = "test_consulates_map.html"
        m.save(output_file)
        logger.info(f"Map saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_fetches_and_creates_layer()
