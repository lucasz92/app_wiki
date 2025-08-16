#!/usr/bin/env python3
"""
WikiApp - Aplicación de documentación estilo wiki
Autor: Kiro AI Assistant
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.main_window import MainWindow
from src.database import DatabaseManager

def main():
    app = QApplication(sys.argv)
    
    # Inicializar base de datos
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    # Crear ventana principal
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()