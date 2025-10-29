# 🎯 Guía de Inicio Rápido

## ⚡ Instalación Express (5 minutos)

### Windows

```powershell
# 1. Abrir PowerShell en el directorio del proyecto

# 2. Ejecutar script de instalación
.\install.ps1

# 3. Ejecutar la aplicación
python src/main.py
```

### Linux/Mac

```bash
# 1. Abrir terminal en el directorio del proyecto

# 2. Dar permisos de ejecución
chmod +x install.sh

# 3. Ejecutar script de instalación
./install.sh

# 4. Ejecutar la aplicación
python src/main.py
```

---

## 🎮 Primeros Pasos

### 1. Al iniciar la aplicación

La aplicación descargará automáticamente:
- ✅ Lista actualizada de cámaras de tráfico de Málaga
- ✅ Imágenes en tiempo real de las primeras cámaras

**Nota**: Requiere conexión a Internet la primera vez.

### 2. Navega por las cámaras

#### Vista Lista (por defecto)
- Lista compacta con miniaturas
- Scroll vertical para ver todas
- Clic en cualquier cámara para ver detalles

#### Vista Cuadrícula
- Tarjetas grandes con imágenes destacadas
- Diseño tipo galería
- Botón "Vista Cuadrícula" en la barra lateral

### 3. Busca y filtra

**Barra de búsqueda**:
```
Ejemplo: "Alameda"
Ejemplo: "Carretera Cadiz"
```

**Filtro por zona**:
- Desplegable con todas las zonas de Málaga
- Agrupa cámaras automáticamente
- "Todas" para ver todo

### 4. Actualiza imágenes

**Manual**: 
- Botón "🔄 Actualizar Todo" (barra lateral)
- O botón individual en cada cámara

**Automático**:
- Activa "⏱ Auto-refresco" en la barra lateral
- Refresca cada 30 segundos automáticamente

### 5. Personaliza

**Cambiar tema**:
- Botón "🌓 Cambiar Tema" en barra lateral
- Alterna entre claro y oscuro

---

## 🔍 Características Principales

| Característica | Descripción |
|----------------|-------------|
| 📹 **Tiempo Real** | Imágenes actualizadas constantemente |
| 🗺️ **Zonas** | Agrupación inteligente por ubicación |
| 🔍 **Búsqueda** | Encuentra cámaras por nombre o dirección |
| 📊 **Vistas** | Lista compacta o cuadrícula visual |
| 🔄 **Auto-refresh** | Actualización automática configurable |
| 🎨 **Temas** | Claro y oscuro |
| 📋 **Detalles** | Info completa de cada cámara |

---

## ❓ Solución de Problemas

### Error: "No se pudieron cargar los datos"

**Causa**: Sin conexión a Internet o servidor no disponible

**Solución**:
1. Verifica tu conexión a Internet
2. Cierra y reinicia la aplicación
3. Si persiste, verifica en https://datosabiertos.malaga.eu

### Error: "Error cargando imagen"

**Causa**: Cámara específica temporalmente no disponible

**Solución**:
- Haz clic en "🔄 Actualizar" en esa cámara
- O espera a que el auto-refresco la intente de nuevo

### La aplicación va lenta

**Solución**:
1. Cierra otras aplicaciones pesadas
2. Reduce el número de cámaras visibles (usa filtros)
3. Desactiva auto-refresco si no lo necesitas

### No se instalan las dependencias

**Windows**:
```powershell
# Actualizar pip manualmente
python -m pip install --upgrade pip

# Instalar una a una
pip install PySide6
pip install pandas
pip install requests
pip install Pillow
```

**Linux/Mac**:
```bash
# Asegurarte de tener Python 3.10+
python3 --version

# Usar pip3 explícitamente
pip3 install -r requirements.txt
```

---

## 📚 Documentación Completa

- **README.md**: Documentación general completa
- **ARCHITECTURE.md**: Detalles técnicos de arquitectura
- **FUENTES.md**: Información sobre las fuentes de datos

---

## 🎓 Atajos de Teclado

_Próximamente en futuras versiones_

---

## 💡 Tips y Trucos

### Tip 1: Mejora el rendimiento
- Usa los filtros para reducir cámaras visibles
- Vista Lista consume menos recursos que Cuadrícula

### Tip 2: Encuentra tu zona rápido
- El filtro de zonas agrupa automáticamente
- Busca por nombre de calle para encontrar cámaras específicas

### Tip 3: Monitoriza tráfico
- Activa auto-refresco
- Coloca varias cámaras en vista cuadrícula
- Minimiza la ventana y consulta periódicamente

### Tip 4: Accede a la web oficial
- Clic en "Ver detalles" de cualquier cámara
- Verás el enlace a la página oficial del Ayuntamiento

---

## 🚀 Próximos Pasos

Una vez familiarizado con la aplicación:

1. **Personaliza** `config.py` con tus preferencias
2. **Explora** todas las zonas de Málaga
3. **Configura** el intervalo de auto-refresco
4. **Comparte** feedback para futuras mejoras

---

## 📧 Soporte

¿Problemas o sugerencias?

- **Issues**: [GitHub Issues](https://github.com/partybrasil/Movilidad-de-Malaga-Camaras-de-Trafico/issues)
- **Documentación**: Lee README.md y ARCHITECTURE.md
- **Verificación**: Ejecuta `python verify.py` para diagnosticar

---

**¡Disfruta monitoreando el tráfico de Málaga en tiempo real! 🚦🚗**
