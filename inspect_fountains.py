
import logging
import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("InspectFountains")

URL = "https://datosabiertos.malaga.eu/recursos/ambiente/fuentesaguapotable/da_medioAmbiente_fuentes-4326.geojson"

def inspect():
    logger.info(f"--- INSPECTING FOUNTAINS ---")
    try:
        response = requests.get(URL, timeout=10)
        data = response.json()
        features = data.get('features', [])
        if not features:
            logger.warning("No features found.")
            return

        # Inspect first feature properties
        props = features[0].get('properties', {})
        logger.info(f"Fields: {list(props.keys())}")
        
    except Exception as e:
        logger.error(f"Failed: {e}")

if __name__ == "__main__":
    inspect()
