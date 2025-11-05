"""
Estilos y temas para la aplicación.

Este módulo define los estilos Qt para múltiples temas y opciones de personalización.
"""

# Paleta de colores base
COLORS = {
    # Grises
    "negro": "#000000",
    "gris_muy_oscuro": "#1a1a1a",
    "gris_oscuro": "#2c3e50",
    "gris_medio": "#7f8c8d",
    "gris_claro": "#bdc3c7",
    "gris_muy_claro": "#ecf0f1",
    "blanco": "#ffffff",
    
    # Azules
    "azul_muy_oscuro": "#0f1419",
    "azul_oscuro": "#1e3a8a",
    "azul_profundo": "#1e40af",
    "azul_medio": "#3498db",
    "azul_claro": "#74b9ff",
    "azul_muy_claro": "#dbeafe",
    "azul_hielo": "#e0f2fe",
    
    # Verdes
    "verde_muy_oscuro": "#064e3b",
    "verde_oscuro": "#059669",
    "verde_bosque": "#047857",
    "verde_medio": "#10b981",
    "verde_claro": "#6ee7b7",
    "verde_muy_claro": "#d1fae5",
    "verde_menta": "#f0fdf4",
    
    # Rojos
    "rojo_muy_oscuro": "#7f1d1d",
    "rojo_oscuro": "#dc2626",
    "rojo_cereza": "#b91c1c",
    "rojo_medio": "#ef4444",
    "rojo_claro": "#fca5a5",
    "rojo_muy_claro": "#fee2e2",
    
    # Púrpuras
    "purpura_muy_oscuro": "#581c87",
    "purpura_oscuro": "#7c3aed",
    "purpura_real": "#8b5cf6",
    "purpura_medio": "#a855f7",
    "purpura_claro": "#c4b5fd",
    "purpura_muy_claro": "#ede9fe",
    "violeta_nocturno": "#4c1d95",
    "lavanda_relajante": "#f3f4f6",
    
    # Naranjas y amarillos
    "naranja_muy_oscuro": "#9a3412",
    "naranja_oscuro": "#ea580c",
    "naranja_atardecer": "#f97316",
    "naranja_medio": "#fb923c",
    "naranja_claro": "#fed7aa",
    "naranja_muy_claro": "#fff7ed",
    "ambar_dorado": "#f59e0b",
    "amarillo_oscuro": "#ca8a04",
    "amarillo_claro": "#fde047",
    "amarillo_muy_claro": "#fefce8",
    
    # Rosas
    "rosa_muy_oscuro": "#9d174d",
    "rosa_oscuro": "#e11d48",
    "rosa_sakura": "#f43f5e",
    "rosa_medio": "#fb7185",
    "rosa_claro": "#fda4af",
    "rosa_muy_claro": "#fdf2f8",
    "salmon_suave": "#fed7d7",
    
    # Otros colores
    "turquesa_oscuro": "#0f766e",
    "turquesa_tropical": "#14b8a6",
    "turquesa_claro": "#5eead4",
    "turquesa_muy_claro": "#f0fdfa",
    "teal_oceano": "#0891b2",
    "coral_vibrante": "#ff6b6b",
    "oliva_natural": "#84cc16",
    "chocolate_rico": "#92400e",
    "slate_moderno": "#475569",
    "crema": "#fefcf3",
    "beige": "#f5f5dc",
}

# Función para obtener colores de texto
def get_text_color(color_name: str) -> str:
    """Retorna el código de color para texto."""
    color_map = {
        "default": "#2c3e50",
        "negro": COLORS["negro"],
        "blanco": COLORS["blanco"],
        "gris_oscuro": COLORS["gris_oscuro"],
        "gris_claro": COLORS["gris_claro"],
        "azul_oscuro": COLORS["azul_oscuro"],
        "azul_claro": COLORS["azul_claro"],
        "verde_oscuro": COLORS["verde_oscuro"],
        "verde_claro": COLORS["verde_claro"],
        "rojo_oscuro": COLORS["rojo_oscuro"],
        "rojo_claro": COLORS["rojo_claro"],
        "purpura_oscuro": COLORS["purpura_oscuro"],
        "purpura_claro": COLORS["purpura_claro"],
        "naranja_oscuro": COLORS["naranja_oscuro"],
        "naranja_claro": COLORS["naranja_claro"],
        "amarillo_oscuro": COLORS["amarillo_oscuro"],
        "amarillo_claro": COLORS["amarillo_claro"],
        "rosa_oscuro": COLORS["rosa_oscuro"],
        "rosa_claro": COLORS["rosa_claro"],
        "turquesa_oscuro": COLORS["turquesa_oscuro"],
        "turquesa_claro": COLORS["turquesa_claro"],
        "marron_oscuro": COLORS["chocolate_rico"],
        "marron_claro": "#d2691e",
    }
    return color_map.get(color_name, color_map["default"])

# Función para obtener colores de fondo de cajas de texto
def get_textbox_background(color_name: str) -> str:
    """Retorna el código de color para fondo de cajas de texto."""
    color_map = {
        "default": COLORS["blanco"],
        "blanco": COLORS["blanco"],
        "gris_muy_claro": COLORS["gris_muy_claro"],
        "gris_claro": COLORS["gris_claro"],
        "gris_medio": COLORS["gris_medio"],
        "gris_oscuro": COLORS["gris_oscuro"],
        "negro": COLORS["negro"],
        "azul_muy_claro": COLORS["azul_muy_claro"],
        "azul_claro": COLORS["azul_claro"],
        "verde_muy_claro": COLORS["verde_muy_claro"],
        "verde_claro": COLORS["verde_claro"],
        "amarillo_muy_claro": COLORS["amarillo_muy_claro"],
        "amarillo_claro": COLORS["amarillo_claro"],
        "rosa_muy_claro": COLORS["rosa_muy_claro"],
        "rosa_claro": COLORS["rosa_claro"],
        "purpura_muy_claro": COLORS["purpura_muy_claro"],
        "purpura_claro": COLORS["purpura_claro"],
        "naranja_muy_claro": COLORS["naranja_muy_claro"],
        "naranja_claro": COLORS["naranja_claro"],
        "turquesa_muy_claro": COLORS["turquesa_muy_claro"],
        "turquesa_claro": COLORS["turquesa_claro"],
        "crema": COLORS["crema"],
        "beige": COLORS["beige"],
    }
    return color_map.get(color_name, color_map["default"])

# Función para generar tema base
def generate_base_theme(
    bg_main: str,
    bg_sidebar: str, 
    bg_header: str,
    text_main: str,
    text_sidebar: str,
    accent: str,
    border_color: str,
    input_bg: str,
    button_bg: str,
    button_hover: str,
    custom_text_color: str = None,
    custom_textbox_bg: str = None
) -> str:
    """Genera un tema completo con los colores especificados."""
    
    # Usar colores personalizados si se especifican
    final_text_color = custom_text_color if custom_text_color else text_main
    final_textbox_bg = custom_textbox_bg if custom_textbox_bg else input_bg
    
    return f"""
QMainWindow {{
    background-color: {bg_main};
}}

QWidget {{
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: {final_text_color};
}}

/* Barra lateral */
#sidebar {{
    background-color: {bg_sidebar};
    border-right: 2px solid {border_color};
}}

#sidebar QPushButton {{
    background-color: transparent;
    color: {text_sidebar};
    border: none;
    padding: 12px;
    text-align: left;
    font-size: 11pt;
}}

#sidebar QPushButton:hover {{
    background-color: {accent};
}}

#sidebar QPushButton:pressed {{
    background-color: {button_hover};
}}

/* Encabezado */
#header {{
    background-color: {bg_header};
    color: white;
    padding: 15px;
}}

#header QLabel {{
    color: white;
    font-size: 18pt;
    font-weight: bold;
}}

/* Barra de búsqueda */
QLineEdit {{
    padding: 8px;
    border: 1px solid {border_color};
    border-radius: 4px;
    background-color: {final_textbox_bg};
    color: {final_text_color};
}}

QLineEdit:focus {{
    border: 2px solid {accent};
}}

/* Combo boxes */
QComboBox {{
    padding: 6px;
    border: 1px solid {border_color};
    border-radius: 4px;
    background-color: {final_textbox_bg};
    color: {final_text_color};
}}

QComboBox:hover {{
    border: 1px solid {accent};
}}

QComboBox::drop-down {{
    border: none;
}}

QComboBox QAbstractItemView {{
    background-color: {final_textbox_bg};
    color: {final_text_color};
    selection-background-color: {accent};
}}

/* Botones */
QPushButton {{
    background-color: {button_bg};
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {button_hover};
}}

QPushButton:pressed {{
    background-color: {accent};
}}

QPushButton:disabled {{
    background-color: {border_color};
    color: {text_main};
}}

QPushButton#secondary {{
    background-color: {border_color};
}}

QPushButton#secondary:hover {{
    background-color: {accent};
}}

/* Scrollbars */
QScrollBar:vertical {{
    background: {bg_main};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background: {accent};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: {button_hover};
}}

/* Labels */
QLabel {{
    color: {final_text_color};
}}

/* Group boxes */
QGroupBox {{
    border: 1px solid {border_color};
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
    color: {final_text_color};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}}

/* Status bar */
QStatusBar {{
    background-color: {bg_header};
    color: white;
}}
"""

# Definiciones de temas
THEMES = {
    "claro": {
        "bg_main": COLORS["gris_muy_claro"],
        "bg_sidebar": COLORS["gris_oscuro"],
        "bg_header": COLORS["azul_medio"],
        "text_main": COLORS["gris_oscuro"],
        "text_sidebar": COLORS["gris_muy_claro"],
        "accent": COLORS["azul_claro"],
        "border_color": COLORS["gris_claro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["azul_medio"],
        "button_hover": COLORS["azul_oscuro"],
    },
    "oscuro": {
        "bg_main": "#1e1e1e",
        "bg_sidebar": "#252526",
        "bg_header": "#007acc",
        "text_main": "#cccccc",
        "text_sidebar": "#cccccc",
        "accent": "#007acc",
        "border_color": "#3e3e42",
        "input_bg": "#2d2d30",
        "button_bg": "#0e639c",
        "button_hover": "#1177bb",
    },
    "azul_profundo": {
        "bg_main": COLORS["azul_muy_claro"],
        "bg_sidebar": COLORS["azul_profundo"],
        "bg_header": COLORS["azul_muy_oscuro"],
        "text_main": COLORS["azul_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["azul_claro"],
        "border_color": COLORS["azul_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["azul_profundo"],
        "button_hover": COLORS["azul_oscuro"],
    },
    "verde_bosque": {
        "bg_main": COLORS["verde_muy_claro"],
        "bg_sidebar": COLORS["verde_bosque"],
        "bg_header": COLORS["verde_muy_oscuro"],
        "text_main": COLORS["verde_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["verde_claro"],
        "border_color": COLORS["verde_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["verde_bosque"],
        "button_hover": COLORS["verde_oscuro"],
    },
    "purpura_real": {
        "bg_main": COLORS["purpura_muy_claro"],
        "bg_sidebar": COLORS["purpura_real"],
        "bg_header": COLORS["purpura_muy_oscuro"],
        "text_main": COLORS["purpura_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["purpura_claro"],
        "border_color": COLORS["purpura_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["purpura_real"],
        "button_hover": COLORS["purpura_oscuro"],
    },
    "rojo_cereza": {
        "bg_main": COLORS["rojo_muy_claro"],
        "bg_sidebar": COLORS["rojo_cereza"],
        "bg_header": COLORS["rojo_muy_oscuro"],
        "text_main": COLORS["rojo_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["rojo_claro"],
        "border_color": COLORS["rojo_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["rojo_cereza"],
        "button_hover": COLORS["rojo_oscuro"],
    },
    "naranja_atardecer": {
        "bg_main": COLORS["naranja_muy_claro"],
        "bg_sidebar": COLORS["naranja_atardecer"],
        "bg_header": COLORS["naranja_muy_oscuro"],
        "text_main": COLORS["naranja_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["naranja_claro"],
        "border_color": COLORS["naranja_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["naranja_atardecer"],
        "button_hover": COLORS["naranja_oscuro"],
    },
    "rosa_sakura": {
        "bg_main": COLORS["rosa_muy_claro"],
        "bg_sidebar": COLORS["rosa_sakura"],
        "bg_header": COLORS["rosa_muy_oscuro"],
        "text_main": COLORS["rosa_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["rosa_claro"],
        "border_color": COLORS["rosa_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["rosa_sakura"],
        "button_hover": COLORS["rosa_oscuro"],
    },
    "gris_corporativo": {
        "bg_main": COLORS["gris_muy_claro"],
        "bg_sidebar": COLORS["slate_moderno"],
        "bg_header": COLORS["gris_muy_oscuro"],
        "text_main": COLORS["gris_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["gris_medio"],
        "border_color": COLORS["gris_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["slate_moderno"],
        "button_hover": COLORS["gris_oscuro"],
    },
    "azul_hielo": {
        "bg_main": COLORS["azul_hielo"],
        "bg_sidebar": COLORS["teal_oceano"],
        "bg_header": COLORS["azul_oscuro"],
        "text_main": COLORS["azul_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["azul_claro"],
        "border_color": COLORS["azul_medio"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["teal_oceano"],
        "button_hover": COLORS["azul_oscuro"],
    },
    "verde_menta": {
        "bg_main": COLORS["verde_menta"],
        "bg_sidebar": COLORS["oliva_natural"],
        "bg_header": COLORS["verde_muy_oscuro"],
        "text_main": COLORS["verde_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["verde_claro"],
        "border_color": COLORS["verde_medio"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["oliva_natural"],
        "button_hover": COLORS["verde_oscuro"],
    },
    "ambar_dorado": {
        "bg_main": COLORS["amarillo_muy_claro"],
        "bg_sidebar": COLORS["ambar_dorado"],
        "bg_header": COLORS["naranja_muy_oscuro"],
        "text_main": COLORS["naranja_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["amarillo_claro"],
        "border_color": COLORS["amarillo_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["ambar_dorado"],
        "button_hover": COLORS["amarillo_oscuro"],
    },
    "violeta_nocturno": {
        "bg_main": COLORS["purpura_muy_claro"],
        "bg_sidebar": COLORS["violeta_nocturno"],
        "bg_header": COLORS["purpura_muy_oscuro"],
        "text_main": COLORS["violeta_nocturno"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["purpura_claro"],
        "border_color": COLORS["purpura_medio"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["violeta_nocturno"],
        "button_hover": COLORS["purpura_muy_oscuro"],
    },
    "turquesa_tropical": {
        "bg_main": COLORS["turquesa_muy_claro"],
        "bg_sidebar": COLORS["turquesa_tropical"],
        "bg_header": COLORS["turquesa_oscuro"],
        "text_main": COLORS["turquesa_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["turquesa_claro"],
        "border_color": COLORS["teal_oceano"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["turquesa_tropical"],
        "button_hover": COLORS["turquesa_oscuro"],
    },
    "salmon_suave": {
        "bg_main": COLORS["salmon_suave"],
        "bg_sidebar": COLORS["coral_vibrante"],
        "bg_header": COLORS["rojo_muy_oscuro"],
        "text_main": COLORS["rojo_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["rosa_claro"],
        "border_color": COLORS["rosa_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["coral_vibrante"],
        "button_hover": COLORS["rojo_oscuro"],
    },
    "lavanda_relajante": {
        "bg_main": COLORS["lavanda_relajante"],
        "bg_sidebar": COLORS["purpura_medio"],
        "bg_header": COLORS["violeta_nocturno"],
        "text_main": COLORS["purpura_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["purpura_claro"],
        "border_color": COLORS["purpura_real"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["purpura_medio"],
        "button_hover": COLORS["purpura_oscuro"],
    },
    "oliva_natural": {
        "bg_main": COLORS["verde_muy_claro"],
        "bg_sidebar": COLORS["oliva_natural"],
        "bg_header": COLORS["verde_muy_oscuro"],
        "text_main": COLORS["verde_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["verde_claro"],
        "border_color": COLORS["verde_medio"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["oliva_natural"],
        "button_hover": COLORS["verde_oscuro"],
    },
    "chocolate_rico": {
        "bg_main": COLORS["beige"],
        "bg_sidebar": COLORS["chocolate_rico"],
        "bg_header": "#654321",
        "text_main": COLORS["chocolate_rico"],
        "text_sidebar": COLORS["crema"],
        "accent": "#cd853f",
        "border_color": "#8b4513",
        "input_bg": COLORS["crema"],
        "button_bg": COLORS["chocolate_rico"],
        "button_hover": "#654321",
    },
    "slate_moderno": {
        "bg_main": COLORS["gris_muy_claro"],
        "bg_sidebar": COLORS["slate_moderno"],
        "bg_header": COLORS["gris_muy_oscuro"],
        "text_main": COLORS["slate_moderno"],
        "text_sidebar": COLORS["gris_muy_claro"],
        "accent": COLORS["gris_claro"],
        "border_color": COLORS["gris_medio"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["slate_moderno"],
        "button_hover": COLORS["gris_oscuro"],
    },
    "teal_oceano": {
        "bg_main": COLORS["turquesa_muy_claro"],
        "bg_sidebar": COLORS["teal_oceano"],
        "bg_header": COLORS["azul_muy_oscuro"],
        "text_main": COLORS["teal_oceano"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["turquesa_claro"],
        "border_color": COLORS["turquesa_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["teal_oceano"],
        "button_hover": COLORS["turquesa_oscuro"],
    },
    "coral_vibrante": {
        "bg_main": COLORS["rosa_muy_claro"],
        "bg_sidebar": COLORS["coral_vibrante"],
        "bg_header": COLORS["rojo_muy_oscuro"],
        "text_main": COLORS["rojo_muy_oscuro"],
        "text_sidebar": COLORS["blanco"],
        "accent": COLORS["salmon_suave"],
        "border_color": COLORS["rosa_oscuro"],
        "input_bg": COLORS["blanco"],
        "button_bg": COLORS["coral_vibrante"],
        "button_hover": COLORS["rojo_oscuro"],
    },
}

# Temas legados (mantenidos por compatibilidad)
LIGHT_THEME = generate_base_theme(**THEMES["claro"])
DARK_THEME = generate_base_theme(**THEMES["oscuro"])


def get_theme(theme_name: str = "claro", text_color: str = "default", textbox_bg: str = "default") -> str:
    """
    Retorna el stylesheet del tema especificado con personalizaciones opcionales.
    
    Args:
        theme_name: Nombre del tema principal
        text_color: Color personalizado para texto ("default" para usar el del tema)
        textbox_bg: Color personalizado para fondo de cajas de texto ("default" para usar el del tema)
        
    Returns:
        String con el stylesheet Qt
    """
    if theme_name not in THEMES:
        theme_name = "claro"  # Fallback al tema por defecto
    
    theme_config = THEMES[theme_name].copy()
    
    # Aplicar personalizaciones si no son "default"
    custom_text = get_text_color(text_color) if text_color != "default" else None
    custom_textbox = get_textbox_background(textbox_bg) if textbox_bg != "default" else None
    
    return generate_base_theme(
        **theme_config,
        custom_text_color=custom_text,
        custom_textbox_bg=custom_textbox
    )


def get_available_themes() -> list:
    """Retorna la lista de temas disponibles."""
    return list(THEMES.keys())


def get_theme_preview_colors(theme_name: str) -> dict:
    """
    Retorna los colores principales de un tema para preview.
    
    Args:
        theme_name: Nombre del tema
        
    Returns:
        Diccionario con los colores principales del tema
    """
    if theme_name not in THEMES:
        theme_name = "claro"
    
    return {
        "background": THEMES[theme_name]["bg_main"],
        "sidebar": THEMES[theme_name]["bg_sidebar"],
        "header": THEMES[theme_name]["bg_header"],
        "accent": THEMES[theme_name]["accent"],
    }
