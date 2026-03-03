# WikiApp - Aplicación de Documentación Empresarial

Una aplicación de escritorio estilo wiki desarrollada en Python con PyQt6 y SQLite para gestionar documentación empresarial de manera organizada y eficiente. Diseño inspirado en ChatGPT con funcionalidades avanzadas.

## 🚀 Características Principales
[!IMPORTANT]
asdasd

### 📝 Editor Avanzado
- **Editor Markdown** con sintaxis highlighting y vista previa en tiempo real
- **Toolbar de formato** con botones para negrita, cursiva, títulos, listas, enlaces y código
- **Plantillas predefinidas** para diferentes tipos de documentos
- **Auto-guardado** y gestión de versiones

### 📁 Organización Inteligente
- **Categorización avanzada** con colores personalizables
- **Sistema de etiquetas** para clasificación cruzada
- **Búsqueda en tiempo real** en títulos, contenido y etiquetas
- **Filtros por categoría** para navegación rápida

### 🎨 Interfaz Moderna
- **Diseño estilo ChatGPT** con tema oscuro y claro
- **Interfaz responsive** y fácil de usar
- **Estilos QSS modulares** completamente personalizables
- **Iconos intuitivos** y navegación fluida

### 📚 Gestión de Contenido
- **Historial de versiones** completo con comparación y restauración
- **Sistema de plantillas** para documentos estándar
- **Backup automático** y manual
- **Importación/Exportación** múltiple

### 📤 Exportación Avanzada
- **HTML** con estilos profesionales
- **PDF** de alta calidad (con WeasyPrint)
- **Markdown** para compatibilidad
- **JSON** para intercambio de datos
- **Backup completo** en ZIP

## 📋 Requisitos

- Python 3.8 o superior
- PyQt6
- SQLite (incluido con Python)

## 🛠️ Instalación

1. Clona o descarga el proyecto
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
python main.py
```

## 📁 Estructura del Proyecto

```
WikiApp/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias de Python
├── README.md              # Este archivo
├── wiki.db                # Base de datos SQLite (se crea automáticamente)
├── src/                   # Código fuente
│   ├── __init__.py
│   ├── database.py        # Gestor de base de datos SQLite
│   ├── main_window.py     # Ventana principal con menús
│   ├── article_editor.py  # Editor Markdown avanzado
│   ├── article_viewer.py  # Visor con renderizado HTML
│   ├── markdown_renderer.py # Renderizador con temas
│   ├── category_manager.py # Gestor de categorías
│   ├── theme_manager.py   # Gestor de temas oscuro/claro
│   ├── export_manager.py  # Exportación múltiple
│   ├── template_manager.py # Sistema de plantillas
│   └── version_manager.py # Historial de versiones
├── styles/                # Estilos QSS
│   └── main.qss          # Estilos estilo ChatGPT
├── config/                # Configuración
│   ├── theme_config.json # Configuración de tema
│   ├── templates.json    # Plantillas personalizadas
│   └── versions.json     # Historial de versiones
└── run.bat               # Ejecutor para Windows
```

## 🎯 Uso

### 📝 Crear un Nuevo Artículo
1. **Desde cero**: Haz clic en "📝 Nuevo Artículo" o usa `Ctrl+N`
2. **Desde plantilla**: Ve a "📄 Plantillas" y selecciona una plantilla predefinida
3. Completa el título y selecciona una categoría
4. Escribe el contenido usando la **toolbar de Markdown**
5. Agrega etiquetas separadas por comas
6. Usa la pestaña "👁️ Vista Previa" para ver el resultado
7. Guarda con `Ctrl+S`

### 📁 Gestionar Categorías
1. Ve a "🔧 Herramientas" → "📁 Gestionar Categorías"
2. Agrega nuevas categorías con nombre, descripción y **color personalizado**
3. Las categorías se muestran con códigos de color en toda la aplicación

### 🔍 Buscar y Filtrar
- **Búsqueda en tiempo real**: Escribe en la barra de búsqueda
- **Filtro por categoría**: Usa el menú desplegable
- **Búsqueda avanzada**: Busca en títulos, contenido y etiquetas simultáneamente

### 📄 Usar Plantillas
1. Ve a "📄 Plantillas" en la toolbar
2. Selecciona entre plantillas predefinidas:
   - **Procedimiento 5S**
   - **Tutorial Paso a Paso**
   - **Procedimiento de Seguridad**
   - **Proceso Organizacional**
3. Personaliza el contenido según tus necesidades
4. Crea tus propias plantillas personalizadas

### 📚 Historial de Versiones
1. Selecciona un artículo
2. Haz clic en "📚 Historial"
3. Ve todas las versiones anteriores
4. **Compara versiones** para ver cambios
5. **Restaura versiones** anteriores si es necesario

### 🌙 Cambiar Tema
- Haz clic en "🌙 Cambiar Tema" en la toolbar
- Alterna entre **modo oscuro** (estilo ChatGPT) y **modo claro**
- El tema se guarda automáticamente

### 📤 Exportar Documentación
Ve al menú "📤 Exportar" y selecciona:
- **🌐 HTML**: Página web completa con estilos
- **📄 PDF**: Documento profesional (requiere WeasyPrint)
- **📝 Markdown**: Archivos .md individuales
- **📊 JSON**: Datos estructurados para intercambio

### 💾 Backup y Restauración
- **Backup manual**: "📁 Archivo" → "💾 Crear Backup"
- **Backup automático**: Se crea un ZIP con base de datos, configuración y estilos
- **Restauración**: Descomprime el ZIP en el directorio de la aplicación

## 📝 Sintaxis Markdown Soportada

WikiApp soporta Markdown completo con renderizado HTML profesional:

### Texto y Formato
```markdown
# Título Principal
## Subtítulo  
### Subtítulo Menor

**Texto en negrita**
*Texto en cursiva*
`código inline`
~~Texto tachado~~

> Cita o blockquote
> Múltiples líneas
```

### Listas y Tablas
```markdown
- Lista no ordenada
- Otro elemento
  - Sub-elemento

1. Lista ordenada
2. Segundo elemento

| Columna 1 | Columna 2 | Columna 3 |
|-----------|-----------|-----------|
| Dato 1    | Dato 2    | Dato 3    |
| Dato 4    | Dato 5    | Dato 6    |
```

### Código y Enlaces
```markdown
```python
def hello_world():
    print("¡Hola WikiApp!")
```

[Enlace simple](https://ejemplo.com)
[Enlace con título](https://ejemplo.com "Título del enlace")
```

### Elementos Avanzados
```markdown
---
Línea horizontal

- [ ] Tarea pendiente
- [x] Tarea completada

![Imagen](ruta/imagen.png "Descripción")
```

## 🎨 Personalización

Los estilos de la aplicación están definidos en `styles/main.qss`. Puedes modificar:
- Colores de la interfaz
- Fuentes y tamaños
- Espaciado y márgenes
- Efectos hover y focus

## 🗄️ Base de Datos

La aplicación utiliza SQLite con las siguientes tablas:

- **categories**: Almacena las categorías con nombre, descripción y color
- **articles**: Almacena los artículos con título, contenido, categoría y etiquetas

## ✅ Funcionalidades Implementadas

- [x] **Exportación completa** (PDF, HTML, Markdown, JSON)
- [x] **Importación** desde archivos Markdown
- [x] **Historial de versiones** con restauración
- [x] **Búsqueda de texto completo** en tiempo real
- [x] **Sistema de plantillas** predefinidas y personalizables
- [x] **Backup automático y manual**
- [x] **Modo oscuro/claro** con cambio dinámico
- [x] **Gestión avanzada de categorías**

## 🔧 Funcionalidades Futuras

- [ ] Sincronización en la nube
- [ ] Colaboración en tiempo real
- [ ] Plugins y extensiones
- [ ] API REST
- [ ] Aplicación móvil complementaria
- [ ] Integración con sistemas externos
- [ ] OCR para imágenes
- [ ] Diagramas integrados

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 🆘 Soporte

Si encuentras algún problema o tienes sugerencias:
1. Revisa los issues existentes
2. Crea un nuevo issue con detalles del problema
3. Incluye información del sistema y pasos para reproducir

## 🎯 Casos de Uso Empresarial

### 🏭 Manufactura y Producción
- **Procedimientos 5S** con plantillas predefinidas
- **Manuales de seguridad** con categorización por riesgo
- **Instructivos de trabajo** paso a paso
- **Documentación de procesos** con diagramas

### 🏢 Oficinas y Administración
- **Políticas corporativas** organizadas por departamento
- **Tutoriales de software** con capturas de pantalla
- **Procedimientos administrativos** con flujos de trabajo
- **Base de conocimiento** para soporte técnico

### 🎓 Capacitación y Desarrollo
- **Materiales de entrenamiento** con plantillas educativas
- **Evaluaciones y certificaciones** documentadas
- **Historial de capacitaciones** con versiones
- **Recursos de aprendizaje** categorizados por nivel

## 🔧 Instalación Avanzada

### Instalación Completa con PDF
```bash
# Instalar dependencias básicas
pip install -r requirements.txt

# Para exportación PDF mejorada (opcional)
pip install weasyprint

# En Windows, puede requerir:
# - Microsoft Visual C++ Build Tools
# - GTK+ runtime
```

### Instalación Mínima
```bash
# Solo funcionalidades básicas
pip install PyQt6 python-dateutil
```

## 🚀 Desarrollo y Contribución

### Estructura del Código
- **Patrón MVC**: Separación clara entre modelo, vista y controlador
- **Gestores especializados**: Cada funcionalidad tiene su propio gestor
- **Configuración modular**: Archivos JSON para configuración
- **Estilos separados**: QSS para personalización visual

### Agregar Nuevas Funcionalidades
1. Crea un nuevo gestor en `src/`
2. Integra con `main_window.py`
3. Actualiza los estilos en `styles/main.qss`
4. Documenta en el README

### Testing
```bash
# Ejecutar pruebas básicas
python -m pytest tests/

# Verificar funcionalidad completa
python main.py
```

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~3,000+
- **Archivos Python**: 10 módulos principales
- **Funcionalidades**: 15+ características principales
- **Plantillas incluidas**: 4 plantillas profesionales
- **Formatos de exportación**: 4 formatos diferentes
- **Temas**: 2 temas completos (oscuro/claro)

---

**🚀 WikiApp v2.0 - Desarrollado con ❤️ para revolucionar la gestión de documentación empresarial**

*Inspirado en la elegancia de ChatGPT y la funcionalidad de las mejores herramientas de documentación*
