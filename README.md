# 🚦 Cámaras de Tráfico - Málaga

Aplicación de escritorio moderna y robusta para visualizar en tiempo real las cámaras de tráfico de Málaga, utilizando datos abiertos oficiales del Ayuntamiento de Málaga.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Activo-success.svg)

## ✨ Características Principales

### 🎯 Visualización
- 📹 **Visualización en tiempo real** de más de 135 cámaras de tráfico
- � **Dos modos de vista**: Lista compacta y cuadrícula expandida
- 🔍 **Zoom dinámico** en vista cuadrícula (5 niveles: 200px a 400px)
- 📐 **Reorganización automática** de columnas según el tamaño de ventana
- 🖼️ **Imágenes de alta calidad** directamente desde el servidor municipal

### 🔎 Búsqueda y Filtrado
- 🔍 **Búsqueda en tiempo real** por nombre o dirección
- �️ **Filtrado por zonas** y distritos de Málaga
- 🏷️ **Agrupación inteligente** por ubicación geográfica
- ❌ **Limpieza rápida** de todos los filtros

### 🔄 Actualización
- ⏱️ **Auto-refresco configurable** (cada 30 segundos por defecto)
- 🔄 **Actualización manual** global o individual por cámara
- 💾 **Sistema de caché** para optimizar el rendimiento
- ⚡ **Carga asíncrona** sin bloquear la interfaz

### 🎥 Timelapse
- 🎬 **Grabación de sesiones** con captura en segundo plano y control por cámara
- ⏱️ **Intervalos configurables** y seguimiento en tiempo real del progreso
- 📚 **Biblioteca de sesiones** con gestión de historiales y metadatos clave
- 🎛️ **Reproducción integrada** con nuevas velocidades (0.05x a 16x)
- 📦 **Exportación a MP4 o GIF** directamente desde la aplicación
- 🛡️ **Grabaciones resilientes** ante fallos temporales de red o cámara

### 🗺️ Mapa Interactivo
- 📍 **Geolocalización precisa** de todas las cámaras en un mapa interactivo
- 🚶 **Street View Integrado**:
  - Acceso directo a Google Street View desde cada cámara
  - Navegación virtual por las calles de Málaga
  - Accesible vía menú contextual (clic derecho) en el mapa
- 📹 **Tarjetas de Cámara Mejoradas**:
  - **Mini-reproductor en vivo** integrado en el popup del mapa
  - **Selector de actualización**: Elige la frecuencia (1s, 3s, 5s...)
  - Control automático de recursos al cerrar popups

### �🎨 Personalización
- 🌓 **Temas claro y oscuro** con transición suave
- � **Configuración flexible** mediante archivo config.py
- 📏 **Interfaz responsive** que se adapta al tamaño de ventana
- 🖱️ **Controles intuitivos** con indicadores visuales

### 🏗️ Arquitectura
- 🔨 **Patrón MVC** para separación de responsabilidades
- 📦 **Código modular** y bien organizado
- 🧪 **Preparado para testing** con estructura clara
- 📝 **Documentación inline** completa

## 📋 Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python**: 3.10 o superior
- **RAM**: 4 GB (recomendado 8 GB)
- **Conexión a Internet**: Necesaria para cargar datos e imágenes
- **Resolución de Pantalla**: Mínimo 1280x720 (recomendado 1920x1080)

### Dependencias Principales
- **PySide6**: 6.6+ (Framework Qt para interfaces gráficas)
- **requests**: Para peticiones HTTP a los servidores
- **pandas**: Procesamiento de datos CSV
- Todas las dependencias están en `requirements.txt`

## 🚀 Instalación y Configuración

### Instalación Rápida

1. **Clonar el repositorio:**
```bash
git clone https://github.com/partybrasil/Movilidad-de-Malaga-Camaras-de-Trafico.git
cd Movilidad-de-Malaga-Camaras-de-Trafico
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv .venv
```

3. **Activar entorno virtual:**

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

4. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### Verificación de la Instalación

Ejecuta el script de verificación:
```bash
python verify.py
```

Este script comprueba:
- ✅ Versión de Python correcta
- ✅ Todas las dependencias instaladas
- ✅ Conexión al servidor de datos
- ✅ Capacidad de descarga de imágenes

### Diagnóstico de Problemas

Si encuentras problemas, ejecuta:
```bash
python diagnose.py
```

Este script proporciona información detallada sobre:
- Estado del entorno Python
- Versiones de paquetes instalados
- Conectividad de red
- Permisos de archivos

## 🎮 Guía de Uso

### Iniciar la Aplicación

```bash
python src/main.py
```

La aplicación se iniciará y cargará automáticamente todas las cámaras disponibles.

### �️ Modos de Vista

#### Vista Lista
- **Activación**: Clic en "📋 Vista Lista" en la barra lateral
- **Características**:
  - Visualización compacta de todas las cámaras
  - Miniaturas pequeñas con información básica
  - Ideal para navegar rápidamente por muchas cámaras
  - Scroll vertical fluido

#### Vista Cuadrícula
- **Activación**: Clic en "🔲 Vista Cuadrícula" en la barra lateral
- **Características**:
  - Tarjetas grandes con imágenes ampliadas
  - Control de zoom dinámico (5 niveles)
  - Reorganización automática de columnas
  - Mejor para visualización detallada

### 🔍 Control de Zoom (Vista Cuadrícula)

El control de zoom permite ajustar el tamaño de las miniaturas:

**Controles:**
- **Botón "−"**: Reduce el tamaño (más cámaras por pantalla)
- **Botón "+"**: Aumenta el tamaño (mayor detalle)
- **Indicador**: Muestra el nivel actual (1/5 a 5/5)

**Niveles de Zoom:**
| Nivel | Tamaño | Columnas* | Uso Recomendado |
|-------|--------|-----------|-----------------|
| 1     | 200×150px | ~6 | Máxima densidad, vista general |
| 2     | 250×187px | ~5 | Alta densidad |
| 3     | 300×225px | ~4 | **Balance óptimo (default)** |
| 4     | 350×262px | ~3 | Más detalle |
| 5     | 400×300px | ~2 | Máximo detalle |

*El número de columnas se calcula dinámicamente según el ancho de la ventana

**Características del Zoom:**
- ✅ Ajuste instantáneo al cambiar nivel
- ✅ Sin scroll horizontal (solo vertical)
- ✅ Mantiene el aspecto de las imágenes
- ✅ Los botones se deshabilitan en los límites
- ✅ Posición de scroll preservada

### 🔍 Búsqueda y Filtrado

#### Búsqueda por Texto
1. Escribe en la barra de búsqueda (🔍)
2. La búsqueda se aplica en tiempo real
3. Busca en: nombres de cámaras y direcciones
4. No distingue entre mayúsculas/minúsculas

**Ejemplos:**
- `"Alameda"` → Todas las cámaras en la Alameda
- `"Centro"` → Cámaras del centro
- `"TV-"` → Búsqueda por código de cámara

#### Filtrado por Zona
1. Despliega el combo "Zona"
2. Selecciona una zona específica
3. Las cámaras se filtran automáticamente
4. Selecciona "Todas" para ver todas las zonas

**Zonas Disponibles:**
- Centro
- Este
- Bailén-Miraflores
- Carretera de Cádiz
- Cruz de Humilladero
- Churriana
- Campanillas
- Puerto de la Torre
- Palma-Palmilla
- Teatinos-Universidad

#### Limpiar Filtros
- Botón "❌ Limpiar": Restablece búsqueda y filtros
- Útil para volver a la vista completa

### 🔄 Actualización de Imágenes

#### Actualización Manual
- **Actualizar Todo**: Botón "🔄 Actualizar Todo" refresca todas las cámaras
- **Actualizar Individual**: Botón "🔄 Actualizar" en cada cámara
- **Indicador de Progreso**: Barra de estado muestra el progreso

#### Auto-Refresco
1. Activa con el botón "⏱ Auto-refresco"
2. Las imágenes se actualizan cada 30 segundos (configurable)
3. El indicador visual muestra el estado:
   - **▶ Auto-refresco: Activo** (verde)
   - **⏸ Auto-refresco: Inactivo** (gris)
4. Desactiva el botón para pausar

**Ventajas del Auto-Refresco:**
- Mantiene las imágenes actualizadas automáticamente
- Útil para monitoreo continuo
- Se puede pausar en cualquier momento
- Optimizado para no consumir recursos innecesarios

### 📋 Vista Detallada de Cámara

Accede a información completa de cualquier cámara:

1. **Abrir**: Clic en "👁 Ver detalles" en cualquier cámara
2. **Información Mostrada**:
   - Imagen en tamaño completo
   - Nombre de la cámara
   - Dirección exacta
   - Zona/Distrito
   - Coordenadas geográficas
   - Enlace al sitio web oficial
3. **Acciones Disponibles**:
   - 🔄 Actualizar imagen
   - 🌐 Abrir en navegador
   - ❌ Cerrar vista detalle

### 🎨 Cambio de Tema

1. Clic en "🌓 Cambiar Tema" en la barra lateral
2. Alterna entre tema claro y oscuro
3. El cambio es instantáneo
4. La preferencia se mantiene durante la sesión

**Temas Disponibles:**
- **Claro**: Fondo blanco, ideal para ambientes luminosos
- **Oscuro**: Fondo oscuro, reduce fatiga visual en ambientes con poca luz

### 🎥 Timelapse

La aplicación incluye un flujo completo para capturar y gestionar timelapses sin salir de la interfaz principal.

#### Crear una Sesión
1. Abre el menú contextual de cualquier cámara (icono ⋮) y selecciona "🎬 Grabar timelapse".
2. Configura intervalo de captura, duración máxima y directorio opcional.
3. Inicia la grabación; la barra lateral mostrará el estado y los frames capturados.
4. Puedes minimizar el diálogo: la captura continúa en segundo plano.

#### Revisar y Reproducir
1. Accede a la "Biblioteca de timelapses" desde la barra lateral.
2. Selecciona una sesión para ver detalles, previsualizar miniaturas y metadatos.
3. Pulsa "▶ Reproducir" para abrir el reproductor incorporado.
4. Ajusta velocidad entre 0.05x y 16x o aplica bouclé para revisiones continuas.

#### Exportar y Compartir
1. Desde la biblioteca, abre el menú de acciones de la sesión.
2. Elige "Exportar" y selecciona formato MP4 o GIF.
3. Configura fps de salida, resolución opcional y carpeta destino.
4. La exportación se ejecuta mediante hilos dedicados, con notificaciones al finalizar.

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
Movilidad-de-Malaga-Camaras-de-Trafico/
├── 📁 src/                          # Código fuente principal
│   ├── 📄 __init__.py              # Inicialización del paquete
│   ├── 📄 main.py                  # Punto de entrada de la aplicación
│   │
│   ├── 📁 models/                  # Modelos de datos (Capa de datos)
│   │   ├── 📄 __init__.py
│   │   └── 📄 camera.py            # Clase Camera con lógica de datos
│   │
│   ├── 📁 timelapse/               # Módulos de gestión de timelapses
│   │   ├── 📄 __init__.py
│   │   ├── 📄 manager.py           # Orquestador y persistencia de sesiones
│   │   ├── 📄 recorder.py          # Captura de frames en segundo plano
│   │   ├── 📄 exporter.py          # Exportación a MP4/GIF con imageio
│   │   ├── 📄 player.py            # Reproductor y controles de velocidad
│   │   └── 📄 models.py            # Entidades Timelapse y utilidades
│   │
│   ├── 📁 views/                   # Interfaces gráficas (Capa de presentación)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main_window.py       # Ventana principal de la app
│   │   ├── 📄 camera_widget.py     # Widgets de visualización de cámaras
│   │   ├── 📄 timelapse_library.py # Biblioteca y acciones de sesiones
│   │   ├── 📄 timelapse_start_dialog.py # Asistente de grabación
│   │   └── 📄 styles.py            # Estilos Qt (temas claro/oscuro)
│   │
│   ├── 📁 controllers/             # Controladores (Capa de lógica)
│   │   ├── 📄 __init__.py
│   │   └── 📄 camera_controller.py # Lógica de negocio y coordinación
│   │
│   └── 📁 utils/                   # Utilidades y helpers
│       ├── 📄 __init__.py
│       ├── 📄 data_loader.py       # Carga y parseo del CSV
│       └── 📄 image_loader.py      # Descarga asíncrona de imágenes
│
├── 📄 config.py                     # Configuración global centralizada
├── 📄 requirements.txt              # Dependencias del proyecto
├── 📄 verify.py                     # Script de verificación de instalación
├── 📄 diagnose.py                   # Script de diagnóstico de problemas
│
├── 📄 README.md                     # Este archivo (documentación principal)
├── 📄 QUICKSTART.md                 # Guía rápida de inicio
├── 📄 ARCHITECTURE.md               # Documentación de arquitectura detallada
├── 📄 FUENTES.md                    # Información sobre fuentes de datos
├── 📄 PROJECT_SUMMARY.md            # Resumen ejecutivo del proyecto
│
├── 📄 LICENSE                       # Licencia MIT
├── 📄 .gitignore                    # Archivos ignorados por Git
│
└── 📁 .venv/                        # Entorno virtual (no versionado)
```

### Patrón de Arquitectura: MVC

El proyecto sigue el patrón **Model-View-Controller** para separación de responsabilidades:

#### 🗂️ Models (`src/models/`)
**Responsabilidad**: Representación de datos y lógica de dominio

- `camera.py`: Define la clase `Camera`
  - Propiedades: id, nombre, dirección, URL imagen, coordenadas, etc.
  - Métodos: validación, parseo de datos, extracción de zona
  - Sin dependencias de UI

**Principios:**
- Independiente de la capa de presentación
- Validación de datos robusta
- Inmutabilidad cuando es posible

#### 🎥 Timelapse (`src/timelapse/`)
**Responsabilidad**: Gestión integral de sesiones timelapse y su ciclo de vida

- `models.py`: Entidades para sesiones, capturas y estados persistentes
- `manager.py`: Servicio de alto nivel que coordina grabación, reproducción y biblioteca
- `recorder.py`: Captura asíncrona con reintentos y notificaciones thread-safe
- `exporter.py`: Pipeline de exportación a MP4/GIF basado en imageio y FFmpeg
- `player.py`: Diálogo de reproducción con controles de velocidad y navegación

**Principios:**
- Aislamiento respecto al resto de la UI mediante señales Qt
- Operaciones largas siempre en hilos dedicados para no bloquear la interfaz
- Persistencia simple en disco para facilitar integraciones futuras

#### 👁️ Views (`src/views/`)
**Responsabilidad**: Interfaz gráfica y experiencia de usuario

- `main_window.py`: Ventana principal
`main_window.py`: Ventana principal
  - Barra lateral de navegación y accesos a timelapse
  - Área de contenido con vistas lista/cuadrícula
  - Barra de filtros y búsqueda
  - Gestión de eventos de UI y estado global

- `camera_widget.py`: Componentes visuales de cámaras
  - `CameraWidget`: Tarjeta de cámara para vista cuadrícula
  - `CameraListItem`: Item compacto para vista lista
  - `CameraDetailDialog`: Diálogo de detalles completos

- `timelapse_library.py`: Diálogo maestro para explorar y gestionar sesiones
- `timelapse_start_dialog.py`: Asistente guiado para configurar nuevas capturas

- `styles.py`: Gestión de temas visuales
  - Estilos Qt para tema claro
  - Estilos Qt para tema oscuro
  - Paletas de colores

**Principios:**
- Solo maneja presentación y eventos de UI
- Delega lógica de negocio al Controller
- Comunicación mediante signals/slots de Qt

#### 🎮 Controllers (`src/controllers/`)
**Responsabilidad**: Lógica de negocio y coordinación

- `camera_controller.py`: Controlador principal
  - Carga de datos desde CSV
  - Filtrado y búsqueda de cámaras
  - Gestión de actualización de imágenes
  - Auto-refresco periódico
  - Coordinación entre Models y Views
  - Integración con `TimelapseManager` para capturas y exportaciones

**Principios:**
- Orquesta la interacción entre Models y Views
- Contiene la lógica de negocio
- Gestiona el estado de la aplicación

#### 🛠️ Utils (`src/utils/`)
**Responsabilidad**: Utilidades y servicios compartidos

- `data_loader.py`: Carga de datos
  - Descarga del CSV desde URL
  - Parseo con pandas
  - Transformación a objetos Camera
  - Manejo de errores de red

- `image_loader.py`: Gestor de imágenes
  - Descarga asíncrona con threads
  - Sistema de caché LRU
  - Manejo de errores HTTP
  - Conversión a QPixmap para Qt
  - Signals para notificaciones

**Principios:**
- Reutilizables y desacoplados
- Sin dependencias entre sí
- Logging detallado para debugging

### 🔄 Flujo de Datos

```
1. Usuario interactúa con la UI (View)
           ↓
2. View emite señales (Qt Signals)
           ↓
3. Controller recibe señales y procesa
           ↓
4. Controller actualiza Models o llama a Utils
           ↓
5. Controller emite señales de vuelta a View
           ↓
6. View actualiza la interfaz
```

### 🧩 Componentes Clave

#### Sistema de Caché
- **Ubicación**: `image_loader.py`
- **Tipo**: LRU (Least Recently Used)
- **Capacidad**: Configurable (default: 100 imágenes)
- **Beneficios**: Reduce peticiones HTTP, mejora rendimiento

#### Sistema de Threading
- **Workers**: Threads para descarga de imágenes
- **Queue**: Cola de peticiones pendientes
- **Signals**: Comunicación thread-safe con UI

#### Sistema de Logging
- **Configuración**: `config.py` y `main.py`
- **Niveles**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Salidas**: Archivo `app.log` y consola (opcional)

### 📚 Dependencias Principales

| Librería | Versión | Propósito |
|----------|---------|-----------|
| PySide6 | 6.6+ | Framework Qt para GUI |
| requests | 2.31+ | Peticiones HTTP |
| pandas | 2.0+ | Procesamiento de datos CSV |
| imageio | 2.34+ | Exportación de timelapses a GIF/MP4 |
| imageio-ffmpeg | 0.5+ | Backend FFmpeg para codificación de video |

### 🔒 Principios de Diseño

1. **Separation of Concerns**: Cada capa tiene responsabilidades claras
2. **DRY (Don't Repeat Yourself)**: Código reutilizable en utils
3. **Single Responsibility**: Cada clase/función tiene un propósito específico
4. **Open/Closed**: Extensible sin modificar código existente
5. **Dependency Injection**: Controllers inyectados en Views

### 🧪 Testing (Futuro)

Estructura planificada:
```
tests/
├── unit/              # Tests unitarios
├── integration/       # Tests de integración
└── e2e/              # Tests end-to-end
```

## ⚙️ Configuración Avanzada

El archivo `config.py` centraliza toda la configuración de la aplicación. Puedes personalizarlo según tus necesidades:

### Configuración de Actualización

```python
# Intervalo de auto-refresco (en segundos)
IMAGE_REFRESH_INTERVAL = 30  # Ajusta según preferencia (mínimo: 10s)

# Timeout para descarga de imágenes
IMAGE_TIMEOUT = 10  # Segundos antes de marcar error
```

### Configuración de Vista

```python
# Vista por defecto al iniciar
DEFAULT_VIEW_MODE = "lista"  # Opciones: "lista" o "cuadricula"

# Niveles de zoom disponibles (ancho, alto en píxeles)
THUMBNAIL_SIZES = {
    1: (200, 150),   # Muy pequeño
    2: (250, 187),   # Pequeño
    3: (300, 225),   # Medio (default)
    4: (350, 262),   # Grande
    5: (400, 300),   # Muy grande
}

# Nivel de zoom por defecto
DEFAULT_THUMBNAIL_ZOOM = 3  # Valores: 1-5
```

### Configuración de Caché

```python
# Habilitar sistema de caché de imágenes
ENABLE_IMAGE_CACHE = True  # True/False

# Número máximo de imágenes en caché
CACHE_MAX_SIZE = 100  # Ajusta según RAM disponible
```

### Configuración de Interfaz

```python
# Ventana principal
WINDOW_TITLE = "Cámaras de Tráfico - Málaga"
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800

# Tema por defecto
DEFAULT_THEME = "claro"  # Opciones: "claro" u "oscuro"
```

### Configuración de Logging

```python
# Nivel de detalle de logs
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Archivo de log
LOG_FILE = "app.log"

# Mostrar logs en consola
LOG_TO_CONSOLE = True  # True/False
```

### Configuración de Timelapse

```python
from pathlib import Path

# Directorio raíz para almacenar sesiones
TIMELAPSE_ROOT = Path("timelapses")
TIMELAPSE_INDEX_FILE = TIMELAPSE_ROOT / "index.json"

# Parámetros de captura
TIMELAPSE_DEFAULT_INTERVAL = 5  # segundos
TIMELAPSE_DEFAULT_DURATION = None  # límite opcional en segundos
TIMELAPSE_MAX_ACTIVE_RECORDERS = 10

# Reproductor y exportación
TIMELAPSE_PLAYBACK_SPEEDS = [
  0.05, 0.1, 0.25, 0.5, 0.75,
  1.0, 1.5, 2.0, 3.0, 4.0,
  6.0, 8.0, 12.0, 16.0,
]
TIMELAPSE_EXPORT_FORMATS = ["gif", "avi", "mp4", "mpeg"]
TIMELAPSE_EXPORT_FPS = 8
```

### Headers HTTP Personalizados

```python
# Headers para peticiones de imágenes
IMAGE_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0...',
    'Accept': 'image/*',
    # ... más headers
}
```

**💡 Tip**: Después de modificar `config.py`, reinicia la aplicación para aplicar los cambios.

## 📊 Fuente de Datos

Los datos provienen del **Portal de Datos Abiertos del Ayuntamiento de Málaga**:

- **URL**: https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_camarasTrafico-25830.csv
- **Formato**: CSV (UTF-8)
- **Actualización**: Oficial del Ayuntamiento
- **Licencia**: Datos Abiertos

### Campos utilizados:
- `NOMBRE`: Identificador de la cámara
- `DIRECCION`: Ubicación descriptiva
- `URLIMAGEN`: Imagen en tiempo real
- `URL`: Enlace web oficial
- `ukb_geometry`: Coordenadas (POINT)
- `id_distrito`: Agrupación por distrito

## 🔮 Roadmap y Mejoras Futuras

### ✅ Últimas Novedades
- ✅ **Mapa Interactivo Completo**: Street View, mini-player en vivo y clustering inteligente.
- ✅ **Timelapse completo**: Grabación, biblioteca, reproducción multi-velocidad y exportación MP4/GIF.

### 🎯 Versión 2.0 (En Planificación)
- [x] **Mapa interactivo** con ubicación de cámaras
  - [x] Integración con mapas (Folium/Leaflet)
  - [x] Marcadores clicables en el mapa
  - [x] Vista de mapa en tiempo real (Mini-player)
  - [x] Navegación por ubicación geográfica (Street View)

- [ ] **Mejoras de visualización**
  - Vista de comparación múltiple (2-4 cámaras simultáneas)
  - Modo pantalla completa para cámaras individuales
  - Captura de pantalla de cámaras

### 📊 Versión 2.5 (Futuro)
- [ ] **Análisis y estadísticas**
  - Historial de imágenes con timeline
  - Detección de cambios en el tráfico
  - Gráficos de densidad de tráfico
  - Análisis de patrones por horarios

- [ ] **Funcionalidades avanzadas**
  - Sistema de notificaciones de incidencias
  - Alertas personalizables
  - Favoritos y listas personalizadas
  - Etiquetas y categorización manual

### 🔧 Versión 3.0 (Visión)
- [ ] **Integración y exportación**
  - Exportar reportes en PDF
  - Exportar imágenes en lote
  - API REST para integración externa
  - Webhooks para eventos

- [ ] **Inteligencia Artificial**
  - Detección automática de incidentes
  - Reconocimiento de matrículas (con permisos)
  - Predicción de tráfico
  - Alertas inteligentes

### 📱 Multiplataforma
- [ ] Versión web responsive
- [ ] App móvil (Android/iOS)
- [ ] PWA (Progressive Web App)

### 🌍 Expansión
- [ ] Soporte para otras ciudades
- [ ] Sistema de plugins
- [ ] Modo multidioma
- [ ] Accesibilidad mejorada (WCAG 2.1)

**💡 ¿Tienes una idea?** Abre un [issue](https://github.com/partybrasil/Movilidad-de-Malaga-Camaras-de-Trafico/issues) con la etiqueta `enhancement` para sugerir nuevas funcionalidades.

## 🤝 Contribuir al Proyecto

¡Las contribuciones son bienvenidas y apreciadas! Hay muchas formas de contribuir a este proyecto:

### 🐛 Reportar Bugs

Si encuentras un error:
1. Verifica que no exista ya en [Issues](https://github.com/partybrasil/Movilidad-de-Malaga-Camaras-de-Trafico/issues)
2. Abre un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Screenshots si es posible
   - Información del sistema (OS, Python version)

### 💡 Sugerir Mejoras

Para proponer nuevas funcionalidades:
1. Abre un issue con etiqueta `enhancement`
2. Describe la funcionalidad deseada
3. Explica el caso de uso
4. Proporciona ejemplos si es posible

### 🔧 Contribuir con Código

#### Flujo de Trabajo

1. **Fork** el repositorio
2. **Crea una rama** para tu feature:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Implementa** tus cambios
4. **Sigue las guías de estilo**:
   - PEP 8 para Python
   - Docstrings para todas las funciones
   - Comentarios claros en español
5. **Commit** con mensajes descriptivos:
   ```bash
   git commit -m 'feat: Add amazing feature'
   ```
6. **Push** a tu rama:
   ```bash
   git push origin feature/AmazingFeature
   ```
7. **Abre un Pull Request** con:
   - Descripción detallada de los cambios
   - Referencias a issues relacionados
   - Screenshots si aplica

#### Convenciones de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bugs
- `docs:` Cambios en documentación
- `style:` Formato de código (sin cambios funcionales)
- `refactor:` Refactorización de código
- `test:` Añadir o modificar tests
- `chore:` Tareas de mantenimiento

### 📚 Contribuir con Documentación

- Mejorar el README
- Añadir ejemplos de uso
- Traducir documentación
- Crear tutoriales o guías

### 🧪 Testing

Al contribuir código:
- Asegúrate de que el código existente sigue funcionando
- Añade tests si es posible
- Verifica que no hay errores con `python diagnose.py`

### 📝 Code Review

Todos los PRs serán revisados:
- Se valorará código limpio y bien documentado
- Respeto por la arquitectura existente
- Compatibilidad con versiones anteriores

### 👥 Código de Conducta

- Sé respetuoso y constructivo
- Acepta críticas constructivas
- Enfócate en lo mejor para el proyecto
- Ayuda a otros contribuidores

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Movilidad Málaga Team**

## 🙏 Agradecimientos

- Ayuntamiento de Málaga por proporcionar los datos abiertos
- Comunidad de PySide6/Qt
- Todos los contribuidores del proyecto

## 📧 Contacto y Soporte

### 🐛 Reportar Problemas
Para reportar bugs o problemas técnicos:
- **GitHub Issues**: [Crear nuevo issue](https://github.com/partybrasil/Movilidad-de-Malaga-Camaras-de-Trafico/issues)
- **Etiquetas**: Usa `bug` para errores, `question` para dudas

### 💡 Sugerencias
Para proponer mejoras o nuevas funcionalidades:
- **GitHub Issues**: Usa la etiqueta `enhancement`
- **Discussions**: Únete a las [discusiones](https://github.com/partybrasil/Movilidad-de-Malaga-Camaras-de-Trafico/discussions)

### 📚 Documentación Adicional
- **QUICKSTART.md**: Guía rápida de inicio
- **ARCHITECTURE.md**: Arquitectura técnica detallada
- **FUENTES.md**: Información sobre fuentes de datos
- **PROJECT_SUMMARY.md**: Resumen ejecutivo

### 🌐 Enlaces Útiles
- **Portal Datos Abiertos Málaga**: https://datosabiertos.malaga.eu/
- **Movilidad Málaga**: https://movilidad.malaga.eu/
- **PySide6 Documentación**: https://doc.qt.io/qtforpython/

---

## ❓ Preguntas Frecuentes (FAQ)

### General

**P: ¿La aplicación es gratuita?**  
R: Sí, es completamente gratuita y de código abierto bajo licencia MIT.

**P: ¿Funciona sin conexión a Internet?**  
R: No, requiere conexión para cargar datos e imágenes en tiempo real del servidor municipal.

**P: ¿En qué sistemas operativos funciona?**  
R: Windows 10/11, Linux (Ubuntu 20.04+) y macOS 10.15+.

**P: ¿Cuántas cámaras hay disponibles?**  
R: Actualmente hay más de 135 cámaras de tráfico en Málaga.

### Instalación y Configuración

**P: ¿Qué versión de Python necesito?**  
R: Python 3.10 o superior.

**P: ¿Puedo instalarla sin entorno virtual?**  
R: Sí, pero se recomienda usar un entorno virtual para evitar conflictos de dependencias.

**P: ¿Dónde se guardan los logs?**  
R: En el archivo `app.log` en la raíz del proyecto.

**P: ¿Puedo cambiar la configuración sin editar código?**  
R: Sí, edita el archivo `config.py` con cualquier editor de texto.

### Uso

**P: ¿Cómo cambio el tamaño de las miniaturas?**  
R: En vista cuadrícula, usa los botones +/- junto al filtro de zona.

**P: ¿Las imágenes se guardan localmente?**  
R: Solo en caché temporal mientras la aplicación está abierta. No se guardan en disco.

**P: ¿Puedo ver el historial de una cámara?**  
R: Actualmente no, esta función está en el roadmap para futuras versiones.

**P: ¿Por qué algunas cámaras no cargan?**  
R: Puede ser por mantenimiento del servidor o cámara desconectada temporalmente.

### Rendimiento

**P: ¿Cuánta RAM consume?**  
R: Entre 100-300 MB dependiendo del número de imágenes en caché.

**P: ¿Puedo ajustar el rendimiento?**  
R: Sí, reduce `CACHE_MAX_SIZE` en `config.py` para usar menos memoria.

**P: ¿Por qué va lenta la carga inicial?**  
R: La primera carga descarga todas las imágenes. Usa el caché para siguientes cargas.

### Problemas Comunes

**P: No se muestran las imágenes**  
R: Verifica tu conexión a Internet y que el servidor de Málaga esté accesible.

**P: La aplicación no inicia**  
R: Ejecuta `python diagnose.py` para identificar el problema.

**P: Error de módulo no encontrado**  
R: Asegúrate de haber instalado las dependencias: `pip install -r requirements.txt`

**P: Las imágenes están borrosas**  
R: Aumenta el nivel de zoom en vista cuadrícula para ver imágenes más grandes.

---

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'PySide6'"

**Solución:**
```bash
pip install -r requirements.txt
```

### Error: "Unable to load CSV data"

**Causas posibles:**
1. Sin conexión a Internet
2. Servidor de datos de Málaga no disponible
3. URL del CSV ha cambiado

**Solución:**
```bash
python diagnose.py  # Ejecuta diagnóstico
```

### Las imágenes no se actualizan

**Soluciones:**
1. Verifica que auto-refresco esté activado
2. Haz clic manual en "🔄 Actualizar Todo"
3. Verifica conexión a Internet
4. Revisa el archivo `app.log` para errores

### La aplicación se cierra inesperadamente

**Soluciones:**
1. Revisa `app.log` para el error exacto
2. Ejecuta con más logging: Cambia `LOG_LEVEL = "DEBUG"` en `config.py`
3. Reporta el error en GitHub Issues con el log

### Ventana no se muestra correctamente

**Soluciones:**
1. Ajusta resolución de pantalla (mínimo 1280x720)
2. Actualiza drivers de gráficos
3. Verifica compatibilidad Qt con tu sistema

### Alto consumo de memoria

**Soluciones:**
1. Reduce `CACHE_MAX_SIZE` en `config.py`
2. Cierra otras aplicaciones
3. Usa vista lista en lugar de cuadrícula

### Imágenes se cargan muy lento

**Soluciones:**
1. Verifica velocidad de Internet
2. Aumenta `IMAGE_TIMEOUT` en `config.py`
3. Desactiva auto-refresco temporalmente
4. Habilita caché: `ENABLE_IMAGE_CACHE = True`

### Necesitas más ayuda

Si ninguna solución funciona:
1. Ejecuta `python diagnose.py` y guarda el output
2. Revisa issues existentes en GitHub
3. Crea un nuevo issue con:
   - Descripción del problema
   - Output de `diagnose.py`
   - Logs relevantes de `app.log`
   - Sistema operativo y versión Python

---

**Proyecto mantenido con ❤️ por el equipo de Movilidad Málaga**

⭐ Si te gusta el proyecto, ¡dale una estrella en GitHub!

---

**⚠️ Nota**: Esta aplicación es un prototipo educativo. Las imágenes y datos provienen de fuentes oficiales públicas del Ayuntamiento de Málaga.
