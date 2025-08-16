"""
Gestor de versiones para WikiApp
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                            QPushButton, QLabel, QTextEdit, QMessageBox, 
                            QListWidgetItem, QSplitter, QTableWidget, 
                            QTableWidgetItem, QHeaderView, QWidget)
from PyQt6.QtCore import Qt

class VersionManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.versions_file = "config/versions.json"
        self.load_versions()
    
    def load_versions(self):
        """Carga el historial de versiones"""
        try:
            if os.path.exists(self.versions_file):
                with open(self.versions_file, 'r', encoding='utf-8') as f:
                    self.versions = json.load(f)
            else:
                self.versions = {}
        except Exception as e:
            print(f"Error cargando versiones: {e}")
            self.versions = {}
    
    def save_versions(self):
        """Guarda el historial de versiones"""
        try:
            os.makedirs(os.path.dirname(self.versions_file), exist_ok=True)
            with open(self.versions_file, 'w', encoding='utf-8') as f:
                json.dump(self.versions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando versiones: {e}")
    
    def create_version(self, article_id: int, title: str, content: str, 
                      category_id: int, tags: str, change_description: str = ""):
        """Crea una nueva versión de un artículo"""
        article_key = str(article_id)
        
        if article_key not in self.versions:
            self.versions[article_key] = []
        
        version = {
            'version_number': len(self.versions[article_key]) + 1,
            'timestamp': datetime.now().isoformat(),
            'title': title,
            'content': content,
            'category_id': category_id,
            'tags': tags,
            'change_description': change_description,
            'content_hash': hash(content)  # Para detectar cambios reales
        }
        
        # Solo guardar si el contenido realmente cambió
        if not self.versions[article_key] or \
           self.versions[article_key][-1]['content_hash'] != version['content_hash']:
            self.versions[article_key].append(version)
            self.save_versions()
            return True
        
        return False
    
    def get_versions(self, article_id: int) -> List[Dict]:
        """Obtiene todas las versiones de un artículo"""
        article_key = str(article_id)
        return self.versions.get(article_key, [])
    
    def get_version(self, article_id: int, version_number: int) -> Optional[Dict]:
        """Obtiene una versión específica de un artículo"""
        versions = self.get_versions(article_id)
        for version in versions:
            if version['version_number'] == version_number:
                return version
        return None
    
    def restore_version(self, article_id: int, version_number: int) -> bool:
        """Restaura una versión específica de un artículo"""
        version = self.get_version(article_id, version_number)
        if not version:
            return False
        
        try:
            # Actualizar el artículo en la base de datos
            self.db_manager.update_article(
                article_id,
                version['title'],
                version['content'],
                version['category_id'],
                version['tags']
            )
            
            # Crear una nueva versión marcando la restauración
            self.create_version(
                article_id,
                version['title'],
                version['content'],
                version['category_id'],
                version['tags'],
                f"Restaurado desde versión {version_number}"
            )
            
            return True
        except Exception as e:
            print(f"Error restaurando versión: {e}")
            return False
    
    def delete_versions(self, article_id: int):
        """Elimina todas las versiones de un artículo"""
        article_key = str(article_id)
        if article_key in self.versions:
            del self.versions[article_key]
            self.save_versions()
    
    def compare_versions(self, article_id: int, version1: int, version2: int) -> Dict:
        """Compara dos versiones de un artículo"""
        v1 = self.get_version(article_id, version1)
        v2 = self.get_version(article_id, version2)
        
        if not v1 or not v2:
            return {}
        
        return {
            'version1': v1,
            'version2': v2,
            'title_changed': v1['title'] != v2['title'],
            'content_changed': v1['content'] != v2['content'],
            'category_changed': v1['category_id'] != v2['category_id'],
            'tags_changed': v1['tags'] != v2['tags']
        }


class VersionHistoryDialog(QDialog):
    def __init__(self, db_manager, article_id, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.article_id = article_id
        self.version_manager = VersionManager(db_manager)
        
        # Obtener información del artículo
        self.article = db_manager.get_article(article_id)
        if not self.article:
            QMessageBox.critical(self, "Error", "Artículo no encontrado")
            self.reject()
            return
        
        self.setWindowTitle(f"Historial de Versiones - {self.article['title']}")
        self.setGeometry(200, 200, 1000, 700)
        
        self.setup_ui()
        self.load_versions()
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel(f"📚 Historial de Versiones: {self.article['title']}")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)
        
        # Splitter principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Panel izquierdo - Lista de versiones
        left_panel = self.create_versions_panel()
        splitter.addWidget(left_panel)
        
        # Panel derecho - Contenido de la versión
        right_panel = self.create_content_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([400, 600])
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        self.restore_btn = QPushButton("🔄 Restaurar Versión")
        self.restore_btn.clicked.connect(self.restore_version)
        self.restore_btn.setEnabled(False)
        buttons_layout.addWidget(self.restore_btn)
        
        self.compare_btn = QPushButton("🔍 Comparar")
        self.compare_btn.clicked.connect(self.compare_versions)
        self.compare_btn.setEnabled(False)
        buttons_layout.addWidget(self.compare_btn)
        
        buttons_layout.addStretch()
        
        self.close_btn = QPushButton("Cerrar")
        self.close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(self.close_btn)
        
        layout.addLayout(buttons_layout)
    
    def create_versions_panel(self):
        """Crea el panel de versiones"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("📋 Versiones:"))
        
        # Tabla de versiones
        self.versions_table = QTableWidget()
        self.versions_table.setColumnCount(4)
        self.versions_table.setHorizontalHeaderLabels([
            "Versión", "Fecha", "Cambios", "Descripción"
        ])
        
        # Configurar tabla
        header = self.versions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        self.versions_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.versions_table.itemSelectionChanged.connect(self.on_version_selected)
        
        layout.addWidget(self.versions_table)
        
        return widget
    
    def create_content_panel(self):
        """Crea el panel de contenido"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Información de la versión
        self.version_info = QLabel("Selecciona una versión para ver su contenido")
        layout.addWidget(self.version_info)
        
        # Contenido de la versión
        self.version_content = QTextEdit()
        self.version_content.setReadOnly(True)
        layout.addWidget(self.version_content)
        
        return widget
    
    def load_versions(self):
        """Carga las versiones en la tabla"""
        versions = self.version_manager.get_versions(self.article_id)
        
        # Agregar versión actual como primera fila
        current_version = {
            'version_number': 'Actual',
            'timestamp': self.article.get('updated_at', ''),
            'title': self.article['title'],
            'content': self.article['content'],
            'category_id': self.article['category_id'],
            'tags': self.article.get('tags', ''),
            'change_description': 'Versión actual'
        }
        
        all_versions = [current_version] + sorted(versions, key=lambda x: x['version_number'], reverse=True)
        
        self.versions_table.setRowCount(len(all_versions))
        
        for row, version in enumerate(all_versions):
            # Número de versión
            version_item = QTableWidgetItem(str(version['version_number']))
            version_item.setData(Qt.ItemDataRole.UserRole, version)
            self.versions_table.setItem(row, 0, version_item)
            
            # Fecha
            timestamp = version['timestamp']
            if timestamp:
                try:
                    if 'T' in timestamp:  # ISO format
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        formatted_date = dt.strftime("%d/%m/%Y %H:%M")
                    else:
                        formatted_date = timestamp
                except:
                    formatted_date = timestamp
            else:
                formatted_date = "N/A"
            
            self.versions_table.setItem(row, 1, QTableWidgetItem(formatted_date))
            
            # Indicador de cambios
            changes = []
            if row < len(all_versions) - 1:  # No comparar la última versión
                next_version = all_versions[row + 1]
                if version['title'] != next_version['title']:
                    changes.append("Título")
                if version['content'] != next_version['content']:
                    changes.append("Contenido")
                if version['category_id'] != next_version['category_id']:
                    changes.append("Categoría")
                if version['tags'] != next_version['tags']:
                    changes.append("Tags")
            
            changes_text = ", ".join(changes) if changes else "N/A"
            self.versions_table.setItem(row, 2, QTableWidgetItem(changes_text))
            
            # Descripción
            description = version.get('change_description', '')
            self.versions_table.setItem(row, 3, QTableWidgetItem(description))
        
        # Seleccionar la primera fila (versión actual)
        if all_versions:
            self.versions_table.selectRow(0)
    
    def on_version_selected(self):
        """Maneja la selección de una versión"""
        selected_rows = self.versions_table.selectionModel().selectedRows()
        if not selected_rows:
            self.restore_btn.setEnabled(False)
            self.compare_btn.setEnabled(False)
            return
        
        row = selected_rows[0].row()
        version_item = self.versions_table.item(row, 0)
        version = version_item.data(Qt.ItemDataRole.UserRole)
        
        # Mostrar información de la versión
        version_num = version['version_number']
        timestamp = version['timestamp']
        
        if timestamp:
            try:
                if 'T' in timestamp:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_date = dt.strftime("%d/%m/%Y a las %H:%M")
                else:
                    formatted_date = timestamp
            except:
                formatted_date = timestamp
        else:
            formatted_date = "Fecha desconocida"
        
        info_text = f"📄 Versión {version_num} - {formatted_date}"
        if version.get('change_description'):
            info_text += f"\n📝 {version['change_description']}"
        
        self.version_info.setText(info_text)
        
        # Mostrar contenido
        content = f"# {version['title']}\n\n"
        if version.get('tags'):
            content += f"**Tags:** {version['tags']}\n\n"
        content += version['content']
        
        self.version_content.setPlainText(content)
        
        # Habilitar botones (excepto para versión actual)
        is_current = version_num == 'Actual'
        self.restore_btn.setEnabled(not is_current)
        self.compare_btn.setEnabled(True)
    
    def restore_version(self):
        """Restaura la versión seleccionada"""
        selected_rows = self.versions_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        version_item = self.versions_table.item(row, 0)
        version = version_item.data(Qt.ItemDataRole.UserRole)
        
        version_num = version['version_number']
        
        reply = QMessageBox.question(
            self, "Confirmar Restauración",
            f"¿Estás seguro de que quieres restaurar la versión {version_num}?\n\n"
            "Esto sobrescribirá la versión actual del artículo.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.version_manager.restore_version(self.article_id, version_num)
            
            if success:
                QMessageBox.information(
                    self, "Restauración Exitosa",
                    f"La versión {version_num} ha sido restaurada correctamente."
                )
                self.accept()  # Cerrar el diálogo
            else:
                QMessageBox.critical(
                    self, "Error",
                    "No se pudo restaurar la versión seleccionada."
                )
    
    def compare_versions(self):
        """Compara versiones (funcionalidad básica)"""
        selected_rows = self.versions_table.selectionModel().selectedRows()
        if len(selected_rows) != 1:
            QMessageBox.information(
                self, "Comparar Versiones",
                "Selecciona una versión para compararla con la actual."
            )
            return
        
        row = selected_rows[0].row()
        version_item = self.versions_table.item(row, 0)
        version = version_item.data(Qt.ItemDataRole.UserRole)
        
        # Comparar con la versión actual
        current_version = self.versions_table.item(0, 0).data(Qt.ItemDataRole.UserRole)
        
        comparison = []
        
        if version['title'] != current_version['title']:
            comparison.append(f"**Título:**\n- Anterior: {version['title']}\n- Actual: {current_version['title']}\n")
        
        if version['content'] != current_version['content']:
            comparison.append("**Contenido:** Ha cambiado\n")
        
        if version['tags'] != current_version['tags']:
            comparison.append(f"**Tags:**\n- Anterior: {version['tags']}\n- Actual: {current_version['tags']}\n")
        
        if not comparison:
            comparison.append("No hay diferencias detectadas.")
        
        comparison_text = "\n".join(comparison)
        
        QMessageBox.information(
            self, f"Comparación - Versión {version['version_number']} vs Actual",
            comparison_text
        )