"""
Renderizador de Markdown usando QTextBrowser
"""

from PyQt6.QtWidgets import QTextBrowser
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import re

class MarkdownRenderer(QTextBrowser):
    def __init__(self):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setFont(QFont("Segoe UI", 11))
        self._current_markdown = ""
        
    def render_markdown(self, markdown_text: str):
        """Convierte Markdown a HTML y lo muestra"""
        html = self.markdown_to_html(markdown_text)
        self.setHtml(html)
    
    def update_content(self):
        """Re-renderiza el contenido actual"""
        if hasattr(self, '_current_markdown') and self._current_markdown:
            self.render_markdown(self._current_markdown)
    
    def markdown_to_html(self, markdown: str) -> str:
        """Convierte Markdown básico a HTML"""
        self._current_markdown = markdown
        html = markdown
        
        # Escapar HTML existente
        html = html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Títulos
        html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Negrita y cursiva
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Código inline
        html = re.sub(r'`(.*?)`', r'<code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">\1</code>', html)
        
        # Bloques de código
        html = re.sub(r'```(.*?)```', r'<pre style="background-color: #f8f8f8; padding: 10px; border-radius: 5px; border-left: 4px solid #ddd;"><code>\1</code></pre>', html, flags=re.DOTALL)
        
        # Enlaces
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
        
        # Listas
        lines = html.split('\n')
        in_list = False
        result_lines = []
        
        for line in lines:
            if re.match(r'^\s*[-*+]\s+', line):
                if not in_list:
                    result_lines.append('<ul>')
                    in_list = True
                item_text = re.sub(r'^\s*[-*+]\s+', '', line)
                result_lines.append(f'<li>{item_text}</li>')
            else:
                if in_list:
                    result_lines.append('</ul>')
                    in_list = False
                result_lines.append(line)
        
        if in_list:
            result_lines.append('</ul>')
        
        html = '\n'.join(result_lines)
        
        # Párrafos
        paragraphs = html.split('\n\n')
        html_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                # No envolver en <p> si ya es un elemento HTML
                if not (para.startswith('<') and para.endswith('>')):
                    # Reemplazar saltos de línea simples con <br>
                    para = para.replace('\n', '<br>')
                    para = f'<p>{para}</p>'
                html_paragraphs.append(para)
        
        html = '\n'.join(html_paragraphs)
        
        # Usar solo tema claro
        css = self.get_light_theme_css()
        
        return f"{css}<body>{html}</body>"
    
    def get_dark_theme_css(self) -> str:
        """Estilos CSS para tema oscuro"""
        return """
        <style>
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.7;
            color: #ececec;
            max-width: 100%;
            margin: 0;
            padding: 24px;
            background-color: #212121;
        }
        h1 {
            color: #ececec;
            font-weight: 600;
            font-size: 2em;
            margin: 1.5em 0 0.5em 0;
            border-bottom: none;
        }
        h2 {
            color: #ececec;
            font-weight: 600;
            font-size: 1.5em;
            margin: 1.3em 0 0.5em 0;
            border-bottom: none;
        }
        h3 {
            color: #ececec;
            font-weight: 600;
            font-size: 1.25em;
            margin: 1.2em 0 0.5em 0;
        }
        p {
            margin: 1em 0;
            color: #ececec;
        }
        code {
            font-family: 'JetBrains Mono', 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
            background-color: #2d2d2d;
            color: #10a37f;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }
        pre {
            font-family: 'JetBrains Mono', 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
            background-color: #171717;
            border: 1px solid #2d2d2d;
            border-radius: 8px;
            padding: 16px;
            overflow-x: auto;
            margin: 1.5em 0;
        }
        pre code {
            background-color: transparent;
            color: #ececec;
            padding: 0;
        }
        ul, ol {
            padding-left: 24px;
            margin: 1em 0;
        }
        li {
            margin-bottom: 8px;
            color: #ececec;
        }
        a {
            color: #10a37f;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        blockquote {
            border-left: 4px solid #10a37f;
            margin: 1.5em 0;
            padding-left: 20px;
            color: #8e8ea0;
            font-style: italic;
            background-color: #171717;
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
        }
        strong {
            color: #ececec;
            font-weight: 600;
        }
        em {
            color: #ececec;
            font-style: italic;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            background-color: #171717;
            border-radius: 8px;
            overflow: hidden;
        }
        th, td {
            border: 1px solid #2d2d2d;
            padding: 12px;
            text-align: left;
            color: #ececec;
        }
        th {
            background-color: #2d2d2d;
            font-weight: 600;
        }
        hr {
            border: none;
            height: 1px;
            background-color: #2d2d2d;
            margin: 2em 0;
        }
        </style>
        """
    
    def get_light_theme_css(self) -> str:
        """Estilos CSS para tema claro"""
        return """
        <style>
        body {
            font-family: 'Google Sans', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 2.0;
            color: #202124;
            max-width: 100%;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            font-size: 18px;
            font-weight: 400;
        }
        h1 {
            color: #202124;
            font-weight: 400;
            font-size: 2.8em;
            margin: 1.5em 0 1em 0;
            border-bottom: none;
            padding-bottom: 0;
            line-height: 1.2;
        }
        h2 {
            color: #202124;
            font-weight: 400;
            font-size: 2em;
            margin: 1.4em 0 0.6em 0;
            border-bottom: none;
            padding-bottom: 0;
            line-height: 1.3;
        }
        h3 {
            color: #5f6368;
            font-weight: 500;
            font-size: 1.5em;
            margin: 1.6em 0 0.6em 0;
            line-height: 1.4;
        }
        p {
            margin: 1.2em 0;
            color: #202124;
            font-size: 18px;
            line-height: 1.8;
        }
        code {
            font-family: 'Roboto Mono', 'JetBrains Mono', 'SF Mono', monospace;
            background-color: #f8f9fa;
            color: #1a73e8;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
            border: 1px solid #f1f3f4;
        }
        pre {
            font-family: 'Roboto Mono', 'JetBrains Mono', 'SF Mono', monospace;
            background-color: #f8f9fa;
            border: 1px solid #f1f3f4;
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            margin: 2em 0;
            line-height: 1.6;
        }
        pre code {
            background-color: transparent;
            color: #1a1a1a;
            padding: 0;
        }
        ul, ol {
            padding-left: 28px;
            margin: 1.2em 0;
        }
        li {
            margin-bottom: 8px;
            color: #202124;
            line-height: 1.7;
        }
        a {
            color: #10a37f;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        blockquote {
            border-left: 4px solid #1a73e8;
            margin: 2em 0;
            padding-left: 24px;
            color: #5f6368;
            font-style: italic;
            background-color: #f8f9fa;
            padding: 20px 24px;
            border-radius: 0 8px 8px 0;
            font-size: 1.1em;
        }
        strong {
            color: #1a1a1a;
            font-weight: 600;
        }
        em {
            color: #1a1a1a;
            font-style: italic;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        }
        th, td {
            border: 1px solid #e5e7eb;
            padding: 12px;
            text-align: left;
            color: #1a1a1a;
        }
        th {
            background-color: #f3f4f6;
            font-weight: 600;
        }
        hr {
            border: none;
            height: 1px;
            background-color: #e5e7eb;
            margin: 2em 0;
        }
        </style>
        """