"""
Configuración global de la aplicación Cámaras de Tráfico Málaga.

Este módulo centraliza todas las constantes y configuraciones del proyecto.
"""

from pathlib import Path

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
MAX_FAVORITES = 25  # Límite de cámaras favoritas (configurable)
APP_DATA_DIR_NAME = "movilidad_malaga"
FAVORITES_FILE_NAME = "favorites.json"

# Configuración de caché
ENABLE_IMAGE_CACHE = True
CACHE_MAX_SIZE = 100  # Número máximo de imágenes en caché

# Tema
DEFAULT_THEME = "azul_profundo"  # Tema principal por defecto
DEFAULT_TEXT_COLOR = "amarillo_oscuro"  # Color de texto por defecto
DEFAULT_TEXTBOX_BACKGROUND = "negro"  # Fondo de caja de texto por defecto

# Temas disponibles
AVAILABLE_THEMES = [
    "claro", "oscuro", "azul_profundo", "verde_bosque", "purpura_real", 
    "rojo_cereza", "naranja_atardecer", "rosa_sakura", "gris_corporativo",
    "azul_hielo", "verde_menta", "ambar_dorado", "violeta_nocturno",
    "turquesa_tropical", "salmon_suave", "lavanda_relajante", "oliva_natural",
    "chocolate_rico", "slate_moderno", "teal_oceano", "coral_vibrante"
]

# Colores de texto disponibles
TEXT_COLORS = [
    "default", "negro", "blanco", "gris_oscuro", "gris_claro", "azul_oscuro",
    "azul_claro", "verde_oscuro", "verde_claro", "rojo_oscuro", "rojo_claro",
    "purpura_oscuro", "purpura_claro", "naranja_oscuro", "naranja_claro",
    "amarillo_oscuro", "amarillo_claro", "rosa_oscuro", "rosa_claro",
    "turquesa_oscuro", "turquesa_claro", "marron_oscuro", "marron_claro"
]

# Colores de fondo para cajas de texto
TEXTBOX_BACKGROUNDS = [
    "default", "blanco", "gris_muy_claro", "gris_claro", "gris_medio", 
    "gris_oscuro", "negro", "azul_muy_claro", "azul_claro", "verde_muy_claro",
    "verde_claro", "amarillo_muy_claro", "amarillo_claro", "rosa_muy_claro",
    "rosa_claro", "purpura_muy_claro", "purpura_claro", "naranja_muy_claro",
    "naranja_claro", "turquesa_muy_claro", "turquesa_claro", "crema", "beige"
]

# Logging
LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "app.log"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
LOG_TO_CONSOLE = True  # Mostrar logs en consola además de archivo

# Columnas del CSV
CSV_COLUMNS = {
    "nombre": "NOMBRE",
    "direccion": "DIRECCION",
    "geometry": "SDOGEOMETRIA",  # Corregido: era "ukb_geometry"
    "url_imagen": "URLIMAGEN",
    "url": "URL",
    "acceso": "ACCESOPMR",  # Corregido: era "ACCESO"
    "distrito": None  # No existe en el CSV actual
}

# Timelapse
TIMELAPSE_ROOT = Path("timelapses")
TIMELAPSE_INDEX_FILE = TIMELAPSE_ROOT / "index.json"
TIMELAPSE_FRAME_FORMAT = "jpg"
TIMELAPSE_DEFAULT_INTERVAL = 5  # segundos
TIMELAPSE_DEFAULT_DURATION = None  # segundos
TIMELAPSE_MAX_ACTIVE_RECORDERS = 10
TIMELAPSE_EXPORT_FORMATS = ["gif", "avi", "mp4", "mpeg"]
TIMELAPSE_EXPORT_FPS = 8
TIMELAPSE_PLAYBACK_SPEEDS = [
    0.05,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0,
    1.5,
    2.0,
    3.0,
    4.0,
    6.0,
    8.0,
    12.0,
    16.0,
]

# Mapa interactivo
MAP_CENTER_LAT = 36.7213  # Centro de Málaga
MAP_CENTER_LON = -4.4214
MAP_DEFAULT_ZOOM = 13
MAP_TILE_LAYER = "OpenStreetMap"  # Opciones: OpenStreetMap, CartoDB positron, CartoDB dark_matter
MAP_COORDINATE_SYSTEM = "EPSG:25830"  # Sistema de coordenadas del CSV oficial
MAP_TARGET_SYSTEM = "EPSG:4326"  # WGS84 (lat/lon) para folium

# Distritos de Málaga (colores para el mapa)
DISTRICT_COLORS = {
    "1": "#FF6B6B",   # Centro
    "2": "#4ECDC4",   # Málaga Este
    "3": "#45B7D1",   # Ciudad Jardín
    "4": "#96CEB4",   # Bailén-Miraflores
    "5": "#FFEAA7",   # Palma-Palmilla
    "6": "#DFE6E9",   # Cruz de Humilladero
    "7": "#A29BFE",   # Carretera de Cádiz
    "8": "#FD79A8",   # Churriana
    "9": "#FDCB6E",   # Campanillas
    "10": "#74B9FF",  # Puerto de la Torre
    "11": "#55EFC4",  # Teatinos-Universidad
}
