"""
Gestor de plantillas para WikiApp
"""

import json
import os
from typing import Dict, List, Optional
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                            QPushButton, QLineEdit, QLabel, QTextEdit, 
                            QMessageBox, QListWidgetItem, QInputDialog,
                            QComboBox, QSplitter, QWidget)
from PyQt6.QtCore import Qt

class TemplateManager(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.templates_file = "config/templates.json"
        
        self.setWindowTitle("Gestor de Plantillas")
        self.setGeometry(200, 200, 800, 600)
        
        self.setup_ui()
        self.load_templates()
        self.load_default_templates()
    
    def setup_ui(self):
        """Configura la interfaz del gestor"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("📄 Gestión de Plantillas")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)
        
        # Splitter principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Panel izquierdo - Lista de plantillas
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Panel derecho - Editor de plantillas
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([300, 500])
        
        # Botones del diálogo
        buttons_layout = QHBoxLayout()
        
        self.close_btn = QPushButton("Cerrar")
        self.close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(self.close_btn)
        
        layout.addLayout(buttons_layout)
    
    def create_left_panel(self):
        """Crea el panel izquierdo con la lista de plantillas"""
        panel = QVBoxLayout()
        
        # Lista de plantillas
        self.templates_list = QListWidget()
        self.templates_list.itemClicked.connect(self.on_template_selected)
        panel.addWidget(self.templates_list)
        
        # Botones de gestión
        buttons_layout = QVBoxLayout()
        
        self.new_template_btn = QPushButton("➕ Nueva Plantilla")
        self.new_template_btn.clicked.connect(self.new_template)
        buttons_layout.addWidget(self.new_template_btn)
        
        self.edit_template_btn = QPushButton("✏️ Editar")
        self.edit_template_btn.clicked.connect(self.edit_template)
        self.edit_template_btn.setEnabled(False)
        buttons_layout.addWidget(self.edit_template_btn)
        
        self.delete_template_btn = QPushButton("🗑️ Eliminar")
        self.delete_template_btn.clicked.connect(self.delete_template)
        self.delete_template_btn.setEnabled(False)
        buttons_layout.addWidget(self.delete_template_btn)
        
        self.use_template_btn = QPushButton("📝 Usar Plantilla")
        self.use_template_btn.clicked.connect(self.use_template)
        self.use_template_btn.setEnabled(False)
        buttons_layout.addWidget(self.use_template_btn)
        
        panel.addLayout(buttons_layout)
        
        widget = QWidget()
        widget.setLayout(panel)
        return widget
    
    def create_right_panel(self):
        """Crea el panel derecho con el editor de plantillas"""
        panel = QVBoxLayout()
        
        # Información de la plantilla
        info_layout = QVBoxLayout()
        
        # Nombre
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nombre:"))
        self.template_name = QLineEdit()
        name_layout.addWidget(self.template_name)
        info_layout.addLayout(name_layout)
        
        # Descripción
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Descripción:"))
        self.template_description = QLineEdit()
        desc_layout.addWidget(self.template_description)
        info_layout.addLayout(desc_layout)
        
        # Categoría sugerida
        cat_layout = QHBoxLayout()
        cat_layout.addWidget(QLabel("Categoría:"))
        self.template_category = QComboBox()
        self.load_categories()
        cat_layout.addWidget(self.template_category)
        info_layout.addLayout(cat_layout)
        
        panel.addLayout(info_layout)
        
        # Editor de contenido
        panel.addWidget(QLabel("Contenido de la plantilla:"))
        self.template_content = QTextEdit()
        self.template_content.setPlaceholderText("Escribe aquí el contenido de la plantilla usando Markdown...")
        panel.addWidget(self.template_content)
        
        # Botones de acción
        action_buttons = QHBoxLayout()
        
        self.save_template_btn = QPushButton("💾 Guardar Plantilla")
        self.save_template_btn.clicked.connect(self.save_template)
        action_buttons.addWidget(self.save_template_btn)
        
        self.clear_form_btn = QPushButton("🗑️ Limpiar")
        self.clear_form_btn.clicked.connect(self.clear_form)
        action_buttons.addWidget(self.clear_form_btn)
        
        panel.addLayout(action_buttons)
        
        widget = QWidget()
        widget.setLayout(panel)
        return widget
    
    def load_categories(self):
        """Carga las categorías en el combo"""
        self.template_category.clear()
        self.template_category.addItem("Sin categoría específica", None)
        
        categories = self.db_manager.get_categories()
        for category in categories:
            self.template_category.addItem(category['name'], category['id'])
    
    def load_templates(self):
        """Carga las plantillas desde el archivo"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    self.templates = json.load(f)
            else:
                self.templates = {}
        except Exception as e:
            print(f"Error cargando plantillas: {e}")
            self.templates = {}
        
        self.refresh_templates_list()
    
    def save_templates(self):
        """Guarda las plantillas al archivo"""
        try:
            os.makedirs(os.path.dirname(self.templates_file), exist_ok=True)
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error guardando plantillas: {str(e)}")
    
    def load_default_templates(self):
        """Carga plantillas por defecto si no existen"""
        if not self.templates:
            default_templates = {
                "procedimiento_5s": {
                    "name": "Procedimiento 5S",
                    "description": "Plantilla para documentar procedimientos de metodología 5S",
                    "category_name": "Metodología 5S",
                    "content": """# Procedimiento 5S: [Nombre del Procedimiento]

## 📋 Información General
- **Área/Departamento:** [Especificar área]
- **Responsable:** [Nombre del responsable]
- **Fecha de creación:** [Fecha]
- **Versión:** 1.0

## 🎯 Objetivo
[Describir el objetivo del procedimiento]

## 📖 Definiciones
- **Seiri (Clasificar):** [Definición específica para este procedimiento]
- **Seiton (Ordenar):** [Definición específica para este procedimiento]
- **Seiso (Limpiar):** [Definición específica para este procedimiento]
- **Seiketsu (Estandarizar):** [Definición específica para este procedimiento]
- **Shitsuke (Disciplina):** [Definición específica para este procedimiento]

## 🔄 Procedimiento

### 1️⃣ Seiri (Clasificar)
- [ ] [Paso específico]
- [ ] [Paso específico]
- [ ] [Paso específico]

### 2️⃣ Seiton (Ordenar)
- [ ] [Paso específico]
- [ ] [Paso específico]
- [ ] [Paso específico]

### 3️⃣ Seiso (Limpiar)
- [ ] [Paso específico]
- [ ] [Paso específico]
- [ ] [Paso específico]

### 4️⃣ Seiketsu (Estandarizar)
- [ ] [Paso específico]
- [ ] [Paso específico]
- [ ] [Paso específico]

### 5️⃣ Shitsuke (Disciplina)
- [ ] [Paso específico]
- [ ] [Paso específico]
- [ ] [Paso específico]

## 📊 Indicadores de Control
| Indicador | Meta | Frecuencia de Medición |
|-----------|------|------------------------|
| [Indicador 1] | [Meta] | [Frecuencia] |
| [Indicador 2] | [Meta] | [Frecuencia] |

## 📝 Registros
- [Registro 1]
- [Registro 2]

## 🔄 Revisión y Mejora
- **Frecuencia de revisión:** [Especificar]
- **Responsable de revisión:** [Nombre]
- **Próxima revisión:** [Fecha]
"""
                },
                "tutorial_paso_a_paso": {
                    "name": "Tutorial Paso a Paso",
                    "description": "Plantilla para crear tutoriales detallados",
                    "category_name": "Tutorial",
                    "content": """# Tutorial: [Título del Tutorial]

## 📋 Información del Tutorial
- **Nivel:** [Principiante/Intermedio/Avanzado]
- **Tiempo estimado:** [X minutos/horas]
- **Autor:** [Nombre del autor]
- **Fecha:** [Fecha de creación]

## 🎯 Objetivo
[Describir qué aprenderá el usuario al completar este tutorial]

## 📋 Prerrequisitos
- [Prerrequisito 1]
- [Prerrequisito 2]
- [Prerrequisito 3]

## 🛠️ Herramientas Necesarias
- [Herramienta 1]
- [Herramienta 2]
- [Herramienta 3]

## 📚 Pasos del Tutorial

### Paso 1: [Título del paso]
[Descripción detallada del paso]

```
[Código o comandos si aplica]
```

**Resultado esperado:** [Describir qué debería ver el usuario]

### Paso 2: [Título del paso]
[Descripción detallada del paso]

**💡 Consejo:** [Consejo útil para este paso]

### Paso 3: [Título del paso]
[Descripción detallada del paso]

**⚠️ Advertencia:** [Advertencia importante si aplica]

## ✅ Verificación
Para verificar que has completado correctamente el tutorial:
- [ ] [Criterio de verificación 1]
- [ ] [Criterio de verificación 2]
- [ ] [Criterio de verificación 3]

## 🔧 Solución de Problemas
### Problema: [Descripción del problema común]
**Solución:** [Cómo resolverlo]

### Problema: [Descripción del problema común]
**Solución:** [Cómo resolverlo]

## 📚 Recursos Adicionales
- [Enlace o recurso 1]
- [Enlace o recurso 2]
- [Enlace o recurso 3]

## 🔄 Próximos Pasos
[Sugerir qué hacer después de completar este tutorial]
"""
                },
                "procedimiento_seguridad": {
                    "name": "Procedimiento de Seguridad",
                    "description": "Plantilla para documentar procedimientos de higiene y seguridad",
                    "category_name": "Higiene y Seguridad",
                    "content": """# Procedimiento de Seguridad: [Nombre del Procedimiento]

## 📋 Información del Documento
- **Código:** [Código del procedimiento]
- **Versión:** 1.0
- **Fecha de emisión:** [Fecha]
- **Próxima revisión:** [Fecha]
- **Responsable:** [Nombre y cargo]

## 🎯 Objetivo
[Describir el objetivo del procedimiento de seguridad]

## 📖 Alcance
[Definir el alcance de aplicación del procedimiento]

## 📚 Referencias Normativas
- [Norma/Ley 1]
- [Norma/Ley 2]
- [Norma/Ley 3]

## 🔍 Definiciones
- **[Término 1]:** [Definición]
- **[Término 2]:** [Definición]
- **[Término 3]:** [Definición]

## ⚠️ Identificación de Riesgos
| Riesgo | Probabilidad | Severidad | Nivel de Riesgo |
|--------|--------------|-----------|-----------------|
| [Riesgo 1] | [Alta/Media/Baja] | [Alta/Media/Baja] | [Alto/Medio/Bajo] |
| [Riesgo 2] | [Alta/Media/Baja] | [Alta/Media/Baja] | [Alto/Medio/Bajo] |

## 🛡️ Medidas Preventivas
### Controles de Ingeniería
- [Medida 1]
- [Medida 2]
- [Medida 3]

### Controles Administrativos
- [Medida 1]
- [Medida 2]
- [Medida 3]

### Equipos de Protección Personal (EPP)
- [EPP 1] - [Especificación]
- [EPP 2] - [Especificación]
- [EPP 3] - [Especificación]

## 📋 Procedimiento Paso a Paso

### Antes de Iniciar
- [ ] [Verificación 1]
- [ ] [Verificación 2]
- [ ] [Verificación 3]

### Durante la Actividad
1. [Paso 1 con medidas de seguridad]
2. [Paso 2 con medidas de seguridad]
3. [Paso 3 con medidas de seguridad]

### Al Finalizar
- [ ] [Verificación final 1]
- [ ] [Verificación final 2]
- [ ] [Verificación final 3]

## 🚨 Procedimiento de Emergencia
### En caso de [Tipo de emergencia]
1. [Acción inmediata 1]
2. [Acción inmediata 2]
3. [Acción inmediata 3]

**Contactos de Emergencia:**
- Emergencias: 911
- [Contacto interno]: [Teléfono]
- [Contacto específico]: [Teléfono]

## 📊 Indicadores de Seguridad
| Indicador | Meta | Frecuencia |
|-----------|------|------------|
| [Indicador 1] | [Meta] | [Frecuencia] |
| [Indicador 2] | [Meta] | [Frecuencia] |

## 📝 Registros y Documentación
- [Registro 1]
- [Registro 2]
- [Registro 3]

## 👥 Responsabilidades
- **[Cargo/Rol 1]:** [Responsabilidades específicas]
- **[Cargo/Rol 2]:** [Responsabilidades específicas]
- **[Cargo/Rol 3]:** [Responsabilidades específicas]

## 📚 Capacitación Requerida
- [Capacitación 1] - [Frecuencia]
- [Capacitación 2] - [Frecuencia]
- [Capacitación 3] - [Frecuencia]
"""
                },
                "proceso_organizacional": {
                    "name": "Proceso Organizacional",
                    "description": "Plantilla para documentar procesos organizacionales",
                    "category_name": "Procesos",
                    "content": """# Proceso: [Nombre del Proceso]

## 📋 Información del Proceso
- **Código:** [Código del proceso]
- **Versión:** 1.0
- **Propietario del proceso:** [Nombre y cargo]
- **Fecha de creación:** [Fecha]
- **Última actualización:** [Fecha]

## 🎯 Propósito
[Describir el propósito y objetivo del proceso]

## 📖 Alcance
[Definir el alcance del proceso - qué incluye y qué no incluye]

## 📊 Entradas y Salidas

### Entradas (Inputs)
| Entrada | Proveedor | Criterios de Aceptación |
|---------|-----------|-------------------------|
| [Entrada 1] | [Proveedor] | [Criterios] |
| [Entrada 2] | [Proveedor] | [Criterios] |

### Salidas (Outputs)
| Salida | Cliente | Criterios de Calidad |
|--------|---------|---------------------|
| [Salida 1] | [Cliente] | [Criterios] |
| [Salida 2] | [Cliente] | [Criterios] |

## 👥 Roles y Responsabilidades
| Rol | Responsabilidades |
|-----|-------------------|
| [Rol 1] | [Responsabilidades específicas] |
| [Rol 2] | [Responsabilidades específicas] |
| [Rol 3] | [Responsabilidades específicas] |

## 🔄 Descripción del Proceso

### Fase 1: [Nombre de la fase]
**Responsable:** [Rol responsable]
**Tiempo estimado:** [Tiempo]

1. [Actividad 1]
   - [Detalle específico]
   - [Detalle específico]

2. [Actividad 2]
   - [Detalle específico]
   - [Detalle específico]

### Fase 2: [Nombre de la fase]
**Responsable:** [Rol responsable]
**Tiempo estimado:** [Tiempo]

1. [Actividad 1]
2. [Actividad 2]

### Fase 3: [Nombre de la fase]
**Responsable:** [Rol responsable]
**Tiempo estimado:** [Tiempo]

1. [Actividad 1]
2. [Actividad 2]

## 📊 Indicadores de Desempeño (KPIs)
| Indicador | Fórmula | Meta | Frecuencia de Medición |
|-----------|---------|------|------------------------|
| [KPI 1] | [Fórmula] | [Meta] | [Frecuencia] |
| [KPI 2] | [Fórmula] | [Meta] | [Frecuencia] |

## 🛠️ Recursos Necesarios
### Recursos Humanos
- [Recurso 1]
- [Recurso 2]

### Recursos Tecnológicos
- [Recurso 1]
- [Recurso 2]

### Recursos Materiales
- [Recurso 1]
- [Recurso 2]

## 📝 Documentos y Registros
- [Documento/Registro 1]
- [Documento/Registro 2]
- [Documento/Registro 3]

## 🔄 Mejora Continua
### Frecuencia de Revisión
[Especificar frecuencia]

### Criterios para Mejora
- [Criterio 1]
- [Criterio 2]
- [Criterio 3]

## 📚 Documentos Relacionados
- [Documento relacionado 1]
- [Documento relacionado 2]
- [Documento relacionado 3]

## 📞 Contactos
| Rol | Nombre | Teléfono | Email |
|-----|--------|----------|-------|
| [Rol 1] | [Nombre] | [Teléfono] | [Email] |
| [Rol 2] | [Nombre] | [Teléfono] | [Email] |
"""
                }
            }
            
            self.templates.update(default_templates)
            self.save_templates()
            self.refresh_templates_list()
    
    def refresh_templates_list(self):
        """Actualiza la lista de plantillas"""
        self.templates_list.clear()
        
        for template_id, template in self.templates.items():
            item = QListWidgetItem(f"📄 {template['name']}")
            item.setData(Qt.ItemDataRole.UserRole, template_id)
            item.setToolTip(template.get('description', 'Sin descripción'))
            self.templates_list.addItem(item)
    
    def on_template_selected(self, item):
        """Maneja la selección de una plantilla"""
        template_id = item.data(Qt.ItemDataRole.UserRole)
        template = self.templates.get(template_id, {})
        
        # Cargar datos en el formulario
        self.template_name.setText(template.get('name', ''))
        self.template_description.setText(template.get('description', ''))
        self.template_content.setPlainText(template.get('content', ''))
        
        # Seleccionar categoría
        category_name = template.get('category_name', '')
        for i in range(self.template_category.count()):
            if self.template_category.itemText(i) == category_name:
                self.template_category.setCurrentIndex(i)
                break
        
        # Habilitar botones
        self.edit_template_btn.setEnabled(True)
        self.delete_template_btn.setEnabled(True)
        self.use_template_btn.setEnabled(True)
    
    def new_template(self):
        """Crea una nueva plantilla"""
        self.clear_form()
        self.template_name.setFocus()
    
    def edit_template(self):
        """Edita la plantilla seleccionada"""
        # El formulario ya está cargado con los datos
        pass
    
    def save_template(self):
        """Guarda la plantilla actual"""
        name = self.template_name.text().strip()
        description = self.template_description.text().strip()
        content = self.template_content.toPlainText()
        category_name = self.template_category.currentText()
        
        if not name:
            QMessageBox.warning(self, "Error", "El nombre de la plantilla es obligatorio")
            return
        
        if not content:
            QMessageBox.warning(self, "Error", "El contenido de la plantilla es obligatorio")
            return
        
        # Generar ID único
        template_id = name.lower().replace(' ', '_').replace(':', '')
        
        # Crear plantilla
        template = {
            'name': name,
            'description': description,
            'content': content,
            'category_name': category_name if category_name != "Sin categoría específica" else ""
        }
        
        self.templates[template_id] = template
        self.save_templates()
        self.refresh_templates_list()
        
        QMessageBox.information(self, "Éxito", "Plantilla guardada correctamente")
    
    def delete_template(self):
        """Elimina la plantilla seleccionada"""
        selected_items = self.templates_list.selectedItems()
        if not selected_items:
            return
        
        template_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        template_name = self.templates[template_id]['name']
        
        reply = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Estás seguro de que quieres eliminar la plantilla '{template_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            del self.templates[template_id]
            self.save_templates()
            self.refresh_templates_list()
            self.clear_form()
            QMessageBox.information(self, "Éxito", "Plantilla eliminada correctamente")
    
    def use_template(self):
        """Usa la plantilla seleccionada para crear un nuevo artículo"""
        selected_items = self.templates_list.selectedItems()
        if not selected_items:
            return
        
        template_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        template = self.templates[template_id]
        
        # Cerrar el gestor de plantillas
        self.accept()
        
        # Crear nuevo artículo con la plantilla
        from .article_editor import ArticleEditor
        
        editor = ArticleEditor(self.db_manager, parent=self.parent())
        
        # Cargar contenido de la plantilla
        editor.content_editor.setPlainText(template['content'])
        
        # Seleccionar categoría si está especificada
        if template.get('category_name'):
            for i in range(editor.category_combo.count()):
                if editor.category_combo.itemText(i) == template['category_name']:
                    editor.category_combo.setCurrentIndex(i)
                    break
        
        # Mostrar el editor
        editor.exec()
    
    def clear_form(self):
        """Limpia el formulario"""
        self.template_name.clear()
        self.template_description.clear()
        self.template_content.clear()
        self.template_category.setCurrentIndex(0)
        
        # Deshabilitar botones
        self.edit_template_btn.setEnabled(False)
        self.delete_template_btn.setEnabled(False)
        self.use_template_btn.setEnabled(False)
        
        # Limpiar selección
        self.templates_list.clearSelection()
    
    def get_templates(self) -> Dict:
        """Obtiene todas las plantillas"""
        return self.templates
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """Obtiene una plantilla específica"""
        return self.templates.get(template_id)