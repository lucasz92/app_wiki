"""
Gestor de exportación para WikiApp
"""

import os
import json
import zipfile
from datetime import datetime
from typing import List, Dict, Optional
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtGui import QTextDocument, QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

class ExportWorker(QThread):
    progress_updated = pyqtSignal(int)
    export_finished = pyqtSignal(bool, str)
    
    def __init__(self, db_manager, export_type, file_path, articles=None):
        super().__init__()
        self.db_manager = db_manager
        self.export_type = export_type
        self.file_path = file_path
        self.articles = articles or []
    
    def run(self):
        try:
            if self.export_type == "html":
                self.export_to_html()
            elif self.export_type == "pdf":
                self.export_to_pdf()
            elif self.export_type == "markdown":
                self.export_to_markdown()
            elif self.export_type == "json":
                self.export_to_json()
            elif self.export_type == "backup":
                self.create_backup()
            
            self.export_finished.emit(True, "Exportación completada exitosamente")
        except Exception as e:
            self.export_finished.emit(False, f"Error durante la exportación: {str(e)}")
    
    def export_to_html(self):
        """Exporta artículos a HTML"""
        if not self.articles:
            self.articles = self.db_manager.get_articles()
        
        html_content = self.generate_html_content()
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.progress_updated.emit(100)
    
    def export_to_pdf(self):
        """Exporta artículos a PDF"""
        if WEASYPRINT_AVAILABLE:
            self.export_to_pdf_weasyprint()
        else:
            self.export_to_pdf_qt()
    
    def export_to_pdf_weasyprint(self):
        """Exporta a PDF usando WeasyPrint"""
        html_content = self.generate_html_content()
        weasyprint.HTML(string=html_content).write_pdf(self.file_path)
        self.progress_updated.emit(100)
    
    def export_to_pdf_qt(self):
        """Exporta a PDF usando Qt (fallback)"""
        html_content = self.generate_html_content()
        
        document = QTextDocument()
        document.setHtml(html_content)
        
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(self.file_path)
        printer.setPageSize(QPrinter.PageSize.A4)
        
        document.print(printer)
        self.progress_updated.emit(100)
    
    def export_to_markdown(self):
        """Exporta artículos a archivos Markdown"""
        if not self.articles:
            self.articles = self.db_manager.get_articles()
        
        # Crear directorio si no existe
        os.makedirs(self.file_path, exist_ok=True)
        
        total = len(self.articles)
        for i, article in enumerate(self.articles):
            # Crear nombre de archivo seguro
            safe_title = "".join(c for c in article['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_title}.md"
            filepath = os.path.join(self.file_path, filename)
            
            # Generar contenido markdown
            content = self.generate_markdown_content(article)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            progress = int((i + 1) / total * 100)
            self.progress_updated.emit(progress)
    
    def export_to_json(self):
        """Exporta artículos a JSON"""
        if not self.articles:
            self.articles = self.db_manager.get_articles()
        
        categories = self.db_manager.get_categories()
        
        export_data = {
            "export_date": datetime.now().isoformat(),
            "version": "1.0",
            "categories": categories,
            "articles": self.articles
        }
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        self.progress_updated.emit(100)
    
    def create_backup(self):
        """Crea un backup completo de la aplicación"""
        with zipfile.ZipFile(self.file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Backup de la base de datos
            if os.path.exists("wiki.db"):
                zipf.write("wiki.db", "wiki.db")
            
            # Backup de configuración
            if os.path.exists("config"):
                for root, dirs, files in os.walk("config"):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, ".")
                        zipf.write(file_path, arcname)
            
            # Backup de estilos
            if os.path.exists("styles"):
                for root, dirs, files in os.walk("styles"):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, ".")
                        zipf.write(file_path, arcname)
            
            # Exportar datos como JSON
            articles = self.db_manager.get_articles()
            categories = self.db_manager.get_categories()
            
            backup_data = {
                "backup_date": datetime.now().isoformat(),
                "version": "1.0",
                "categories": categories,
                "articles": articles
            }
            
            zipf.writestr("backup_data.json", json.dumps(backup_data, indent=2, ensure_ascii=False))
        
        self.progress_updated.emit(100)
    
    def generate_html_content(self) -> str:
        """Genera contenido HTML para exportación"""
        if not self.articles:
            self.articles = self.db_manager.get_articles()
        
        html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>WikiApp - Documentación Exportada</title>
            <style>
                body {
                    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #fff;
                }
                .header {
                    text-align: center;
                    border-bottom: 2px solid #10a37f;
                    padding-bottom: 20px;
                    margin-bottom: 40px;
                }
                .article {
                    margin-bottom: 60px;
                    padding: 30px;
                    border: 1px solid #e5e5e5;
                    border-radius: 12px;
                    background-color: #fafafa;
                }
                .article-title {
                    color: #2c3e50;
                    font-size: 2em;
                    margin-bottom: 10px;
                    border-bottom: 2px solid #10a37f;
                    padding-bottom: 10px;
                }
                .article-meta {
                    color: #7f8c8d;
                    font-size: 0.9em;
                    margin-bottom: 20px;
                }
                .article-content {
                    font-size: 1.1em;
                    line-height: 1.7;
                }
                .category-badge {
                    display: inline-block;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.8em;
                    font-weight: bold;
                    color: white;
                    margin-right: 10px;
                }
                .toc {
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 40px;
                }
                .toc h2 {
                    margin-top: 0;
                    color: #2c3e50;
                }
                .toc ul {
                    list-style-type: none;
                    padding-left: 0;
                }
                .toc li {
                    margin-bottom: 8px;
                }
                .toc a {
                    color: #10a37f;
                    text-decoration: none;
                }
                .toc a:hover {
                    text-decoration: underline;
                }
                pre {
                    background-color: #f4f4f4;
                    padding: 15px;
                    border-radius: 8px;
                    overflow-x: auto;
                }
                code {
                    background-color: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-family: 'Consolas', 'Monaco', monospace;
                }
                blockquote {
                    border-left: 4px solid #10a37f;
                    margin: 20px 0;
                    padding-left: 20px;
                    color: #7f8c8d;
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📚 WikiApp - Documentación</h1>
                <p>Exportado el {export_date}</p>
            </div>
            
            <div class="toc">
                <h2>📋 Índice de Contenidos</h2>
                <ul>
        """.format(export_date=datetime.now().strftime("%d/%m/%Y %H:%M"))
        
        # Generar índice
        for article in self.articles:
            safe_id = "".join(c for c in article['title'] if c.isalnum() or c in ('-', '_'))
            html += f'<li><a href="#{safe_id}">{article["title"]}</a></li>\n'
        
        html += """
                </ul>
            </div>
        """
        
        # Generar artículos
        for article in self.articles:
            safe_id = "".join(c for c in article['title'] if c.isalnum() or c in ('-', '_'))
            
            category_color = article.get('category_color', '#10a37f')
            category_name = article.get('category_name', 'Sin categoría')
            
            html += f"""
            <div class="article" id="{safe_id}">
                <h1 class="article-title">{article['title']}</h1>
                <div class="article-meta">
                    <span class="category-badge" style="background-color: {category_color};">
                        {category_name}
                    </span>
                    Creado: {article.get('created_at', 'N/A')} | 
                    Actualizado: {article.get('updated_at', 'N/A')}
                    {f" | Tags: {article['tags']}" if article.get('tags') else ""}
                </div>
                <div class="article-content">
                    {self.markdown_to_html(article['content'])}
                </div>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def generate_markdown_content(self, article: Dict) -> str:
        """Genera contenido Markdown para un artículo"""
        content = f"# {article['title']}\n\n"
        
        # Metadatos
        content += "---\n"
        content += f"Categoría: {article.get('category_name', 'Sin categoría')}\n"
        content += f"Creado: {article.get('created_at', 'N/A')}\n"
        content += f"Actualizado: {article.get('updated_at', 'N/A')}\n"
        if article.get('tags'):
            content += f"Tags: {article['tags']}\n"
        content += "---\n\n"
        
        # Contenido
        content += article['content']
        
        return content
    
    def markdown_to_html(self, markdown: str) -> str:
        """Convierte Markdown básico a HTML"""
        # Implementación básica - se puede mejorar con una librería como markdown
        html = markdown
        
        # Títulos
        html = html.replace('\n### ', '\n<h3>').replace('\n## ', '\n<h2>').replace('\n# ', '\n<h1>')
        
        # Negrita y cursiva
        html = html.replace('**', '<strong>').replace('**', '</strong>')
        html = html.replace('*', '<em>').replace('*', '</em>')
        
        # Código
        html = html.replace('`', '<code>').replace('`', '</code>')
        
        # Párrafos
        paragraphs = html.split('\n\n')
        html_paragraphs = []
        for para in paragraphs:
            if para.strip():
                if not para.startswith('<'):
                    para = f'<p>{para}</p>'
                html_paragraphs.append(para)
        
        return '\n'.join(html_paragraphs)


class ExportManager(QObject):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.parent_widget = parent
    
    def export_to_html(self, articles: Optional[List[Dict]] = None):
        """Exporta artículos a HTML"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent_widget,
            "Exportar a HTML",
            f"wiki_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            "Archivos HTML (*.html)"
        )
        
        if file_path:
            self.start_export("html", file_path, articles)
    
    def export_to_pdf(self, articles: Optional[List[Dict]] = None):
        """Exporta artículos a PDF"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent_widget,
            "Exportar a PDF",
            f"wiki_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "Archivos PDF (*.pdf)"
        )
        
        if file_path:
            self.start_export("pdf", file_path, articles)
    
    def export_to_markdown(self, articles: Optional[List[Dict]] = None):
        """Exporta artículos a archivos Markdown"""
        dir_path = QFileDialog.getExistingDirectory(
            self.parent_widget,
            "Seleccionar directorio para exportar Markdown"
        )
        
        if dir_path:
            export_dir = os.path.join(dir_path, f"wiki_markdown_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            self.start_export("markdown", export_dir, articles)
    
    def export_to_json(self, articles: Optional[List[Dict]] = None):
        """Exporta artículos a JSON"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent_widget,
            "Exportar a JSON",
            f"wiki_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "Archivos JSON (*.json)"
        )
        
        if file_path:
            self.start_export("json", file_path, articles)
    
    def create_backup(self):
        """Crea un backup completo"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent_widget,
            "Crear Backup",
            f"wiki_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            "Archivos ZIP (*.zip)"
        )
        
        if file_path:
            self.start_export("backup", file_path)
    
    def start_export(self, export_type: str, file_path: str, articles: Optional[List[Dict]] = None):
        """Inicia el proceso de exportación"""
        # Crear diálogo de progreso
        progress_dialog = QProgressDialog(
            f"Exportando...",
            "Cancelar",
            0, 100,
            self.parent_widget
        )
        progress_dialog.setWindowTitle("Exportación en progreso")
        progress_dialog.setModal(True)
        progress_dialog.show()
        
        # Crear worker thread
        self.export_worker = ExportWorker(self.db_manager, export_type, file_path, articles)
        
        # Conectar señales
        self.export_worker.progress_updated.connect(progress_dialog.setValue)
        self.export_worker.export_finished.connect(
            lambda success, message: self.on_export_finished(success, message, progress_dialog)
        )
        
        # Conectar cancelación
        progress_dialog.canceled.connect(self.export_worker.terminate)
        
        # Iniciar exportación
        self.export_worker.start()
    
    def on_export_finished(self, success: bool, message: str, progress_dialog: QProgressDialog):
        """Maneja la finalización de la exportación"""
        progress_dialog.close()
        
        if success:
            QMessageBox.information(self.parent_widget, "Exportación Exitosa", message)
        else:
            QMessageBox.critical(self.parent_widget, "Error de Exportación", message)