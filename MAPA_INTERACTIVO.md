# 🗺️ Vista de Mapa Interactivo - Documentación

## Descripción General

La nueva **Vista de Mapa Interactivo** añade una forma visual e intuitiva de explorar las cámaras de tráfico de Málaga sobre un mapa interactivo, con separación por distritos y acceso directo a los detalles de cada cámara.

## Características Implementadas

### ✨ Funcionalidades Principales

1. **Mapa Interactivo con Leaflet/Folium**
   - Mapa base de OpenStreetMap centrado en Málaga
   - Zoom y navegación fluida
   - Controles de capas integrados

2. **Visualización de Cámaras**
   - Cada cámara se representa con un pin/marcador en su ubicación exacta
   - Icons de FontAwesome (video-camera) para mejor identificación visual
   - Tooltips al pasar el mouse mostrando nombre y dirección

3. **Diferenciación por Distritos**
   - 11 distritos de Málaga con colores únicos
   - Leyenda visual en la esquina del mapa
   - Filtro por distrito en la interfaz

4. **Clustering Inteligente**
   - Agrupación automática de cámaras cercanas
   - Mejora el rendimiento con muchas cámaras
   - Números indicando cantidad de cámaras agrupadas

5. **Popups Informativos**
   - Click en cualquier pin para ver detalles completos
   - Información mostrada:
     - Nombre de la cámara
     - Dirección completa
     - Distrito al que pertenece
     - Accesibilidad (PMR si disponible)
     - Enlaces directos a:
       - Web oficial de la cámara
       - Imagen en tiempo real
     - Datos técnicos (ID, coordenadas UTM y WGS84)

6. **Conversión de Coordenadas**
   - Sistema automático de conversión EPSG:25830 (UTM) → EPSG:4326 (WGS84)
   - Validación de coordenadas
   - Manejo robusto de errores

## Arquitectura Técnica

### Nuevos Componentes

#### 1. `src/utils/coordinate_converter.py`
```python
class CoordinateConverter:
    """Conversor de coordenadas entre EPSG:25830 (UTM) y EPSG:4326 (WGS84)"""
```

**Responsabilidades:**
- Conversión de coordenadas UTM a lat/lon
- Validación de coordenadas
- Singleton global para reutilización

**Tecnología:** pyproj 3.6+

#### 2. `src/views/map_view.py`
```python
class MapView(QWidget):
    """Vista de mapa interactivo con cámaras y distritos"""
```

**Responsabilidades:**
- Renderizado del mapa con folium
- Gestión de filtros por distrito
- Generación de marcadores y popups
- Integración con el navegador web

**Componentes UI:**
- Botón "Actualizar Mapa" - Regenera el mapa
- Botón "Abrir en Navegador" - Abre el HTML en navegador externo
- ComboBox de filtro por distrito
- Checkbox para mostrar/ocultar límites de distritos
- Contador de cámaras visibles
- Área de información con instrucciones

### Integración con MVC Existente

#### Model (sin cambios)
- `Camera`: Ya incluye coordenadas y distrito

#### View (modificado)
- `MainWindow`: Añadido botón "🗺️ Modo Mapa" en sidebar
- `MapView`: Nueva vista en el stacked widget (índice 3)

#### Controller (sin cambios necesarios)
- `CameraController`: Ya proporciona métodos para obtener cámaras filtradas

### Flujo de Datos

```
Usuario click "🗺️ Modo Mapa"
    ↓
MainWindow._change_view("mapa")
    ↓
map_view.set_cameras(cameras)
    ↓
Usuario click "Actualizar Mapa"
    ↓
map_view._generate_map()
    ↓
    Para cada cámara:
        coordinate_converter.convert(x, y)
        folium.Marker(...)
    ↓
mapa.save(html_file)
    ↓
Usuario click "Abrir en Navegador"
    ↓
QDesktopServices.openUrl(html_file)
```

## Configuración

### `config.py` - Nuevas Constantes

```python
# Mapa interactivo
MAP_CENTER_LAT = 36.7213  # Centro de Málaga
MAP_CENTER_LON = -4.4214
MAP_DEFAULT_ZOOM = 13
MAP_TILE_LAYER = "OpenStreetMap"
MAP_COORDINATE_SYSTEM = "EPSG:25830"  # Sistema CSV oficial
MAP_TARGET_SYSTEM = "EPSG:4326"  # WGS84 para folium

# Distritos de Málaga (colores)
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
```

### `requirements.txt` - Nuevas Dependencias

```
folium>=0.14.0      # Mapas interactivos Leaflet
pyproj>=3.6.0       # Conversión de coordenadas
```

## Uso para el Usuario Final

### Paso 1: Acceder a la Vista de Mapa
1. Abrir la aplicación "Cámaras de Tráfico Málaga"
2. En la barra lateral izquierda, click en **"🗺️ Modo Mapa"**

### Paso 2: Generar el Mapa
1. Click en el botón **"🔄 Actualizar Mapa"**
2. Esperar unos segundos mientras se procesan las cámaras
3. Ver mensaje de confirmación con cantidad de cámaras procesadas

### Paso 3: Visualizar en el Navegador
1. Click en **"🌐 Abrir en Navegador"**
2. Se abrirá automáticamente en tu navegador predeterminado
3. Explorar el mapa:
   - Zoom: Rueda del mouse o botones +/-
   - Pan: Arrastrar con el mouse
   - Click en pins: Ver detalles de la cámara

### Paso 4: Filtrar por Distrito (Opcional)
1. Usar el dropdown "Filtrar por distrito"
2. Seleccionar un distrito específico
3. Click nuevamente en "Actualizar Mapa"
4. Solo se mostrarán cámaras del distrito seleccionado

## Ventajas Técnicas

### 🚀 Performance
- **Clustering automático**: Las cámaras cercanas se agrupan evitando sobrecarga visual
- **Generación bajo demanda**: El mapa solo se genera cuando el usuario lo solicita
- **HTML estático**: Una vez generado, no consume recursos de la aplicación

### 🎨 UX Mejorada
- **Contexto geográfico**: Los usuarios ven instantáneamente dónde están las cámaras
- **Navegación intuitiva**: Familiar para cualquiera que haya usado Google Maps
- **Información rica**: Popups con todos los detalles relevantes

### 🔧 Mantenibilidad
- **Separación de concerns**: Conversión de coordenadas aislada en módulo propio
- **Configuración centralizada**: Colores y parámetros en `config.py`
- **Arquitectura MVC preservada**: Nueva vista no afecta modelos ni controlador

### ♿ Accesibilidad
- **Múltiples vías de acceso**: Además del mapa, las vistas lista/cuadrícula siguen disponibles
- **Navegador externo**: Los usuarios pueden usar herramientas de accesibilidad del navegador
- **Información textual**: Todos los datos visibles también están en popups de texto

## Extensiones Futuras Posibles

### 🌟 Mejoras Propuestas

1. **Integración QtWebEngine**
   - Mostrar mapa directamente en la aplicación (sin navegador externo)
   - Comunicación JavaScript ↔ Python para clicks en pins
   - Abrir CameraDetailDialog directamente desde el mapa

2. **Capas Adicionales**
   - Capa de tráfico en tiempo real
   - Capa de incidencias
   - Capa de rutas de transporte público

3. **Heatmap**
   - Densidad de cámaras por zona
   - Actividad/eventos detectados

4. **Rutas**
   - Calcular rutas entre puntos
   - Mostrar cámaras en la ruta

5. **Exportación**
   - Exportar mapa como imagen PNG/PDF
   - Compartir URL del mapa generado

6. **Geolocalización**
   - Centrar mapa en ubicación del usuario
   - Mostrar cámaras cercanas

## Testing Realizado

### ✅ Tests Unitarios
- `coordinate_converter.py`: Conversión UTM → WGS84 validada
- Coordenadas de prueba: UTM(374000, 4065000) → WGS84(-4.410956, 36.722348)

### ✅ Tests de Integración
- Generación de mapa con 5 cámaras de prueba
- Marcadores renderizados correctamente
- Popups con información completa
- Clustering funcionando
- Leyenda de distritos visible

### ✅ Tests Manuales Recomendados
1. [ ] Cargar datos reales del CSV de Málaga
2. [ ] Verificar renderizado de 135+ cámaras
3. [ ] Probar filtro por cada uno de los 11 distritos
4. [ ] Click en múltiples pins y verificar popups
5. [ ] Probar en diferentes navegadores (Chrome, Firefox, Safari, Edge)
6. [ ] Verificar responsive design (desktop, tablet, mobile)
7. [ ] Probar con temas claro/oscuro de la aplicación

## Archivos Generados

### Archivos Temporales
- `{temp_dir}/malaga_camaras_mapa.html`: Mapa generado por la aplicación
- `demo_mapa_camaras.html`: Mapa de demostración (script de prueba)

### Persistencia
- Los mapas se regeneran cada vez (no se guardan permanentemente)
- Esto asegura datos siempre actualizados

## Compatibilidad

### Sistemas Operativos
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+, Debian, Fedora)

### Navegadores Soportados
- ✅ Chrome/Chromium 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Python
- ✅ Python 3.10+
- ✅ Python 3.11
- ✅ Python 3.12

## Resolución de Problemas

### Problema: "El mapa no se genera"
**Solución:**
1. Verificar que las dependencias están instaladas: `pip install folium pyproj`
2. Verificar que hay cámaras cargadas
3. Revisar logs de la aplicación para errores

### Problema: "Coordenadas incorrectas"
**Solución:**
1. Verificar que el CSV tiene campo `ukb_geometry` con formato `POINT(x y)`
2. Verificar que las coordenadas están en EPSG:25830
3. Probar conversión manual con `coordinate_converter.py`

### Problema: "El navegador no se abre"
**Solución:**
1. Verificar navegador predeterminado configurado
2. Abrir manualmente el archivo HTML desde el explorador de archivos
3. Ruta mostrada en el área de información de la app

### Problema: "Pins no visibles en el mapa"
**Solución:**
1. Hacer zoom out para ver área más amplia
2. Verificar filtro de distrito (cambiarlo a "Todos")
3. Verificar que las coordenadas están en rango válido para Málaga

## Créditos

### Tecnologías Utilizadas
- **Folium**: Librería Python para mapas interactivos Leaflet
- **Leaflet**: Librería JavaScript de mapas de código abierto
- **PyProj**: Conversión de coordenadas geodésicas
- **OpenStreetMap**: Datos de mapas de código abierto
- **FontAwesome**: Iconos (video-camera)

### Datos
- **Ayuntamiento de Málaga**: Datos abiertos de cámaras de tráfico
- **URL CSV**: https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_camarasTrafico-25830.csv

## Changelog

### v1.0.0 (2025-11-05)
- ✨ Implementación inicial de vista de mapa interactivo
- ✨ Conversión automática de coordenadas EPSG:25830 → WGS84
- ✨ Filtrado por distrito
- ✨ Clustering de marcadores
- ✨ Popups informativos con enlaces
- ✨ Leyenda de distritos
- ✨ Integración con arquitectura MVC existente
