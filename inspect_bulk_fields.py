
import logging
import requests
import json
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("InspectBulk")

URLS = {
    "TAXIS": "https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_paradasTaxi-4326.geojson",
    "EMT": "https://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTLineasYParadas/lineasyparadas.geojson",
    "ECOPOINTS": "https://datosabiertos.malaga.eu/recursos/energia/ecopuntos/da_ecopuntos-4326.geojson",
    "PARKING": "https://datosabiertos.malaga.eu/recursos/aparcamientos/ubappublicosmun/da_aparcamientosPublicosMunicipales-4326.geojson",
    "WIFI": "https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/sedesWifi/da_sedesWifi-4326.geojson", 
    "DOG_PARKS": "https://datosabiertos.malaga.eu/recursos/ambiente/parquesCaninos/da_parquesCaninos-4326.geojson",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def inspect_all():
    for name, url in URLS.items():
        logger.info(f"--- INSPECTING {name} ---")
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            # Check content type if it fails
            try:
                data = response.json()
            except Exception:
                logger.error(f"Failed to parse JSON. Status: {response.status_code}. Content-Type: {response.headers.get('Content-Type')}")
                continue

            features = []
            if isinstance(data, dict):
                features = data.get('features', [])
                if not features: 
                    # check if it is a flat dict that shouldn't happen for FeatureCollection
                     logger.warning("No 'features' key or empty.")
            elif isinstance(data, list):
                logger.info("Data is a LIST.")
                features = data
            
            if not features:
                logger.warning("No features found.")
                continue
                
            # Inspect first feature properties
            first_feature = features[0]
            
            # Check if it has 'properties' (standard GeoJSON) or if fields are at root
            if 'properties' in first_feature:
                props = first_feature['properties']
                logger.info("Found 'properties' key.")
            else:
                props = first_feature
                logger.info("No 'properties' key, using root.")

            logger.info(f"Fields: {list(props.keys())}")
            
        except Exception as e:
            logger.error(f"Failed to fetch {name}: {e}")

if __name__ == "__main__":
    inspect_all()
