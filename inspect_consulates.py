
import logging
import requests
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InspectConsulates")

CONSULATES_URL = "https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_consulados-4326.geojson"

def inspect_data():
    logger.info("Fetching Consulates data...")
    try:
        response = requests.get(CONSULATES_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        features = data.get('features', [])
        logger.info(f"Fetched {len(features)} features.")
        
        # Collect unique tooltips/names to guess countries
        names = set()
        for f in features:
            props = f.get('properties', {})
            name = props.get('TOOLTIP', '') or props.get('NOMBRE', '')
            names.add(name)
            
        logger.info(f"Unique Names: {sorted(list(names))}")
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    inspect_data()
