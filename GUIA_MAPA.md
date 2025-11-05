# 🗺️ Guía Rápida: Vista de Mapa Interactivo

## ¿Qué es?

La **Vista de Mapa Interactivo** es una nueva funcionalidad que permite visualizar todas las cámaras de tráfico de Málaga sobre un mapa interactivo, con separación por distritos y acceso directo a los detalles de cada cámara mediante clicks en los pines.

## Acceso Rápido

1. Abre la aplicación "Cámaras de Tráfico - Málaga"
2. En la barra lateral izquierda, haz click en **"🗺️ Modo Mapa"**
3. Haz click en **"🔄 Actualizar Mapa"**
4. Haz click en **"🌐 Abrir en Navegador"**

¡Listo! Ahora puedes explorar el mapa interactivo en tu navegador.

## Características Principales

### 📍 Pins de Cámaras
- Cada cámara aparece como un pin en su ubicación exacta
- Los pins están coloreados según el distrito
- Al pasar el mouse, aparece el nombre y dirección

### 🎨 Colores por Distrito
Cada uno de los 11 distritos de Málaga tiene un color único:
- Distrito 1 (Centro): 🔴 Rojo
- Distrito 2 (Málaga Este): 🔵 Azul turquesa
- Distrito 3 (Ciudad Jardín): 🔵 Azul claro
- Distrito 4 (Bailén-Miraflores): 🟢 Verde menta
- Distrito 5 (Palma-Palmilla): 🟡 Amarillo
- ... y más

### 📊 Clustering Inteligente
- Las cámaras cercanas se agrupan automáticamente
- Los números en los clusters indican cuántas cámaras hay
- Al hacer zoom, los clusters se expanden

### ℹ️ Información Detallada
Haz click en cualquier pin para ver:
- 📹 Nombre de la cámara
- 📍 Dirección completa
- 🏛️ Distrito
- ♿ Accesibilidad (si aplica)
- 🔗 Enlace a la web oficial
- 📷 Enlace a la imagen en tiempo real
- 🔢 Datos técnicos (ID, coordenadas)

### 🔍 Filtros
Usa el selector de distrito para ver solo cámaras de un distrito específico:
1. Selecciona un distrito del menú desplegable
2. Haz click en "Actualizar Mapa"
3. Solo aparecerán las cámaras de ese distrito

## Navegación del Mapa

### 🖱️ Controles del Mouse
- **Zoom**: Rueda del mouse o botones +/- en la esquina
- **Pan**: Arrastra con el botón izquierdo
- **Click**: En un pin para ver información

### ⌨️ Atajos de Teclado
- **+**: Acercar zoom
- **-**: Alejar zoom
- **←↑↓→**: Mover el mapa

### 📱 En Dispositivos Táctiles
- **Pellizcar**: Para hacer zoom
- **Arrastrar**: Para mover el mapa
- **Toque**: En un pin para información

## Casos de Uso

### 1️⃣ Planificar una Ruta
"Quiero saber qué cámaras hay en mi ruta al trabajo"
1. Abre el mapa
2. Localiza tu punto de partida
3. Sigue visualmente tu ruta
4. Observa las cámaras en el camino

### 2️⃣ Buscar Cámaras por Zona
"¿Qué cámaras hay en el centro?"
1. Filtra por "Distrito 1"
2. Actualiza el mapa
3. Todas las cámaras del centro aparecen

### 3️⃣ Explorar una Cámara Específica
"Quiero ver la cámara de la Alameda"
1. Busca la zona de la Alameda en el mapa
2. Click en el pin de la cámara
3. Click en "Ver imagen actual" en el popup

### 4️⃣ Obtener Información Geográfica
"¿Dónde exactamente está esta cámara?"
1. Click en el pin de la cámara
2. En el popup, mira "Datos técnicos"
3. Ahí encontrarás las coordenadas exactas

## Solución de Problemas

### ❓ "El mapa no se abre en el navegador"
**Solución:**
1. Copia la ruta del archivo HTML mostrada en la app
2. Pégala en la barra de direcciones de tu navegador
3. Presiona Enter

### ❓ "No veo ninguna cámara"
**Posibles causas:**
1. Estás muy alejado - Haz zoom in
2. Tienes un filtro activo - Cambia a "Todos los distritos"
3. Las cámaras no se cargaron - Vuelve a Vista Lista primero

### ❓ "El mapa se ve en blanco"
**Solución:**
1. Verifica tu conexión a Internet (necesaria para los tiles del mapa)
2. Intenta recargar la página del navegador (F5)
3. Prueba con otro navegador

### ❓ "Los pins están en el lugar equivocado"
**Nota:** 
Las coordenadas provienen del CSV oficial del Ayuntamiento de Málaga.
Si detectas un error, puedes reportarlo a:
https://datosabiertos.malaga.eu

## Diferencias con Otras Vistas

| Característica | Vista Lista | Vista Cuadrícula | Vista Mapa |
|---------------|-------------|------------------|------------|
| Contexto geográfico | ❌ | ❌ | ✅ |
| Miniaturas de cámaras | ✅ | ✅ | ❌ |
| Filtro por zona | ✅ | ✅ | ✅ |
| Ordenación | ✅ | ❌ | ❌ |
| Búsqueda texto | ✅ | ✅ | ❌ |
| Relaciones espaciales | ❌ | ❌ | ✅ |

**Recomendación:** Usa el mapa para ubicar cámaras geográficamente, y las otras vistas para ver las imágenes.

## Preguntas Frecuentes

### ¿Necesito Internet?
Sí, para cargar los tiles del mapa (OpenStreetMap). Las cámaras ya están en tu dispositivo.

### ¿El mapa se actualiza automáticamente?
No, debes hacer click en "Actualizar Mapa" para regenerarlo con datos actuales.

### ¿Puedo guardar el mapa?
Sí, el archivo HTML se guarda temporalmente. Puedes copiarlo a otra ubicación si lo deseas.

### ¿Funciona offline?
Parcialmente. Las cámaras aparecerán, pero el mapa base necesita conexión.

### ¿Puedo compartir el mapa?
Sí, puedes enviar el archivo HTML a otra persona. Se abrirá en su navegador.

### ¿Los colores de distrito son personalizables?
Actualmente no desde la interfaz, pero puedes editarlos en `config.py`.

## Próximas Mejoras

Las siguientes características están planificadas para futuras versiones:

- 🔍 **Búsqueda en el mapa**: Buscar cámaras directamente desde el mapa
- 🖼️ **Miniaturas en popups**: Ver imagen de la cámara sin salir del mapa
- 🛣️ **Rutas**: Calcular rutas entre puntos mostrando cámaras
- 🔥 **Heatmap**: Densidad de cámaras por zona
- 📱 **Geolocalización**: Centrar en tu ubicación actual
- 💾 **Exportar**: Guardar el mapa como imagen PNG

## Más Información

- **Documentación técnica completa**: `MAPA_INTERACTIVO.md`
- **Código fuente**: `src/views/map_view.py`
- **Demo standalone**: `python3 demo_map_test.py`

## Créditos

- Mapa base: OpenStreetMap (licencia ODbL)
- Tecnología de mapas: Folium/Leaflet
- Datos de cámaras: Ayuntamiento de Málaga (Datos Abiertos)

---

**¿Necesitas ayuda?** Contacta con el desarrollador o abre un issue en GitHub.
