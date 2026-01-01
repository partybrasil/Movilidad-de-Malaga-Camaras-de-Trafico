
import logging
import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("InspectEMT")

URL = "https://datosabiertos.malaga.eu/recursos/transporte/EMT/EMTLineasYParadas/lineasyparadas.geojson"

def inspect():
    logger.info(f"--- INSPECTING EMT ---")
    try:
        response = requests.get(URL, timeout=20) # Increased timeout as it's a large file
        data = response.json()
        
        if not isinstance(data, list):
            logger.error(f"Data is not a list, it is {type(data)}")
            return

        logger.info(f"Number of lines: {len(data)}")
        
        if len(data) > 0:
            first_line = data[0]
            logger.info(f"First Line Keys: {list(first_line.keys())}")
            
            paradas = first_line.get('paradas', [])
            logger.info(f"Number of stops in first line: {len(paradas)}")
            
            if len(paradas) > 0:
                first_stop = paradas[0]
                logger.info(f"First Stop Structure: {json.dumps(first_stop, indent=2, ensure_ascii=False)}")
                
                # Check properties inside 'parada' key if it exists? 
                # Or are properties direct?
                
    except Exception as e:
        logger.error(f"Failed: {e}")

if __name__ == "__main__":
    inspect()
