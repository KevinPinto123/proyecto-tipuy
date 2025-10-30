# Sistema RPA Universitario - TIPUY 🎓

Sistema automatizado de gestión de trámites académicos para la Facultad de Ingeniería Eléctrica y Electrónica (FIEE) de la Universidad Nacional de Ingeniería (UNI).

## 🚀 Características Principales

### ✨ Funcionalidades Implementadas

- **🤖 Asistente Virtual TIPUY**: Chat inteligente para consultas académicas
- **🔐 Autenticación Segura**: Sistema de login con Supabase (modo demo disponible)
- **📄 Generación Automática**: Constancias de matrícula con validación completa
- **🆔 Validación DNI**: Verificación de documentos de identidad
- **🎓 Validación UNI**: Verificación de códigos estudiantiles en portal institucional
- **📊 Dashboard Moderno**: Interfaz intuitiva con navegación fluida
- **📱 Diseño Responsivo**: Compatible con dispositivos móviles
- **🔒 Seguridad**: Cifrado extremo a extremo y validaciones robustas

### 🛠️ Tecnologías Utilizadas

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Base de Datos**: Supabase (PostgreSQL)
- **Automatización**: Selenium WebDriver
- **Autenticación**: Supabase Auth
- **Estilos**: Bootstrap 5 + CSS personalizado
- **Iconos**: Font Awesome 6

## 📁 Estructura del Proyecto

```
proyecto/
├── app.py                      # Aplicación Flask principal
├── rpa_service.py             # Servicio de automatización RPA
├── uni_validation_service.py   # Validación portal UNI
├── dni_validation_service.py   # Validación DNI
├── test_sistema.py            # Script de pruebas
├── README.md                  # Documentación
├── templates/
│   ├── auth.html             # Página de autenticación
│   ├── dashboard.html        # Dashboard principal
│   ├── chat.html            # Interfaz de chat
│   └── configuracion.html   # Página de configuración
├── static/
│   ├── dashboard.css        # Estilos principales
│   ├── dashboard.js         # Lógica del dashboard
│   ├── demo-config.js       # Configuración demo
│   └── demo-data.js         # Datos de demostración
└── autoridad_entrada/        # Carpeta para PDFs generados
```

## 🚀 Instalación y Configuración

### 1. Requisitos Previos

```bash
# Python 3.8 o superior
python --version

# Instalar dependencias
pip install flask flask-cors selenium requests beautifulsoup4 reportlab
```

### 2. Configuración del Navegador

```bash
# Descargar ChromeDriver desde:
# https://chromedriver.chromium.org/
# Colocar en PATH del sistema
```

### 3. Configuración de Supabase (Opcional)

```javascript
// En static/demo-config.js
const supabaseUrl = 'TU_SUPABASE_URL';
const supabaseKey = 'TU_SUPABASE_ANON_KEY';
```

### 4. Ejecutar la Aplicación

```bash
# Iniciar servidor
python app.py

# La aplicación estará disponible en:
# http://localhost:5000
```

## 🎯 Uso del Sistema

### 1. Autenticación

- **Modo Demo**: Usar credenciales de prueba
- **Modo Producción**: Login con Supabase

### 2. Dashboard Principal

- **Chat TIPUY**: Asistente virtual para consultas
- **Trámites**: Gestión de solicitudes
- **Configuración**: Validación DNI + UNI
- **Notificaciones**: Estado de trámites

### 3. Generación de Constancias

1. Ir a **Configuración**
2. Completar datos personales
3. **Validar DNI** con RENIEC
4. **Validar Código UNI** en portal institucional
5. Seleccionar carrera y ciclo
6. **Generar Constancia** automáticamente

### 4. Chat con TIPUY

- Consultas en lenguaje natural
- Acciones rápidas predefinidas
- Respuestas contextuales inteligentes

## 🔧 API Endpoints

### Autenticación
- `GET /` - Redirección a auth
- `GET /auth` - Página de login
- `GET /dashboard` - Dashboard principal

### Validaciones
- `POST /api/validar-dni` - Validar DNI en RENIEC
- `POST /api/validar-estudiante` - Validar en portal UNI
- `POST /api/validar-uni` - Validación UNI alternativa

### Constancias
- `POST /api/generar-constancia` - Generar constancia
- `GET /api/obtener-seguimiento` - Listar constancias
- `GET /api/descargar-constancia/<id>` - Descargar PDF
- `DELETE /api/eliminar-constancia` - Eliminar constancia

### Contenido
- `GET /api/chat` - Contenido del chat
- `GET /api/configuracion-page` - Página de configuración

## 🧪 Pruebas

```bash
# Ejecutar pruebas automatizadas
python test_sistema.py

# Verificar endpoints manualmente
curl http://localhost:5000/api/obtener-seguimiento
```

## 🔒 Seguridad

### Validaciones Implementadas

- **DNI**: Verificación con RENIEC
- **Código UNI**: Validación en portal institucional
- **Correo**: Verificación dominio @uni.pe
- **Datos**: Sanitización de inputs
- **Archivos**: Validación de tipos y tamaños

### Medidas de Seguridad

- Cifrado de comunicaciones
- Validación de sesiones
- Sanitización de datos
- Rate limiting (recomendado)
- Logs de auditoría

## 📊 Datos de Demostración

### Estudiantes de Prueba

| Código    | Nombre                    | DNI      | Carrera                |
|-----------|---------------------------|----------|------------------------|
| 20210001A | Juan Carlos Pérez         | 12345678 | Ingeniería Eléctrica   |
| 20210002B | María García López        | 87654321 | Ingeniería Electrónica |
| 20220259H | Kevin Eduardo Pinto       | 77804421 | Ing. Telecomunicaciones|
| 20230001C | Ana Sofía Mendoza         | 11223344 | Ing. Ciberseguridad    |

## 🚀 Despliegue en Producción

### 1. Configuración del Servidor

```bash
# Usar servidor WSGI como Gunicorn
pip install gunicorn

# Ejecutar en producción
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2. Variables de Entorno

```bash
export FLASK_ENV=production
export SUPABASE_URL=tu_url_real
export SUPABASE_KEY=tu_key_real
```

### 3. Nginx (Opcional)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🐛 Solución de Problemas

### Errores Comunes

1. **ChromeDriver no encontrado**
   ```bash
   # Descargar y agregar al PATH
   export PATH=$PATH:/ruta/a/chromedriver
   ```

2. **Error de conexión Supabase**
   ```javascript
   // Verificar credenciales en demo-config.js
   // Usar modo demo si es necesario
   ```

3. **Puerto 5000 ocupado**
   ```bash
   # Cambiar puerto en app.py
   app.run(debug=True, port=5001)
   ```

## 📈 Roadmap Futuro

- [ ] Integración con más servicios UNI
- [ ] Notificaciones push
- [ ] Firma digital avanzada
- [ ] API REST completa
- [ ] Aplicación móvil
- [ ] Análisis de datos
- [ ] Inteligencia artificial mejorada

## 👥 Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

- **Email**: soporte@tipuy.uni.pe
- **Documentación**: [Wiki del proyecto]
- **Issues**: [GitHub Issues]

---

**TIPUY** - *Transformando la gestión académica con inteligencia artificial* 🎓✨

Desarrollado con ❤️ para la comunidad UNI