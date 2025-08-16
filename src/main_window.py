"""
Ventana principal de WikiApp
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QSplitter, QPushButton, QLineEdit, QComboBox, 
                            QListWidget, QListWidgetItem, QLabel, QMessageBox,
                            QToolBar, QStatusBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QFont

from .database import DatabaseManager
from .article_editor import ArticleEditor
from .article_viewer import ArticleViewer
from .category_manager import CategoryManager

from .export_manager import ExportManager
from .template_manager import TemplateManager
from .version_manager import VersionManager, VersionHistoryDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_article_id = None
        
        self.setWindowTitle("WikiApp - Documentación Empresarial")
        self.setGeometry(100, 50, 1400, 1000)  # Ventana mucho más alta
        
        # Inicializar gestores
        self.export_manager = ExportManager(self.db_manager, self)
        self.version_manager = VersionManager(self.db_manager)
        
        # Cargar estilos (solo tema claro)
        self.load_styles()
        
        # Configurar UI
        self.setup_ui()
        self.setup_toolbar()
        self.setup_statusbar()
        self.setup_menubar()
        
        # Cargar datos iniciales
        self.load_categories()
        self.load_articles()
    
    def load_styles(self):
        """Carga los estilos QSS"""
        try:
            with open("styles/main.qss", "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo de estilos no encontrado, usando estilos por defecto")
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panel izquierdo (navegación)
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Panel derecho (contenido)
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Configurar proporciones del splitter (panel izquierdo mínimo, contenido máximo)
        splitter.setSizes([160, 1240])
    
    def create_left_panel(self) -> QWidget:
        """Crea el panel de navegación izquierdo"""
        panel = QWidget()
        panel.setObjectName("leftPanel")
        layout = QVBoxLayout(panel)
        
        # Título
        title = QLabel("📚 Documentación")
        title.setObjectName("panelTitle")
        layout.addWidget(title)
        
        # Barra de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar artículos...")
        self.search_input.textChanged.connect(self.filter_articles)
        layout.addWidget(self.search_input)
        
        # Filtro por categoría
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Categoría:"))
        
        self.category_filter = QComboBox()
        self.category_filter.currentTextChanged.connect(self.filter_articles)
        category_layout.addWidget(self.category_filter)
        
        layout.addLayout(category_layout)
        
        # Lista de artículos
        self.articles_list = QListWidget()
        self.articles_list.itemClicked.connect(self.on_article_selected)
        layout.addWidget(self.articles_list)
        
        # Botones de acción
        buttons_layout = QVBoxLayout()
        
        self.new_article_btn = QPushButton("Nuevo Artículo")
        self.new_article_btn.setObjectName("sidebarButton")
        self.new_article_btn.clicked.connect(self.new_article)
        buttons_layout.addWidget(self.new_article_btn)
        
        self.edit_article_btn = QPushButton("Editar")
        self.edit_article_btn.setObjectName("sidebarButton")
        self.edit_article_btn.clicked.connect(self.edit_article)
        self.edit_article_btn.setEnabled(False)
        buttons_layout.addWidget(self.edit_article_btn)
        
        self.delete_article_btn = QPushButton("Eliminar")
        self.delete_article_btn.setObjectName("sidebarButton")
        self.delete_article_btn.clicked.connect(self.delete_article)
        self.delete_article_btn.setEnabled(False)
        buttons_layout.addWidget(self.delete_article_btn)
        
        self.history_btn = QPushButton("Historial")
        self.history_btn.setObjectName("sidebarButton")
        self.history_btn.clicked.connect(self.show_version_history)
        self.history_btn.setEnabled(False)
        buttons_layout.addWidget(self.history_btn)
        
        layout.addLayout(buttons_layout)
        
        return panel
    
    def create_right_panel(self) -> QWidget:
        """Crea el panel de contenido derecho"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Viewer de artículos
        self.article_viewer = ArticleViewer()
        layout.addWidget(self.article_viewer)
        
        return panel
    
    def setup_toolbar(self):
        """Configura la barra de herramientas"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Plantillas
        templates_action = QAction("📄 Plantillas", self)
        templates_action.triggered.connect(self.manage_templates)
        toolbar.addAction(templates_action)
        
        toolbar.addSeparator()
        
        # Acción nueva categoría
        new_category_action = QAction("📁 Categorías", self)
        new_category_action.triggered.connect(self.manage_categories)
        toolbar.addAction(new_category_action)
        
        toolbar.addSeparator()
        
        # Backup
        backup_action = QAction("💾 Backup", self)
        backup_action.triggered.connect(self.create_backup)
        toolbar.addAction(backup_action)
    
    def setup_statusbar(self):
        """Configura la barra de estado"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Listo")
    
    def load_categories(self):
        """Carga las categorías en el filtro"""
        self.category_filter.clear()
        self.category_filter.addItem("Todas las categorías", None)
        
        categories = self.db_manager.get_categories()
        for category in categories:
            self.category_filter.addItem(category['name'], category['id'])
    
    def load_articles(self):
        """Carga los artículos en la lista"""
        search_term = self.search_input.text()
        category_id = self.category_filter.currentData()
        
        articles = self.db_manager.get_articles(category_id, search_term)
        
        self.articles_list.clear()
        
        # Agregar artículo de bienvenida como primera opción
        welcome_item = QListWidgetItem("🏠 Página de Inicio")
        welcome_item.setData(Qt.ItemDataRole.UserRole, "welcome")
        welcome_item.setToolTip("Página de bienvenida con información sobre WikiApp")
        self.articles_list.addItem(welcome_item)
        
        # Agregar artículos reales
        for article in articles:
            item = QListWidgetItem(f"📄 {article['title']}")
            item.setData(Qt.ItemDataRole.UserRole, article['id'])
            
            # Agregar información de categoría
            if article['category_name']:
                item.setToolTip(f"Categoría: {article['category_name']}\nÚltima actualización: {article['updated_at']}")
            
            self.articles_list.addItem(item)
        
        # Seleccionar la página de inicio por defecto si no hay búsqueda
        if not search_term and not category_id:
            self.articles_list.setCurrentRow(0)
            self.show_welcome_page()
        
        total_articles = len(articles)
        self.statusbar.showMessage(f"{total_articles} artículos encontrados")
    
    def filter_articles(self):
        """Filtra los artículos según búsqueda y categoría"""
        self.load_articles()
    
    def on_article_selected(self, item):
        """Maneja la selección de un artículo"""
        article_id = item.data(Qt.ItemDataRole.UserRole)
        
        if article_id == "welcome":
            # Mostrar página de bienvenida
            self.show_welcome_page()
            self.current_article_id = None
            self.edit_article_btn.setEnabled(False)
            self.delete_article_btn.setEnabled(False)
            self.history_btn.setEnabled(False)
        else:
            # Mostrar artículo normal
            self.current_article_id = article_id
            article = self.db_manager.get_article(article_id)
            if article:
                self.article_viewer.display_article(article)
                self.edit_article_btn.setEnabled(True)
                self.delete_article_btn.setEnabled(True)
                self.history_btn.setEnabled(True)
    
    def show_welcome_page(self):
        """Muestra la página de bienvenida"""
        self.article_viewer.show_welcome_message()
    
    def new_article(self):
        """Abre el editor para crear un nuevo artículo"""
        editor = ArticleEditor(self.db_manager, parent=self)
        if editor.exec() == editor.DialogCode.Accepted:
            self.load_articles()
    
    def edit_article(self):
        """Edita el artículo seleccionado"""
        if not self.current_article_id:
            return
        
        article = self.db_manager.get_article(self.current_article_id)
        if article:
            editor = ArticleEditor(self.db_manager, article, parent=self)
            if editor.exec() == editor.DialogCode.Accepted:
                self.load_articles()
                # Recargar el artículo en el viewer
                updated_article = self.db_manager.get_article(self.current_article_id)
                if updated_article:
                    self.article_viewer.display_article(updated_article)
    
    def delete_article(self):
        """Elimina el artículo seleccionado"""
        if not self.current_article_id:
            return
        
        reply = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este artículo?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_article(self.current_article_id)
            self.load_articles()
            self.article_viewer.clear()
            self.current_article_id = None
            self.edit_article_btn.setEnabled(False)
            self.delete_article_btn.setEnabled(False)
            self.history_btn.setEnabled(False)
    
    def manage_categories(self):
        """Abre el gestor de categorías"""
        manager = CategoryManager(self.db_manager, parent=self)
        if manager.exec() == manager.DialogCode.Accepted:
            self.load_categories()
    
    def setup_menubar(self):
        """Configura la barra de menú"""
        menubar = self.menuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu("📁 Archivo")
        
        new_action = QAction("📝 Nuevo Artículo", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_article)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction("💾 Crear Backup", self)
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("❌ Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menú Exportar
        export_menu = menubar.addMenu("📤 Exportar")
        
        export_html_action = QAction("🌐 Exportar a HTML", self)
        export_html_action.triggered.connect(self.export_to_html)
        export_menu.addAction(export_html_action)
        
        export_pdf_action = QAction("📄 Exportar a PDF", self)
        export_pdf_action.triggered.connect(self.export_to_pdf)
        export_menu.addAction(export_pdf_action)
        
        export_md_action = QAction("📝 Exportar a Markdown", self)
        export_md_action.triggered.connect(self.export_to_markdown)
        export_menu.addAction(export_md_action)
        
        export_json_action = QAction("📊 Exportar a JSON", self)
        export_json_action.triggered.connect(self.export_to_json)
        export_menu.addAction(export_json_action)
        
        # Menú Herramientas
        tools_menu = menubar.addMenu("🔧 Herramientas")
        
        templates_action = QAction("📄 Gestionar Plantillas", self)
        templates_action.triggered.connect(self.manage_templates)
        tools_menu.addAction(templates_action)
        
        categories_action = QAction("📁 Gestionar Categorías", self)
        categories_action.triggered.connect(self.manage_categories)
        tools_menu.addAction(categories_action)
        

        
        # Menú Ayuda
        help_menu = menubar.addMenu("❓ Ayuda")
        
        about_action = QAction("ℹ️ Acerca de", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    

    
    def manage_templates(self):
        """Abre el gestor de plantillas"""
        manager = TemplateManager(self.db_manager, parent=self)
        manager.exec()
    
    def create_backup(self):
        """Crea un backup completo"""
        self.export_manager.create_backup()
    
    def export_to_html(self):
        """Exporta a HTML"""
        self.export_manager.export_to_html()
    
    def export_to_pdf(self):
        """Exporta a PDF"""
        self.export_manager.export_to_pdf()
    
    def export_to_markdown(self):
        """Exporta a Markdown"""
        self.export_manager.export_to_markdown()
    
    def export_to_json(self):
        """Exporta a JSON"""
        self.export_manager.export_to_json()
    
    def show_version_history(self):
        """Muestra el historial de versiones del artículo actual"""
        if not self.current_article_id:
            return
        
        dialog = VersionHistoryDialog(self.db_manager, self.current_article_id, self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            # Recargar el artículo si se restauró una versión
            self.load_articles()
            updated_article = self.db_manager.get_article(self.current_article_id)
            if updated_article:
                self.article_viewer.display_article(updated_article)
    
    def show_about(self):
        """Muestra información sobre la aplicación"""
        about_text = """
        <h2>📚 WikiApp</h2>
        <p><b>Versión:</b> 2.0</p>
        <p><b>Descripción:</b> Aplicación de documentación empresarial con soporte completo para Markdown</p>
        
        <h3>✨ Características:</h3>
        <ul>
            <li>📝 Editor Markdown con vista previa</li>
            <li>📁 Categorización avanzada</li>
            <li>🔍 Búsqueda en tiempo real</li>
            <li>📄 Sistema de plantillas</li>
            <li>📚 Historial de versiones</li>
            <li>🌙 Modo oscuro/claro</li>
            <li>📤 Exportación múltiple (HTML, PDF, Markdown, JSON)</li>
            <li>💾 Sistema de backup</li>
        </ul>
        
        <p><b>Desarrollado con:</b> Python, PyQt6, SQLite</p>
        <p><b>Estilo:</b> Inspirado en ChatGPT</p>
        """
        
        QMessageBox.about(self, "Acerca de WikiApp", about_text)