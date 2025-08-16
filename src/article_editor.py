"""
Editor de artículos con soporte para Markdown
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
                            QTextEdit, QComboBox, QPushButton, QLabel, 
                            QSplitter, QTabWidget, QWidget, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .markdown_renderer import MarkdownRenderer
from .version_manager import VersionManager

class ArticleEditor(QDialog):
    def __init__(self, db_manager, article=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.article = article
        self.version_manager = VersionManager(db_manager)
        
        self.setWindowTitle("Editor de Artículos" if not article else f"Editar: {article['title']}")
        self.setGeometry(150, 100, 1200, 800)  # Ventana más grande
        
        self.setup_ui()
        
        if article:
            self.load_article_data()
    
    def setup_ui(self):
        """Configura la interfaz del editor"""
        layout = QVBoxLayout(self)
        
        # Campos del artículo
        form_layout = QVBoxLayout()
        
        # Título
        form_layout.addWidget(QLabel("Título:"))
        self.title_input = QLineEdit()
        form_layout.addWidget(self.title_input)
        
        # Categoría y tags en la misma fila
        row_layout = QHBoxLayout()
        
        # Categoría
        row_layout.addWidget(QLabel("Categoría:"))
        self.category_combo = QComboBox()
        self.load_categories()
        row_layout.addWidget(self.category_combo)
        
        # Tags
        row_layout.addWidget(QLabel("Tags:"))
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Separar con comas")
        row_layout.addWidget(self.tags_input)
        
        form_layout.addLayout(row_layout)
        layout.addLayout(form_layout)
        
        # Editor con vista previa (más espacio)
        self.setup_editor_tabs()
        layout.addWidget(self.editor_tabs, 1)  # Stretch factor para dar más espacio
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Guardar")
        self.save_btn.clicked.connect(self.save_article)
        buttons_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(buttons_layout)
    
    def setup_editor_tabs(self):
        """Configura las pestañas del editor"""
        self.editor_tabs = QTabWidget()
        
        # Pestaña de edición
        edit_widget = QWidget()
        edit_layout = QVBoxLayout(edit_widget)
        
        # Toolbar de markdown mejorado
        toolbar_layout = QHBoxLayout()
        
        # Botones de formato con mejor diseño
        bold_btn = QPushButton("𝐁 Negrita")
        bold_btn.setToolTip("Negrita (Ctrl+B)")
        bold_btn.clicked.connect(lambda: self.insert_markdown("**", "**"))
        toolbar_layout.addWidget(bold_btn)
        
        italic_btn = QPushButton("𝐼 Cursiva")
        italic_btn.setToolTip("Cursiva (Ctrl+I)")
        italic_btn.clicked.connect(lambda: self.insert_markdown("*", "*"))
        toolbar_layout.addWidget(italic_btn)
        
        code_btn = QPushButton("</> Código")
        code_btn.setToolTip("Código inline")
        code_btn.clicked.connect(lambda: self.insert_markdown("`", "`"))
        toolbar_layout.addWidget(code_btn)
        
        toolbar_layout.addWidget(QLabel("|"))  # Separador
        
        h1_btn = QPushButton("H1")
        h1_btn.setToolTip("Título Principal")
        h1_btn.clicked.connect(lambda: self.insert_markdown("# ", ""))
        toolbar_layout.addWidget(h1_btn)
        
        h2_btn = QPushButton("H2")
        h2_btn.setToolTip("Subtítulo")
        h2_btn.clicked.connect(lambda: self.insert_markdown("## ", ""))
        toolbar_layout.addWidget(h2_btn)
        
        h3_btn = QPushButton("H3")
        h3_btn.setToolTip("Subtítulo menor")
        h3_btn.clicked.connect(lambda: self.insert_markdown("### ", ""))
        toolbar_layout.addWidget(h3_btn)
        
        toolbar_layout.addWidget(QLabel("|"))  # Separador
        
        list_btn = QPushButton("• Lista")
        list_btn.setToolTip("Lista con viñetas")
        list_btn.clicked.connect(lambda: self.insert_markdown("- ", ""))
        toolbar_layout.addWidget(list_btn)
        
        numbered_list_btn = QPushButton("1. Lista")
        numbered_list_btn.setToolTip("Lista numerada")
        numbered_list_btn.clicked.connect(lambda: self.insert_markdown("1. ", ""))
        toolbar_layout.addWidget(numbered_list_btn)
        
        toolbar_layout.addWidget(QLabel("|"))  # Separador
        
        link_btn = QPushButton("🔗 Enlace")
        link_btn.setToolTip("Insertar enlace")
        link_btn.clicked.connect(lambda: self.insert_markdown("[texto del enlace](", ")"))
        toolbar_layout.addWidget(link_btn)
        
        quote_btn = QPushButton("❝ Cita")
        quote_btn.setToolTip("Bloque de cita")
        quote_btn.clicked.connect(lambda: self.insert_markdown("> ", ""))
        toolbar_layout.addWidget(quote_btn)
        
        table_btn = QPushButton("⊞ Tabla")
        table_btn.setToolTip("Insertar tabla")
        table_btn.clicked.connect(self.insert_table)
        toolbar_layout.addWidget(table_btn)
        
        toolbar_layout.addStretch()
        edit_layout.addLayout(toolbar_layout)
        
        # Editor de texto (área principal más grande)
        self.content_editor = QTextEdit()
        self.content_editor.setObjectName("content_editor")
        self.content_editor.setFont(QFont("JetBrains Mono", 14))
        self.content_editor.setPlaceholderText("Comienza a escribir tu artículo aquí usando Markdown...\n\n# Título Principal\n\nEscribe tu contenido aquí. Usa **negrita**, *cursiva*, `código`, etc.")
        self.content_editor.textChanged.connect(self.update_preview)
        self.content_editor.setMinimumHeight(450)  # Altura mínima más grande
        edit_layout.addWidget(self.content_editor, 1)  # Stretch factor
        
        self.editor_tabs.addTab(edit_widget, "📝 Editar")
        
        # Pestaña de vista previa
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        
        self.preview_renderer = MarkdownRenderer()
        preview_layout.addWidget(self.preview_renderer)
        
        self.editor_tabs.addTab(preview_widget, "👁️ Vista Previa")
        
        # Hacer que el editor sea la pestaña por defecto y más prominente
        self.editor_tabs.setCurrentIndex(0)
    
    def load_categories(self):
        """Carga las categorías en el combo"""
        categories = self.db_manager.get_categories()
        for category in categories:
            self.category_combo.addItem(category['name'], category['id'])
    
    def load_article_data(self):
        """Carga los datos del artículo en el editor"""
        if not self.article:
            return
        
        self.title_input.setText(self.article['title'])
        self.content_editor.setPlainText(self.article['content'])
        self.tags_input.setText(self.article.get('tags', ''))
        
        # Seleccionar categoría
        for i in range(self.category_combo.count()):
            if self.category_combo.itemData(i) == self.article['category_id']:
                self.category_combo.setCurrentIndex(i)
                break
        
        self.update_preview()
    
    def insert_markdown(self, prefix: str, suffix: str):
        """Inserta formato markdown en el editor"""
        cursor = self.content_editor.textCursor()
        selected_text = cursor.selectedText()
        
        if selected_text:
            new_text = f"{prefix}{selected_text}{suffix}"
            cursor.insertText(new_text)
        else:
            cursor.insertText(f"{prefix}{suffix}")
            # Mover cursor entre prefix y suffix
            if suffix:
                cursor.movePosition(cursor.MoveOperation.Left, cursor.MoveMode.MoveAnchor, len(suffix))
                self.content_editor.setTextCursor(cursor)
    
    def update_preview(self):
        """Actualiza la vista previa del markdown"""
        content = self.content_editor.toPlainText()
        self.preview_renderer.render_markdown(content)
    
    def save_article(self):
        """Guarda el artículo"""
        title = self.title_input.text().strip()
        content = self.content_editor.toPlainText()
        category_id = self.category_combo.currentData()
        tags = self.tags_input.text().strip()
        
        if not title:
            QMessageBox.warning(self, "Error", "El título es obligatorio")
            return
        
        if not content:
            QMessageBox.warning(self, "Error", "El contenido es obligatorio")
            return
        
        if not category_id:
            QMessageBox.warning(self, "Error", "Debe seleccionar una categoría")
            return
        
        try:
            if self.article:
                # Crear versión antes de actualizar
                change_description = f"Actualización del artículo"
                self.version_manager.create_version(
                    self.article['id'],
                    self.article['title'],
                    self.article['content'],
                    self.article['category_id'],
                    self.article.get('tags', ''),
                    change_description
                )
                
                # Actualizar artículo existente
                self.db_manager.update_article(
                    self.article['id'], title, content, category_id, tags
                )
            else:
                # Crear nuevo artículo
                article_id = self.db_manager.create_article(title, content, category_id, tags)
                
                # Crear primera versión
                self.version_manager.create_version(
                    article_id, title, content, category_id, tags, "Versión inicial"
                )
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar el artículo: {str(e)}")
    
    def insert_table(self):
        """Inserta una tabla básica"""
        table_template = """| Columna 1 | Columna 2 | Columna 3 |
|-----------|-----------|-----------|
| Dato 1    | Dato 2    | Dato 3    |
| Dato 4    | Dato 5    | Dato 6    |"""
        
        cursor = self.content_editor.textCursor()
        cursor.insertText(table_template)