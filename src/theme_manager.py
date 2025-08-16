"""
Gestor de temas para WikiApp
"""

import json
import os
from typing import Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal

class ThemeManager(QObject):
    theme_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.config_file = "config/theme_config.json"
        self.current_theme = "dark"
        self.load_theme_config()
    
    def load_theme_config(self):
        """Carga la configuración del tema"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_theme = config.get('theme', 'dark')
        except Exception as e:
            print(f"Error cargando configuración de tema: {e}")
            self.current_theme = "dark"
    
    def save_theme_config(self):
        """Guarda la configuración del tema"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            config = {'theme': self.current_theme}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error guardando configuración de tema: {e}")
    
    def toggle_theme(self):
        """Alterna entre tema oscuro y claro"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.save_theme_config()
        self.theme_changed.emit(self.current_theme)
    
    def get_current_theme(self) -> str:
        """Obtiene el tema actual"""
        return self.current_theme
    
    def get_theme_styles(self, theme: str) -> str:
        """Obtiene los estilos CSS para el tema especificado"""
        if theme == "light":
            return self.get_light_theme_styles()
        else:
            return self.get_dark_theme_styles()
    
    def get_dark_theme_styles(self) -> str:
        """Estilos para tema oscuro (ChatGPT style)"""
        try:
            with open("styles/main.qss", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return self.get_default_dark_styles()
    
    def get_light_theme_styles(self) -> str:
        """Estilos para tema claro"""
        return """
        /* WikiApp - Tema Claro */
        QMainWindow {
            background-color: #ffffff;
            color: #1a1a1a;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }
        
        #leftPanel {
            background-color: #f7f7f8;
            border-right: 1px solid #e5e5e5;
            min-width: 280px;
            max-width: 400px;
        }
        
        #panelTitle {
            font-size: 18px;
            font-weight: 600;
            color: #1a1a1a;
            padding: 20px 16px;
            background-color: #f7f7f8;
            border-bottom: 1px solid #e5e5e5;
        }
        
        QLineEdit {
            padding: 12px 16px;
            border: 1px solid #d1d5db;
            border-radius: 12px;
            font-size: 14px;
            background-color: #ffffff;
            color: #1a1a1a;
            margin: 8px;
        }
        
        QLineEdit:focus {
            border-color: #10a37f;
            outline: none;
            background-color: #ffffff;
        }
        
        QLineEdit::placeholder {
            color: #6b7280;
        }
        
        QListWidget {
            background-color: #f9fafb;
            border: none;
            border-radius: 8px;
            margin: 8px;
            padding: 4px;
        }
        
        QListWidget::item {
            padding: 12px 16px;
            border: none;
            background-color: transparent;
            margin: 2px 0;
            border-radius: 8px;
            color: #1a1a1a;
        }
        
        QListWidget::item:hover {
            background-color: #f3f4f6;
        }
        
        QListWidget::item:selected {
            background-color: #10a37f;
            color: white;
        }
        
        QPushButton {
            background-color: #10a37f;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: 500;
            margin: 4px;
            min-height: 16px;
            font-size: 14px;
        }
        
        QPushButton:hover {
            background-color: #0d8f6b;
        }
        
        QPushButton:pressed {
            background-color: #0a7c5f;
        }
        
        QPushButton:disabled {
            background-color: #e5e7eb;
            color: #9ca3af;
        }
        
        QTextBrowser {
            background-color: #ffffff;
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            padding: 24px;
            font-size: 15px;
            line-height: 1.6;
            color: #1a1a1a;
        }
        
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            padding: 16px;
            font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
            color: #1a1a1a;
        }
        
        QTextEdit:focus {
            border-color: #10a37f;
            background-color: #ffffff;
        }
        
        QComboBox {
            padding: 8px 16px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            background-color: #ffffff;
            color: #1a1a1a;
            margin: 8px;
            min-height: 20px;
        }
        
        QComboBox:hover {
            background-color: #f9fafb;
            border-color: #10a37f;
        }
        
        QComboBox QAbstractItemView {
            border: 1px solid #d1d5db;
            background-color: #ffffff;
            color: #1a1a1a;
            selection-background-color: #10a37f;
            border-radius: 8px;
        }
        
        QToolBar {
            background-color: #f7f7f8;
            border: none;
            border-bottom: 1px solid #e5e5e5;
            padding: 8px 16px;
            spacing: 12px;
        }
        
        QToolBar QToolButton {
            background-color: transparent;
            color: #1a1a1a;
            padding: 10px 16px;
            border-radius: 8px;
            margin: 2px;
            font-size: 14px;
        }
        
        QToolBar QToolButton:hover {
            background-color: #f3f4f6;
        }
        
        QStatusBar {
            background-color: #f7f7f8;
            color: #6b7280;
            border-top: 1px solid #e5e5e5;
            padding: 8px 16px;
            font-size: 12px;
        }
        
        QTabWidget::pane {
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            background-color: #ffffff;
        }
        
        QTabBar::tab {
            background-color: #f3f4f6;
            color: #6b7280;
            padding: 12px 24px;
            margin-right: 4px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border: none;
            font-size: 14px;
            font-weight: 500;
        }
        
        QTabBar::tab:selected {
            background-color: #ffffff;
            color: #1a1a1a;
            border-bottom: 2px solid #10a37f;
        }
        
        QTabBar::tab:hover:!selected {
            background-color: #e5e7eb;
            color: #1a1a1a;
        }
        
        QLabel {
            color: #1a1a1a;
            font-size: 14px;
        }
        
        #articleTitle {
            font-size: 28px;
            font-weight: 600;
            color: #1a1a1a;
            padding: 16px 0;
            border-bottom: 2px solid #10a37f;
            margin-bottom: 16px;
        }
        
        #articleMeta {
            font-size: 13px;
            color: #6b7280;
            padding: 8px 0;
            margin-bottom: 20px;
        }
        
        QScrollBar:vertical {
            background-color: #f9fafb;
            width: 8px;
            border-radius: 4px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #d1d5db;
            border-radius: 4px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #9ca3af;
        }
        
        QDialog {
            background-color: #ffffff;
            color: #1a1a1a;
        }
        
        #dialogTitle {
            font-size: 18px;
            font-weight: 600;
            color: #1a1a1a;
            padding: 16px;
            background-color: #f7f7f8;
            border-radius: 12px;
            margin-bottom: 16px;
            border: 1px solid #e5e5e5;
        }
        """
    
    def get_default_dark_styles(self) -> str:
        """Estilos por defecto para tema oscuro"""
        return """
        QMainWindow {
            background-color: #212121;
            color: #ececec;
        }
        QPushButton {
            background-color: #10a37f;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
        }
        """