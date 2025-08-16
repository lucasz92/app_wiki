"""
Visor de artículos con renderizado de Markdown
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .markdown_renderer import MarkdownRenderer

class ArticleViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del visor"""
        layout = QVBoxLayout(self)
        
        # Área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget contenedor
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # Header del artículo
        self.title_label = QLabel()
        self.title_label.setObjectName("articleTitle")
        self.title_label.setWordWrap(True)
        self.content_layout.addWidget(self.title_label)
        
        self.meta_label = QLabel()
        self.meta_label.setObjectName("articleMeta")
        self.content_layout.addWidget(self.meta_label)
        
        # Renderizador de markdown
        self.markdown_renderer = MarkdownRenderer()
        self.content_layout.addWidget(self.markdown_renderer)
        
        self.content_layout.addStretch()
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
        
        # Mostrar mensaje inicial
        self.show_welcome_message()
    
    def display_article(self, article):
        """Muestra un artículo"""
        self.title_label.setText(article['title'])
        
        # Información meta
        meta_info = []
        if article.get('category_name'):
            meta_info.append(f"📁 {article['category_name']}")
        
        if article.get('tags'):
            tags = [tag.strip() for tag in article['tags'].split(',') if tag.strip()]
            if tags:
                meta_info.append(f"🏷️ {', '.join(tags)}")
        
        if article.get('updated_at'):
            meta_info.append(f"📅 Actualizado: {article['updated_at']}")
        
        self.meta_label.setText(" | ".join(meta_info))
        
        # Renderizar contenido markdown
        self.markdown_renderer.render_markdown(article['content'])
    
    def clear(self):
        """Limpia el visor"""
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Muestra mensaje de bienvenida"""
        self.title_label.setText("📚 Bienvenido a WikiApp")
        self.meta_label.setText("Selecciona un artículo de la lista para comenzar")
        
        welcome_content = """
# Bienvenido a WikiApp

Tu plataforma de documentación empresarial diseñada para crear, organizar y compartir conocimiento de manera eficiente.

## Características principales

**Crear y editar** - Escribe documentos usando Markdown con vista previa en tiempo real

**Organizar** - Categoriza tu contenido por temas: Seguridad, Procesos, Tutoriales, 5S

**Buscar** - Encuentra información rápidamente en títulos, contenido y etiquetas

**Colaborar** - Comparte conocimiento con tu equipo de manera estructurada

## Cómo empezar

Haz clic en **Nuevo Artículo** para crear tu primer documento, o explora los artículos de ejemplo en el panel lateral.

## Sintaxis Markdown

```markdown
# Título principal
## Subtítulo

**Negrita** y *cursiva*
`código inline`

- Lista de elementos
- Otro elemento

[Enlaces](https://ejemplo.com)
```

> Comienza a documentar el conocimiento de tu organización
        """
        
        self.markdown_renderer.render_markdown(welcome_content)
    
    def refresh_content(self):
        """Actualiza el contenido del viewer"""
        if hasattr(self, 'markdown_renderer'):
            self.markdown_renderer.update_content()