# Script de instalación rápida para Windows (PowerShell)
# Cámaras de Tráfico Málaga

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Instalación - Cámaras Tráfico Málaga  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ $pythonVersion encontrado" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python no encontrado. Por favor instala Python 3.10+" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual
Write-Host ""
Write-Host "2. Creando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   ✓ Entorno virtual ya existe" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "   ✓ Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host ""
Write-Host "3. Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Actualizar pip
Write-Host ""
Write-Host "4. Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "   ✓ pip actualizado" -ForegroundColor Green

# Instalar dependencias
Write-Host ""
Write-Host "5. Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "   ✓ Dependencias instaladas" -ForegroundColor Green

# Mensaje final
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✓ Instalación completada exitosamente  " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ejecutar la aplicación:" -ForegroundColor Yellow
Write-Host "  python src/main.py" -ForegroundColor White
Write-Host ""
Write-Host "Si cerraste esta ventana, activa el entorno con:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
