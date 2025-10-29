"""
Punto de entrada principal de la aplicación Cámaras de Tráfico Málaga.

Este script inicializa la aplicación Qt y muestra la ventana principal.
"""

import sys
import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Añadir el directorio raíz al path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.views.main_window import MainWindow
import config


def setup_logging():
    """
    Configura el sistema de logging de la aplicación.
    """
    log_format = config.LOG_FORMAT if hasattr(config, 'LOG_FORMAT') else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [
        logging.FileHandler(config.LOG_FILE, encoding='utf-8', mode='w')  # Sobrescribe cada vez
    ]
    
    if config.LOG_TO_CONSOLE if hasattr(config, 'LOG_TO_CONSOLE') else True:
        handlers.append(logging.StreamHandler(sys.stdout))
    
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format=log_format,
        handlers=handlers,
        force=True  # Forzar reconfiguración
    )
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info("Iniciando aplicación Cámaras de Tráfico Málaga")
    logger.info(f"Nivel de log: {config.LOG_LEVEL}")
    logger.info(f"Python version: {sys.version}")
    logger.info("=" * 80)


def main():
    """
    Función principal que ejecuta la aplicación.
    """
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        app.setApplicationName("Cámaras de Tráfico Málaga")
        app.setOrganizationName("Movilidad Málaga")
        
        # Configurar atributos de alta DPI
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Crear y mostrar ventana principal
        logger.info("Creando ventana principal...")
        window = MainWindow()
        window.show()
        
        logger.info("Aplicación iniciada correctamente")
        
        # Ejecutar loop de eventos
        exit_code = app.exec()
        
        logger.info(f"Aplicación finalizada con código: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.critical(f"Error fatal en la aplicación: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
