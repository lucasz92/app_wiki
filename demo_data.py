#!/usr/bin/env python3
"""
Script para crear datos de demostración en WikiApp
"""

from src.database import DatabaseManager

def create_demo_data():
    """Crea artículos de demostración"""
    db = DatabaseManager()
    db.initialize_database()
    
    # Obtener categorías
    categories = db.get_categories()
    cat_dict = {cat['name']: cat['id'] for cat in categories}
    
    # Artículos de demostración
    demo_articles = [
        {
            'title': 'Introducción a la Metodología 5S',
            'content': '''# Introducción a la Metodología 5S

La metodología **5S** es una técnica de gestión japonesa basada en cinco principios simples que ayudan a crear y mantener un lugar de trabajo organizado, limpio, seguro y de alta calidad.

## Los 5 Principios

### 1️⃣ Seiri (Clasificar)
- Separar lo necesario de lo innecesario
- Eliminar elementos que no se utilizan
- Mantener solo lo esencial

### 2️⃣ Seiton (Ordenar)
- Un lugar para cada cosa y cada cosa en su lugar
- Organizar de manera lógica y eficiente
- Facilitar el acceso a herramientas y materiales

### 3️⃣ Seiso (Limpiar)
- Mantener el área de trabajo limpia
- Inspeccionar mientras se limpia
- Prevenir la suciedad y el desorden

### 4️⃣ Seiketsu (Estandarizar)
- Crear estándares para mantener las primeras 3S
- Desarrollar procedimientos y rutinas
- Asegurar la consistencia

### 5️⃣ Shitsuke (Disciplina)
- Mantener y mejorar los estándares
- Crear hábitos positivos
- Compromiso continuo con la mejora

## Beneficios

- ✅ Mayor productividad
- ✅ Reducción de desperdicios
- ✅ Mejor seguridad laboral
- ✅ Mayor calidad
- ✅ Ambiente de trabajo más agradable

> La metodología 5S no es solo una técnica de organización, es una filosofía de mejora continua.
''',
            'category': 'Metodología 5S',
            'tags': '5S, organización, mejora continua, productividad'
        },
        {
            'title': 'Procedimiento de Seguridad en Laboratorio',
            'content': '''# Procedimiento de Seguridad en Laboratorio

## 🎯 Objetivo
Establecer las medidas de seguridad necesarias para el trabajo en laboratorio y prevenir accidentes.

## ⚠️ Riesgos Identificados

| Riesgo | Probabilidad | Severidad | Medidas Preventivas |
|--------|--------------|-----------|-------------------|
| Exposición a químicos | Media | Alta | EPP, ventilación |
| Cortes con vidrio | Alta | Media | Manipulación cuidadosa |
| Quemaduras | Baja | Alta | Equipos de protección |

## 🛡️ Equipos de Protección Personal (EPP)

### Obligatorios
- **Bata de laboratorio** - Protección contra salpicaduras
- **Gafas de seguridad** - Protección ocular
- **Guantes** - Según el tipo de sustancia

### Opcionales según actividad
- Mascarilla respiratoria
- Zapatos de seguridad
- Protección auditiva

## 📋 Procedimiento Paso a Paso

### Antes de iniciar
1. [ ] Verificar que todos los EPP estén en buen estado
2. [ ] Revisar la hoja de seguridad de las sustancias a utilizar
3. [ ] Comprobar el funcionamiento de equipos de emergencia
4. [ ] Informar al supervisor sobre la actividad a realizar

### Durante el trabajo
1. **Mantener el área limpia** y ordenada
2. **No comer, beber o fumar** en el laboratorio
3. **Etiquetar** todos los recipientes
4. **Reportar inmediatamente** cualquier incidente

### Al finalizar
1. [ ] Limpiar y desinfectar el área de trabajo
2. [ ] Guardar correctamente los materiales
3. [ ] Disponer adecuadamente de los residuos
4. [ ] Registrar las actividades realizadas

## 🚨 En caso de emergencia

### Derrame de químicos
1. **Evacuar** el área si es necesario
2. **Contener** el derrame si es seguro hacerlo
3. **Neutralizar** según procedimiento específico
4. **Reportar** al supervisor

### Contacto con la piel
1. **Lavar inmediatamente** con abundante agua
2. **Quitar** ropa contaminada
3. **Buscar atención médica** si es necesario

## 📞 Contactos de Emergencia
- **Emergencias**: 911
- **Supervisor de laboratorio**: Ext. 1234
- **Seguridad industrial**: Ext. 5678
''',
            'category': 'Higiene y Seguridad',
            'tags': 'seguridad, laboratorio, EPP, procedimientos, emergencia'
        },
        {
            'title': 'Tutorial: Cómo usar Markdown',
            'content': '''# Tutorial: Cómo usar Markdown

**Markdown** es un lenguaje de marcado ligero que permite formatear texto de manera sencilla y legible.

## 📚 Sintaxis Básica

### Títulos
```markdown
# Título Principal (H1)
## Subtítulo (H2)
### Subtítulo menor (H3)
```

### Formato de texto
```markdown
**Texto en negrita**
*Texto en cursiva*
`código inline`
~~Texto tachado~~
```

### Listas

#### Lista con viñetas
```markdown
- Elemento 1
- Elemento 2
  - Sub-elemento
- Elemento 3
```

#### Lista numerada
```markdown
1. Primer elemento
2. Segundo elemento
3. Tercer elemento
```

### Enlaces y referencias
```markdown
[Texto del enlace](https://ejemplo.com)
[Enlace con título](https://ejemplo.com "Título del enlace")
```

### Imágenes
```markdown
![Texto alternativo](ruta/imagen.png "Título opcional")
```

### Citas
```markdown
> Esta es una cita
> Puede tener múltiples líneas
```

### Código

#### Código inline
```markdown
Usa `código` dentro del texto
```

#### Bloques de código
````markdown
```python
def hello_world():
    print("¡Hola mundo!")
```
````

### Tablas
```markdown
| Columna 1 | Columna 2 | Columna 3 |
|-----------|-----------|-----------|
| Dato 1    | Dato 2    | Dato 3    |
| Dato 4    | Dato 5    | Dato 6    |
```

### Líneas horizontales
```markdown
---
```

## ✅ Lista de tareas
```markdown
- [x] Tarea completada
- [ ] Tarea pendiente
- [ ] Otra tarea pendiente
```

## 💡 Consejos

1. **Mantén la simplicidad** - Markdown está diseñado para ser fácil de leer
2. **Usa espacios en blanco** - Ayudan a separar secciones
3. **Previsualiza tu contenido** - Siempre revisa cómo se ve el resultado final
4. **Combina elementos** - Puedes usar **negrita** dentro de listas, etc.

## 🔗 Recursos adicionales

- [Guía oficial de Markdown](https://daringfireball.net/projects/markdown/)
- [Cheat sheet de Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
- [Editor online de Markdown](https://dillinger.io/)

> **Recuerda**: La práctica hace al maestro. ¡Experimenta con diferentes elementos!
''',
            'category': 'Tutorial',
            'tags': 'markdown, tutorial, documentación, formato, sintaxis'
        },
        {
            'title': 'Proceso de Gestión de Inventario',
            'content': '''# Proceso de Gestión de Inventario

## 📋 Información del Proceso
- **Código**: PROC-INV-001
- **Versión**: 2.0
- **Propietario**: Gerencia de Operaciones
- **Última actualización**: Enero 2025

## 🎯 Propósito
Establecer un proceso sistemático para la gestión eficiente del inventario, asegurando disponibilidad de productos y optimización de costos.

## 📊 Entradas y Salidas

### Entradas (Inputs)
| Entrada | Proveedor | Criterios |
|---------|-----------|-----------|
| Órdenes de compra | Departamento de Compras | Aprobadas y autorizadas |
| Solicitudes de material | Producción | Con código de proyecto |
| Reportes de ventas | Comercial | Actualizados semanalmente |

### Salidas (Outputs)
| Salida | Cliente | Criterios de Calidad |
|--------|---------|---------------------|
| Reporte de inventario | Gerencia | Precisión >98% |
| Órdenes de reposición | Compras | Basadas en punto de reorden |
| Materiales despachados | Producción | Completos y a tiempo |

## 👥 Roles y Responsabilidades

| Rol | Responsabilidades |
|-----|-------------------|
| **Jefe de Almacén** | Supervisar operaciones, aprobar ajustes |
| **Almacenista** | Recepción, despacho, conteos físicos |
| **Analista de Inventario** | Análisis de datos, reportes, optimización |

## 🔄 Descripción del Proceso

### Fase 1: Recepción de Materiales
**Responsable**: Almacenista  
**Tiempo estimado**: 30 minutos por orden

1. **Verificar documentación**
   - Orden de compra
   - Guía de remisión
   - Factura del proveedor

2. **Inspección física**
   - Cantidad recibida
   - Estado de los productos
   - Fecha de vencimiento (si aplica)

3. **Registro en sistema**
   - Actualizar inventario
   - Generar etiquetas
   - Ubicar en almacén

### Fase 2: Control de Inventario
**Responsable**: Analista de Inventario  
**Tiempo estimado**: 2 horas diarias

1. **Monitoreo de niveles**
   - Revisar stock mínimo
   - Identificar productos de baja rotación
   - Generar alertas de reposición

2. **Análisis de demanda**
   - Proyecciones de consumo
   - Estacionalidad
   - Tendencias de mercado

### Fase 3: Despacho de Materiales
**Responsable**: Almacenista  
**Tiempo estimado**: 15 minutos por solicitud

1. **Validar solicitud**
   - Autorización correspondiente
   - Disponibilidad en stock
   - Prioridad de entrega

2. **Preparar despacho**
   - Picking de materiales
   - Verificación de cantidades
   - Empaque y etiquetado

3. **Actualizar registros**
   - Descontar del inventario
   - Registrar salida
   - Generar comprobante

## 📊 Indicadores de Desempeño (KPIs)

| Indicador | Fórmula | Meta | Frecuencia |
|-----------|---------|------|------------|
| **Precisión de Inventario** | (Conteo físico / Conteo sistema) × 100 | >98% | Mensual |
| **Rotación de Inventario** | Costo ventas / Inventario promedio | >6 veces/año | Trimestral |
| **Tiempo de Despacho** | Tiempo promedio de preparación | <30 min | Semanal |
| **Stock Out** | Productos sin stock / Total productos | <2% | Semanal |

## 🛠️ Recursos Necesarios

### Tecnológicos
- Sistema ERP
- Lectores de código de barras
- Computadoras y tablets

### Materiales
- Etiquetas y códigos
- Equipos de medición
- Materiales de empaque

## 📝 Documentos y Registros
- Órdenes de compra
- Guías de remisión
- Reportes de inventario
- Solicitudes de material
- Registros de conteo físico

## 🔄 Mejora Continua

### Revisión Mensual
- Análisis de KPIs
- Identificación de oportunidades
- Implementación de mejoras

### Auditorías Trimestrales
- Conteo físico completo
- Verificación de procedimientos
- Actualización de procesos

## 📞 Contactos Clave
| Rol | Nombre | Extensión | Email |
|-----|--------|-----------|-------|
| Jefe de Almacén | [Nombre] | 1001 | almacen@empresa.com |
| Analista de Inventario | [Nombre] | 1002 | inventario@empresa.com |
| Gerente de Operaciones | [Nombre] | 1000 | operaciones@empresa.com |
''',
            'category': 'Procesos',
            'tags': 'inventario, proceso, almacén, gestión, KPIs'
        }
    ]
    
    # Crear artículos
    for article_data in demo_articles:
        category_id = cat_dict.get(article_data['category'], 1)
        
        article_id = db.create_article(
            title=article_data['title'],
            content=article_data['content'],
            category_id=category_id,
            tags=article_data['tags']
        )
        
        print(f"✅ Creado: {article_data['title']}")
    
    print(f"\n🎉 Se crearon {len(demo_articles)} artículos de demostración")
    print("Ejecuta 'python main.py' para ver la aplicación con contenido de ejemplo")

if __name__ == "__main__":
    create_demo_data()