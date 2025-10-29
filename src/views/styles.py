"""
Estilos y temas para la aplicación.

Este módulo define los estilos Qt para temas claro y oscuro.
"""

# Tema Claro
LIGHT_THEME = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

/* Barra lateral */
#sidebar {
    background-color: #2c3e50;
    border-right: 2px solid #34495e;
}

#sidebar QPushButton {
    background-color: transparent;
    color: #ecf0f1;
    border: none;
    padding: 12px;
    text-align: left;
    font-size: 11pt;
}

#sidebar QPushButton:hover {
    background-color: #34495e;
}

#sidebar QPushButton:pressed {
    background-color: #1abc9c;
}

/* Encabezado */
#header {
    background-color: #3498db;
    color: white;
    padding: 15px;
}

#header QLabel {
    color: white;
    font-size: 18pt;
    font-weight: bold;
}

/* Barra de búsqueda */
QLineEdit {
    padding: 8px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    background-color: white;
}

QLineEdit:focus {
    border: 2px solid #3498db;
}

/* Combo boxes */
QComboBox {
    padding: 6px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    background-color: white;
}

QComboBox:hover {
    border: 1px solid #3498db;
}

QComboBox::drop-down {
    border: none;
}

/* Botones */
QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #21618c;
}

QPushButton:disabled {
    background-color: #95a5a6;
}

/* Botón secundario */
QPushButton#secondary {
    background-color: #95a5a6;
}

QPushButton#secondary:hover {
    background-color: #7f8c8d;
}

/* Lista de cámaras */
QListWidget {
    background-color: white;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #ecf0f1;
}

QListWidget::item:selected {
    background-color: #3498db;
    color: white;
}

QListWidget::item:hover {
    background-color: #ecf0f1;
}

/* Scroll bars */
QScrollBar:vertical {
    background: #ecf0f1;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #95a5a6;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #7f8c8d;
}

/* Labels */
QLabel {
    color: #2c3e50;
}

/* Group boxes */
QGroupBox {
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

/* Status bar */
QStatusBar {
    background-color: #ecf0f1;
    color: #2c3e50;
}
"""

# Tema Oscuro
DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: #e0e0e0;
}

/* Barra lateral */
#sidebar {
    background-color: #252526;
    border-right: 2px solid #3e3e42;
}

#sidebar QPushButton {
    background-color: transparent;
    color: #cccccc;
    border: none;
    padding: 12px;
    text-align: left;
    font-size: 11pt;
}

#sidebar QPushButton:hover {
    background-color: #2d2d30;
}

#sidebar QPushButton:pressed {
    background-color: #007acc;
}

/* Encabezado */
#header {
    background-color: #007acc;
    color: white;
    padding: 15px;
}

#header QLabel {
    color: white;
    font-size: 18pt;
    font-weight: bold;
}

/* Barra de búsqueda */
QLineEdit {
    padding: 8px;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    background-color: #2d2d30;
    color: #cccccc;
}

QLineEdit:focus {
    border: 2px solid #007acc;
}

/* Combo boxes */
QComboBox {
    padding: 6px;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    background-color: #2d2d30;
    color: #cccccc;
}

QComboBox:hover {
    border: 1px solid #007acc;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background-color: #2d2d30;
    color: #cccccc;
    selection-background-color: #007acc;
}

/* Botones */
QPushButton {
    background-color: #0e639c;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1177bb;
}

QPushButton:pressed {
    background-color: #007acc;
}

QPushButton:disabled {
    background-color: #3e3e42;
    color: #6e6e6e;
}

/* Botón secundario */
QPushButton#secondary {
    background-color: #3e3e42;
}

QPushButton#secondary:hover {
    background-color: #4e4e52;
}

/* Lista de cámaras */
QListWidget {
    background-color: #2d2d30;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    color: #cccccc;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #3e3e42;
}

QListWidget::item:selected {
    background-color: #007acc;
    color: white;
}

QListWidget::item:hover {
    background-color: #3e3e42;
}

/* Scroll bars */
QScrollBar:vertical {
    background: #1e1e1e;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #424242;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #4e4e4e;
}

/* Labels */
QLabel {
    color: #cccccc;
}

/* Group boxes */
QGroupBox {
    border: 1px solid #3e3e42;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
    color: #cccccc;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

/* Status bar */
QStatusBar {
    background-color: #007acc;
    color: white;
}
"""


def get_theme(theme_name: str = "claro") -> str:
    """
    Retorna el stylesheet del tema especificado.
    
    Args:
        theme_name: "claro" u "oscuro"
        
    Returns:
        String con el stylesheet Qt
    """
    if theme_name.lower() == "oscuro":
        return DARK_THEME
    return LIGHT_THEME
