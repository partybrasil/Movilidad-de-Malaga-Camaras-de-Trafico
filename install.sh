#!/bin/bash
# Script de instalación rápida para Linux/Mac
# Cámaras de Tráfico Málaga

echo "========================================"
echo "  Instalación - Cámaras Tráfico Málaga  "
echo "========================================"
echo ""

# Verificar Python
echo "1. Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✓ $PYTHON_VERSION encontrado"
else
    echo "   ✗ Python3 no encontrado. Por favor instala Python 3.10+"
    exit 1
fi

# Crear entorno virtual
echo ""
echo "2. Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "   ✓ Entorno virtual ya existe"
else
    python3 -m venv venv
    echo "   ✓ Entorno virtual creado"
fi

# Activar entorno virtual
echo ""
echo "3. Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo ""
echo "4. Actualizando pip..."
python -m pip install --upgrade pip --quiet
echo "   ✓ pip actualizado"

# Instalar dependencias
echo ""
echo "5. Instalando dependencias..."
pip install -r requirements.txt --quiet
echo "   ✓ Dependencias instaladas"

# Mensaje final
echo ""
echo "========================================"
echo "  ✓ Instalación completada exitosamente  "
echo "========================================"
echo ""
echo "Para ejecutar la aplicación:"
echo "  python src/main.py"
echo ""
echo "Si cerraste esta terminal, activa el entorno con:"
echo "  source venv/bin/activate"
echo ""
