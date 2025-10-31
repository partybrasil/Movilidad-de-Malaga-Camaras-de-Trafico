"""
Configuración global de la aplicación Cámaras de Tráfico Málaga.

Este módulo centraliza todas las constantes y configuraciones del proyecto.
"""

# URL del dataset oficial
CSV_URL = "https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_camarasTrafico-25830.csv"

# Configuración de la interfaz
WINDOW_TITLE = "Cámaras de Tráfico - Málaga"
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800

# Configuración de actualización de imágenes
IMAGE_REFRESH_INTERVAL = 30  # segundos
IMAGE_TIMEOUT = 10  # segundos para timeout de descarga

# Headers HTTP para peticiones de imágenes
IMAGE_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Referer': 'https://movilidad.malaga.eu/',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin'
}

# Configuración de vista
DEFAULT_VIEW_MODE = "lista"  # "lista" o "cuadricula"
GRID_COLUMNS = 3  # Columnas en vista cuadrícula (calculado dinámicamente)
THUMBNAIL_SIZE = (320, 240)  # Tamaño de miniaturas

# Configuración de zoom en vista cuadrícula
THUMBNAIL_SIZES = {
    1: (200, 150),   # Muy pequeño - más cámaras por pantalla
    2: (250, 187),   # Pequeño
    3: (300, 225),   # Medio (default)
    4: (350, 262),   # Grande
    5: (400, 300),   # Muy grande
}
DEFAULT_THUMBNAIL_ZOOM = 3  # Nivel de zoom por defecto (1-5)

# Sistema de favoritos
MAX_FAVORITES = 9  # Límite de cámaras favoritas (configurable)
APP_DATA_DIR_NAME = "movilidad_malaga"
FAVORITES_FILE_NAME = "favorites.json"

# Configuración de caché
ENABLE_IMAGE_CACHE = True
CACHE_MAX_SIZE = 100  # Número máximo de imágenes en caché

# Tema
DEFAULT_THEME = "claro"  # "claro" u "oscuro"

# Logging
LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "app.log"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
LOG_TO_CONSOLE = True  # Mostrar logs en consola además de archivo

# Columnas del CSV
CSV_COLUMNS = {
    "nombre": "NOMBRE",
    "direccion": "DIRECCION",
    "geometry": "ukb_geometry",
    "url_imagen": "URLIMAGEN",
    "url": "URL",
    "acceso": "ACCESO",
    "distrito": "id_distrito"  # Puede no existir
}
