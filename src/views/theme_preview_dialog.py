"""
Diálogo de vista previa de temas.

Este módulo proporciona una interfaz para previsualizar diferentes temas
antes de aplicarlos.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGridLayout, QFrame, QScrollArea, QWidget, QComboBox, QGroupBox
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPalette, QPixmap, QPainter, QColor
import logging

from src.views.styles import get_theme, get_available_themes, get_theme_preview_colors
import config

logger = logging.getLogger(__name__)


class ThemePreviewWidget(QFrame):
    """Widget que muestra una vista previa de un tema."""
    
    theme_selected = Signal(str)  # Signal emitido cuando se selecciona un tema
    
    def __init__(self, theme_name: str, parent=None):
        super().__init__(parent)
        self.theme_name = theme_name
        self.setFixedSize(200, 120)
        self.setFrameStyle(QFrame.Box)
        self.setCursor(Qt.PointingHandCursor)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura la interfaz del widget de vista previa."""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Título del tema
        theme_display_name = self._get_display_name(self.theme_name)
        title = QLabel(theme_display_name)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 9pt;")
        layout.addWidget(title)
        
        # Vista previa de colores
        colors_widget = self._create_color_preview()
        layout.addWidget(colors_widget)
        
        self.setLayout(layout)
        
        # Aplicar estilo del tema a este widget
        self._apply_preview_style()
        
    def _create_color_preview(self) -> QWidget:
        """Crea una vista previa de los colores del tema."""
        widget = QWidget()
        widget.setFixedHeight(70)
        
        colors = get_theme_preview_colors(self.theme_name)
        
        layout = QGridLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear muestras de color
        color_samples = [
            ("Fondo", colors["background"]),
            ("Barra", colors["sidebar"]),
            ("Encabezado", colors["header"]),
            ("Acento", colors["accent"])
        ]
        
        for i, (name, color) in enumerate(color_samples):
            sample = QLabel()
            sample.setFixedSize(35, 25)
            sample.setStyleSheet(f"""
                background-color: {color};
                border: 1px solid #666;
                border-radius: 3px;
            """)
            sample.setToolTip(f"{name}: {color}")
            
            row = i // 2
            col = i % 2
            layout.addWidget(sample, row, col)
        
        widget.setLayout(layout)
        return widget
        
    def _apply_preview_style(self):
        """Aplica el estilo de vista previa al widget."""
        colors = get_theme_preview_colors(self.theme_name)
        
        self.setStyleSheet(f"""
            ThemePreviewWidget {{
                background-color: {colors["background"]};
                border: 2px solid #ccc;
                border-radius: 8px;
            }}
            ThemePreviewWidget:hover {{
                border: 3px solid {colors["accent"]};
            }}
            QLabel {{
                color: {'#000' if self._is_light_color(colors["background"]) else '#fff'};
            }}
        """)
        
    def _get_display_name(self, theme_name: str) -> str:
        """Convierte el nombre interno del tema a nombre mostrado."""
        name_map = {
            "claro": "Claro",
            "oscuro": "Oscuro",
            "azul_profundo": "Azul Profundo",
            "verde_bosque": "Verde Bosque",
            "purpura_real": "Púrpura Real",
            "rojo_cereza": "Rojo Cereza",
            "naranja_atardecer": "Naranja Atardecer",
            "rosa_sakura": "Rosa Sakura",
            "gris_corporativo": "Gris Corporativo",
            "azul_hielo": "Azul Hielo",
            "verde_menta": "Verde Menta",
            "ambar_dorado": "Ámbar Dorado",
            "violeta_nocturno": "Violeta Nocturno",
            "turquesa_tropical": "Turquesa Tropical",
            "salmon_suave": "Salmón Suave",
            "lavanda_relajante": "Lavanda Relajante",
            "oliva_natural": "Oliva Natural",
            "chocolate_rico": "Chocolate Rico",
            "slate_moderno": "Slate Moderno",
            "teal_oceano": "Teal Océano",
            "coral_vibrante": "Coral Vibrante"
        }
        return name_map.get(theme_name, theme_name.replace("_", " ").title())
        
    def _is_light_color(self, color_hex: str) -> bool:
        """Determina si un color es claro u oscuro."""
        try:
            # Convertir hex a RGB
            color_hex = color_hex.lstrip('#')
            if len(color_hex) == 6:
                r = int(color_hex[0:2], 16)
                g = int(color_hex[2:4], 16)
                b = int(color_hex[4:6], 16)
                
                # Calcular luminancia
                luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                return luminance > 0.5
        except:
            pass
        return True  # Por defecto asumir que es claro
        
    def mousePressEvent(self, event):
        """Maneja el clic en el widget de vista previa."""
        if event.button() == Qt.LeftButton:
            self.theme_selected.emit(self.theme_name)
        super().mousePressEvent(event)


class ThemePreviewDialog(QDialog):
    """Diálogo para previsualizar y seleccionar temas."""
    
    theme_applied = Signal(str)  # Signal emitido cuando se aplica un tema
    
    def __init__(self, current_theme: str, parent=None):
        super().__init__(parent)
        self.current_theme = current_theme
        self.selected_theme = current_theme
        
        self.setWindowTitle("Vista Previa de Temas")
        self.setFixedSize(800, 600)
        self.setModal(True)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura la interfaz del diálogo."""
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("🎨 Seleccionar Tema")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16pt; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Área de scroll para las vistas previas
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QGridLayout()
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        
        # Crear vistas previas para todos los temas
        themes = get_available_themes()
        cols = 3  # Número de columnas
        
        for i, theme_name in enumerate(themes):
            preview_widget = ThemePreviewWidget(theme_name)
            preview_widget.theme_selected.connect(self._on_theme_selected)
            
            # Destacar el tema actual
            if theme_name == self.current_theme:
                preview_widget.setStyleSheet(preview_widget.styleSheet() + """
                    ThemePreviewWidget {
                        border: 3px solid #ff6b35 !important;
                    }
                """)
            
            row = i // cols
            col = i % cols
            scroll_layout.addWidget(preview_widget, row, col)
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # Información del tema seleccionado
        self.info_label = QLabel(f"Tema seleccionado: {self._get_display_name(self.selected_theme)}")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 12pt; margin: 10px; padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.info_label)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.btn_apply = QPushButton("✓ Aplicar Tema")
        self.btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.btn_apply.clicked.connect(self._apply_theme)
        
        self.btn_cancel = QPushButton("✗ Cancelar")
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.btn_cancel.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_cancel)
        button_layout.addWidget(self.btn_apply)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def _on_theme_selected(self, theme_name: str):
        """Maneja la selección de un tema."""
        self.selected_theme = theme_name
        display_name = self._get_display_name(theme_name)
        self.info_label.setText(f"Tema seleccionado: {display_name}")
        logger.info(f"Tema seleccionado en vista previa: {theme_name}")
        
    def _apply_theme(self):
        """Aplica el tema seleccionado."""
        self.theme_applied.emit(self.selected_theme)
        self.accept()
        
    def _get_display_name(self, theme_name: str) -> str:
        """Convierte el nombre interno del tema a nombre mostrado."""
        name_map = {
            "claro": "Claro",
            "oscuro": "Oscuro",
            "azul_profundo": "Azul Profundo",
            "verde_bosque": "Verde Bosque",
            "purpura_real": "Púrpura Real",
            "rojo_cereza": "Rojo Cereza",
            "naranja_atardecer": "Naranja Atardecer",
            "rosa_sakura": "Rosa Sakura",
            "gris_corporativo": "Gris Corporativo",
            "azul_hielo": "Azul Hielo",
            "verde_menta": "Verde Menta",
            "ambar_dorado": "Ámbar Dorado",
            "violeta_nocturno": "Violeta Nocturno",
            "turquesa_tropical": "Turquesa Tropical",
            "salmon_suave": "Salmón Suave",
            "lavanda_relajante": "Lavanda Relajante",
            "oliva_natural": "Oliva Natural",
            "chocolate_rico": "Chocolate Rico",
            "slate_moderno": "Slate Moderno",
            "teal_oceano": "Teal Océano",
            "coral_vibrante": "Coral Vibrante"
        }
        return name_map.get(theme_name, theme_name.replace("_", " ").title())