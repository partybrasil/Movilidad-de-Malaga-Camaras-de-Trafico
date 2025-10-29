# 🚦 Cámaras de Tráfico - Málaga

Aplicación de escritorio moderna para visualizar en tiempo real las cámaras de tráfico de Málaga, utilizando datos abiertos oficiales del Ayuntamiento.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Características

- 📹 **Visualización en tiempo real** de todas las cámaras de tráfico
- 🗺️ **Agrupación por zonas** y distritos de Málaga
- 🔍 **Búsqueda avanzada** por nombre o ubicación
- 📋 **Vista lista y cuadrícula** intercambiables
- 🔄 **Actualización automática** de imágenes configurable
- 🎨 **Temas claro y oscuro** para mejor experiencia
- ⚡ **Carga asíncrona** de imágenes sin bloquear la interfaz
- 💾 **Caché inteligente** para mejor rendimiento
- 🏗️ **Arquitectura MVC** limpia y escalable
- 🗺️ **Preparado para integración futura** con mapas interactivos

## 📋 Requisitos

- Python 3.10 o superior
- Conexión a Internet (para cargar datos e imágenes)

## 🚀 Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/partybrasil/Movilidad-de-Malaga-Camaras-de-Trafico.git
cd Movilidad-de-Malaga-Camaras-de-Trafico
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv
```

3. **Activar entorno virtual:**

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 🎮 Uso

**Ejecutar la aplicación:**
```bash
python src/main.py
```

### Funcionalidades principales:

#### 🔍 Búsqueda y Filtros
- Busca cámaras por nombre o dirección en la barra superior
- Filtra por zona utilizando el combo desplegable
- Limpia todos los filtros con el botón "Limpiar"

#### 📊 Vistas
- **Vista Lista**: Muestra las cámaras en formato compacto con miniaturas
- **Vista Cuadrícula**: Despliega las cámaras en tarjetas con imágenes grandes

#### 🔄 Actualización
- **Actualizar Todo**: Refresca todas las imágenes manualmente
- **Auto-refresco**: Activa actualización automática cada 30 segundos
- **Actualizar Individual**: Cada cámara tiene su botón de refresco

#### 🎨 Personalización
- Cambia entre tema claro y oscuro con el botón "Cambiar Tema"
- La configuración se puede ajustar en `config.py`

#### 📋 Detalles de Cámara
- Haz clic en "Ver detalles" para información completa
- Accede al enlace web oficial de la cámara
- Visualiza coordenadas para futura integración con mapas

## 🏗️ Arquitectura del Proyecto

```
Movilidad-de-Malaga-Camaras-de-Trafico/
├── src/
│   ├── main.py                      # Punto de entrada
│   ├── models/
│   │   └── camera.py               # Modelo de datos de cámara
│   ├── views/
│   │   ├── main_window.py          # Ventana principal
│   │   ├── camera_widget.py        # Widgets de cámara
│   │   └── styles.py               # Estilos Qt (temas)
│   ├── controllers/
│   │   └── camera_controller.py    # Lógica de negocio
│   └── utils/
│       ├── data_loader.py          # Carga del CSV
│       └── image_loader.py         # Carga asíncrona de imágenes
├── config.py                        # Configuración global
├── requirements.txt                 # Dependencias
├── README.md                        # Este archivo
├── LICENSE                          # Licencia MIT
└── FUENTES.md                       # Fuentes de datos
```

### Patrón de Diseño: MVC (Model-View-Controller)

- **Models** (`src/models/`): Clases de datos (Camera)
- **Views** (`src/views/`): Interfaz gráfica con PySide6
- **Controllers** (`src/controllers/`): Lógica de negocio y coordinación
- **Utils** (`src/utils/`): Utilidades para carga de datos e imágenes

## ⚙️ Configuración

Edita `config.py` para personalizar:

```python
# Intervalo de actualización automática (segundos)
IMAGE_REFRESH_INTERVAL = 30

# Tamaño de miniaturas
THUMBNAIL_SIZE = (320, 240)

# Columnas en vista cuadrícula
GRID_COLUMNS = 3

# Tema por defecto ("claro" u "oscuro")
DEFAULT_THEME = "claro"

# Habilitar/deshabilitar caché de imágenes
ENABLE_IMAGE_CACHE = True
CACHE_MAX_SIZE = 100
```

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

## 🔮 Roadmap / Futuras Mejoras

- [ ] **Mapa interactivo** con ubicación de cámaras (OpenStreetMap/Leaflet)
- [ ] **Comparación múltiple** de cámaras lado a lado
- [ ] **Historial de imágenes** con timeline
- [ ] **Notificaciones** de incidencias de tráfico
- [ ] **Exportar datos** (PDF, imágenes)
- [ ] **Estadísticas** de uso y tráfico
- [ ] **Favoritos** personalizados
- [ ] **API REST** para integración externa

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Movilidad Málaga Team**

## 🙏 Agradecimientos

- Ayuntamiento de Málaga por proporcionar los datos abiertos
- Comunidad de PySide6/Qt
- Todos los contribuidores del proyecto

## 📧 Contacto

Para preguntas, sugerencias o reportar problemas, abre un [issue](https://github.com/partybrasil/Movilidad-de-Malaga-Camaras-de-Trafico/issues) en GitHub.

---

**⚠️ Nota**: Esta aplicación es un prototipo educativo. Las imágenes y datos provienen de fuentes oficiales públicas del Ayuntamiento de Málaga.
