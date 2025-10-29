"""
Script de verificación del proyecto.

Verifica que todos los archivos necesarios existan y que las 
dependencias estén correctamente instaladas.
"""

import sys
from pathlib import Path
import importlib.util


def check_file(path: Path, description: str) -> bool:
    """Verifica si un archivo existe."""
    if path.exists():
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - FALTA")
        return False


def check_dependency(module_name: str) -> bool:
    """Verifica si una dependencia está instalada."""
    spec = importlib.util.find_spec(module_name)
    if spec is not None:
        print(f"✓ {module_name}")
        return True
    else:
        print(f"✗ {module_name} - NO INSTALADO")
        return False


def main():
    """Función principal de verificación."""
    print("=" * 50)
    print("  Verificación del Proyecto")
    print("=" * 50)
    print()
    
    root = Path(__file__).parent
    all_ok = True
    
    # Verificar estructura de directorios
    print("📁 Estructura de directorios:")
    print("-" * 50)
    
    dirs_to_check = [
        (root / "src", "src/"),
        (root / "src" / "models", "src/models/"),
        (root / "src" / "views", "src/views/"),
        (root / "src" / "controllers", "src/controllers/"),
        (root / "src" / "utils", "src/utils/"),
    ]
    
    for dir_path, description in dirs_to_check:
        if not check_file(dir_path, description):
            all_ok = False
    
    print()
    
    # Verificar archivos principales
    print("📄 Archivos principales:")
    print("-" * 50)
    
    files_to_check = [
        (root / "config.py", "config.py"),
        (root / "requirements.txt", "requirements.txt"),
        (root / "README.md", "README.md"),
        (root / "src" / "main.py", "src/main.py"),
        (root / "src" / "models" / "camera.py", "src/models/camera.py"),
        (root / "src" / "views" / "main_window.py", "src/views/main_window.py"),
        (root / "src" / "controllers" / "camera_controller.py", "src/controllers/camera_controller.py"),
        (root / "src" / "utils" / "data_loader.py", "src/utils/data_loader.py"),
        (root / "src" / "utils" / "image_loader.py", "src/utils/image_loader.py"),
    ]
    
    for file_path, description in files_to_check:
        if not check_file(file_path, description):
            all_ok = False
    
    print()
    
    # Verificar dependencias
    print("📦 Dependencias:")
    print("-" * 50)
    
    dependencies = [
        "PySide6",
        "pandas",
        "numpy",
        "requests",
        "PIL",  # Pillow
    ]
    
    for dep in dependencies:
        if not check_dependency(dep):
            all_ok = False
    
    print()
    print("=" * 50)
    
    if all_ok:
        print("✓ VERIFICACIÓN EXITOSA - Todo listo para ejecutar")
        print()
        print("Ejecuta la aplicación con:")
        print("  python src/main.py")
        return 0
    else:
        print("✗ VERIFICACIÓN FALLIDA - Hay problemas pendientes")
        print()
        print("Por favor:")
        print("1. Verifica que todos los archivos existan")
        print("2. Instala las dependencias: pip install -r requirements.txt")
        return 1
    
    print("=" * 50)


if __name__ == "__main__":
    sys.exit(main())
