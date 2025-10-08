# 🎓 Sistema Universitario RPA

Sistema web completo que simula procesos universitarios automatizados con RPA, incluyendo generación de constancias académicas, seguimiento administrativo y simulación de firmas digitales.

## 🚀 Características

- **Generación Automatizada**: Constancias académicas en PDF con RPA
- **Seguimiento en Tiempo Real**: Panel web para monitorear el estado de documentos
- **Simulación de Autoridades**: Proceso de firma digital automatizado
- **Integración Completa**: Excel + PDF + Web + RPA en un solo sistema

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **RPA**: rpaframework + Selenium
- **PDF**: reportlab
- **Excel**: openpyxl
- **Frontend**: HTML5 + Bootstrap + JavaScript
- **Automatización**: Navegador Chrome automatizado

## 📋 Requisitos Previos

- Python 3.13+
- Google Chrome instalado
- Conexión a internet (para descargar ChromeDriver automáticamente)

## ⚡ Instalación Rápida

1. **Clonar o descargar el proyecto**
```bash
cd sistema-universitario-rpa
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar el sistema**
```bash
python app.py
```

4. **Abrir en navegador**
```
http://localhost:5000
```

## 🎯 Cómo Usar el Sistema

### 1. Generar Constancia
- Llenar el formulario con datos del estudiante
- Hacer clic en "Generar Constancia con RPA"
- Observar los logs en tiempo real del proceso RPA
- El sistema automáticamente:
  - Abre navegador Chrome
  - Genera PDF de constancia
  - Guarda en carpeta `autoridad_entrada/`
  - Registra en Excel `seguimiento.xlsx`

### 2. Seguimiento de Constancias
- Ver tabla con todas las constancias generadas
- Estados: "Enviado" → "Firmado y Aprobado"
- Firmas: "Pendiente" → "Firmado"

### 3. Simular Firma Digital
- Hacer clic en botón "Firmar" de cualquier constancia pendiente
- El sistema actualiza automáticamente el estado en Excel

## 📁 Estructura del Proyecto

```
sistema-universitario-rpa/
├── app.py                 # Servidor Flask principal
├── rpa_service.py         # Lógica RPA y automatización
├── requirements.txt       # Dependencias Python
├── templates/
│   └── index.html        # Interfaz web principal
├── static/
│   └── app.js           # JavaScript frontend
├── autoridad_entrada/    # PDFs generados (se crea automáticamente)
├── seguimiento.xlsx      # Excel de seguimiento (se crea automáticamente)
└── README.md            # Este archivo
```

## 🔄 Flujo RPA Completo

1. **Entrada**: Datos del estudiante desde formulario web
2. **Automatización**: 
   - Abre navegador Chrome
   - Realiza búsqueda demo en Google
   - Cierra navegador
3. **Generación PDF**: Constancia académica con datos oficiales
4. **Almacenamiento**: PDF en carpeta de autoridades
5. **Registro**: Entrada en Excel con estado y metadatos
6. **Respuesta**: Confirmación en interfaz web

## 📊 Logs del Sistema

El sistema muestra logs detallados en consola y web:

```
✅ Navegador abierto correctamente
✅ Búsqueda de constancia académica realizada  
✅ Navegador cerrado correctamente
✅ PDF generado: constancia_20241001_143022.pdf
✅ Constancia enviada a autoridad
✅ Seguimiento actualizado en Excel
✅ Flujo RPA completado exitosamente
```

## 🎨 Interfaz Web

- **Diseño Responsivo**: Bootstrap 5 + Font Awesome
- **Tiempo Real**: Logs de RPA en vivo
- **Estadísticas**: Contadores automáticos
- **UX Intuitiva**: Notificaciones y estados visuales

## 🔧 Personalización

### Modificar Carreras
Editar en `templates/index.html` líneas 45-51:
```html
<option value="Tu Nueva Carrera">Tu Nueva Carrera</option>
```

### Cambiar Formato PDF
Modificar método `_generar_pdf_constancia()` en `rpa_service.py`

### Agregar Campos Excel
Actualizar headers en método `_inicializar_excel()` en `rpa_service.py`

## 🚨 Solución de Problemas

### Error de ChromeDriver
- El sistema descarga ChromeDriver automáticamente
- Si falla, verificar conexión a internet

### Error de Permisos Excel
- Cerrar Excel si está abierto
- Verificar permisos de escritura en carpeta

### Puerto 5000 Ocupado
Cambiar puerto en `app.py`:
```python
app.run(debug=True, port=5001)  # Usar puerto 5001
```

## 📈 Demostración para Profesores

Este sistema demuestra:

1. **Integración RPA-Web**: Automatización backend con interfaz moderna
2. **Flujo Completo**: Desde formulario hasta documento firmado
3. **Tecnologías Actuales**: Python, Flask, Selenium, Bootstrap
4. **Casos de Uso Reales**: Procesos universitarios automatizados
5. **Escalabilidad**: Base para sistemas más complejos

## 🎓 Casos de Uso Universitarios

- Constancias de estudios
- Certificados de notas
- Solicitudes de documentos
- Procesos de matrícula
- Seguimiento administrativo
- Firmas digitales institucionales

## 📞 Soporte

Para dudas o mejoras, revisar:
- Logs en consola del servidor
- Archivo `seguimiento.xlsx` generado
- PDFs en carpeta `autoridad_entrada/`
- Código comentado en `rpa_service.py`

---

**Desarrollado con ❤️ para demostrar el poder de RPA en procesos universitarios**