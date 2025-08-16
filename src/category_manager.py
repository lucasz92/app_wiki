"""
Gestor de categorías
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                            QPushButton, QLineEdit, QLabel, QColorDialog, 
                            QMessageBox, QListWidgetItem, QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class CategoryManager(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        
        self.setWindowTitle("Gestor de Categorías")
        self.setGeometry(300, 300, 500, 400)
        
        self.setup_ui()
        self.load_categories()
    
    def setup_ui(self):
        """Configura la interfaz del gestor"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("📁 Gestión de Categorías")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)
        
        # Lista de categorías
        self.categories_list = QListWidget()
        layout.addWidget(self.categories_list)
        
        # Formulario para nueva categoría
        form_layout = QVBoxLayout()
        
        form_layout.addWidget(QLabel("Nueva Categoría:"))
        
        # Nombre
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nombre:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)
        
        # Descripción
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Descripción:"))
        self.desc_input = QLineEdit()
        desc_layout.addWidget(self.desc_input)
        form_layout.addLayout(desc_layout)
        
        # Color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.color_btn = QPushButton("Seleccionar Color")
        self.color_btn.clicked.connect(self.select_color)
        self.selected_color = "#3498db"
        self.update_color_button()
        color_layout.addWidget(self.color_btn)
        form_layout.addLayout(color_layout)
        
        layout.addLayout(form_layout)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("➕ Agregar")
        self.add_btn.clicked.connect(self.add_category)
        buttons_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("✏️ Editar")
        self.edit_btn.clicked.connect(self.edit_category)
        self.edit_btn.setEnabled(False)
        buttons_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("🗑️ Eliminar")
        self.delete_btn.clicked.connect(self.delete_category)
        self.delete_btn.setEnabled(False)
        buttons_layout.addWidget(self.delete_btn)
        
        layout.addLayout(buttons_layout)
        
        # Botones del diálogo
        dialog_buttons = QHBoxLayout()
        
        self.close_btn = QPushButton("Cerrar")
        self.close_btn.clicked.connect(self.accept)
        dialog_buttons.addWidget(self.close_btn)
        
        layout.addLayout(dialog_buttons)
        
        # Conectar selección de lista
        self.categories_list.itemSelectionChanged.connect(self.on_category_selected)
    
    def load_categories(self):
        """Carga las categorías en la lista"""
        self.categories_list.clear()
        categories = self.db_manager.get_categories()
        
        for category in categories:
            item = QListWidgetItem(f"📁 {category['name']}")
            item.setData(Qt.ItemDataRole.UserRole, category)
            
            # Aplicar color de categoría
            color = QColor(category.get('color', '#3498db'))
            item.setBackground(color.lighter(180))
            
            item.setToolTip(f"Descripción: {category.get('description', 'Sin descripción')}")
            
            self.categories_list.addItem(item)
    
    def on_category_selected(self):
        """Maneja la selección de categoría"""
        selected_items = self.categories_list.selectedItems()
        has_selection = len(selected_items) > 0
        
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        
        if has_selection:
            category = selected_items[0].data(Qt.ItemDataRole.UserRole)
            self.name_input.setText(category['name'])
            self.desc_input.setText(category.get('description', ''))
            self.selected_color = category.get('color', '#3498db')
            self.update_color_button()
    
    def select_color(self):
        """Abre el selector de color"""
        color = QColorDialog.getColor(QColor(self.selected_color), self)
        if color.isValid():
            self.selected_color = color.name()
            self.update_color_button()
    
    def update_color_button(self):
        """Actualiza el botón de color"""
        self.color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.selected_color};
                color: white;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
            }}
        """)
    
    def add_category(self):
        """Agrega una nueva categoría"""
        name = self.name_input.text().strip()
        description = self.desc_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Error", "El nombre de la categoría es obligatorio")
            return
        
        try:
            self.db_manager.create_category(name, description, self.selected_color)
            self.load_categories()
            self.clear_form()
            QMessageBox.information(self, "Éxito", "Categoría creada correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear la categoría: {str(e)}")
    
    def edit_category(self):
        """Edita la categoría seleccionada"""
        selected_items = self.categories_list.selectedItems()
        if not selected_items:
            return
        
        category = selected_items[0].data(Qt.ItemDataRole.UserRole)
        
        # Por simplicidad, solo permitimos cambiar la descripción y color
        # El nombre requeriría más validaciones
        QMessageBox.information(self, "Información", 
                               "La edición de categorías estará disponible en una futura versión")
    
    def delete_category(self):
        """Elimina la categoría seleccionada"""
        selected_items = self.categories_list.selectedItems()
        if not selected_items:
            return
        
        category = selected_items[0].data(Qt.ItemDataRole.UserRole)
        
        # Verificar si la categoría tiene artículos
        articles = self.db_manager.get_articles(category['id'])
        if articles:
            QMessageBox.warning(self, "No se puede eliminar", 
                               f"La categoría '{category['name']}' tiene {len(articles)} artículos asociados.\n"
                               "Elimine o reasigne los artículos primero.")
            return
        
        reply = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Estás seguro de que quieres eliminar la categoría '{category['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Nota: Necesitaríamos implementar delete_category en DatabaseManager
                QMessageBox.information(self, "Información", 
                                       "La eliminación de categorías estará disponible en una futura versión")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar la categoría: {str(e)}")
    
    def clear_form(self):
        """Limpia el formulario"""
        self.name_input.clear()
        self.desc_input.clear()
        self.selected_color = "#3498db"
        self.update_color_button()
        self.categories_list.clearSelection()