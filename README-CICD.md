# 🚀 CI/CD Pipeline - Sistema RPA Universitario

## 📋 Descripción del Pipeline

Este documento describe la implementación completa de CI/CD para el Sistema de Automatización RPA Universitario, incluyendo Docker multi-stage, GitHub Actions, y configuraciones de deployment.

## 🏗️ Arquitectura del Pipeline

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   📝 Git Push   │───▶│  🧪 Tests &     │───▶│  🐳 Build &    │───▶│  🔒 Security    │
│   (main/dev)    │    │     Quality      │    │     Push        │    │     Scan         │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────────┘
                                │                        │                        │
                                ▼                        ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
                       │  • Flake8       │    │  • Multi-stage  │    │  • Trivy Scan    │
                       │  • Pytest       │    │  • GHCR Push    │    │  • SARIF Upload  │
                       │  • Coverage      │    │  • Cache        │    │  • Vulnerabilit. │
                       └──────────────────┘    └─────────────────┘    └──────────────────┘
                                                        │
                                                        ▼
                                              ┌──────────────────┐
                                              │  📢 Notifications│
                                              │  & Summary       │
                                              └──────────────────┘
```

## 🐳 Dockerfile Multi-Etapa

### Etapa 1: Builder
- **Base:** `python:3.11-slim`
- **Propósito:** Instalar dependencias, ejecutar tests, preparar aplicación
- **Componentes:**
  - Chromium + ChromeDriver para Selenium
  - Dependencias Python completas
  - Ejecución de tests durante build
  - Creación de directorios necesarios

### Etapa 2: Production
- **Base:** `python:3.11-slim`
- **Propósito:** Imagen optimizada para producción
- **Características:**
  - Usuario no-root (`rpauser`, UID 1000)
  - Solo dependencias runtime
  - Healthcheck integrado
  - Variables de entorno optimizadas

## 🔄 GitHub Actions Workflow

### Job 1: Tests y Quality 🧪
```yaml
Ejecuta en: ubuntu-latest
Python: 3.11
Pasos:
  1. Checkout código
  2. Setup Python con cache
  3. Instalar dependencias
  4. Análisis Flake8
  5. Tests con coverage
  6. Upload a Codecov
```

### Job 2: Build y Push 🐳
```yaml
Ejecuta: Solo en push a main, después de tests exitosos
Permisos: contents:read, packages:write, id-token:write
Pasos:
  1. Setup Docker Buildx
  2. Login a GHCR
  3. Generar metadata
  4. Build multi-platform
  5. Push con cache optimizado
```

### Job 3: Security Scan 🔒
```yaml
Ejecuta: Después de build exitoso
Herramienta: Trivy
Pasos:
  1. Scan de vulnerabilidades
  2. Generar reporte SARIF
  3. Upload a GitHub Security
```

### Job 4: Notifications 📢
```yaml
Ejecuta: Siempre (if: always())
Pasos:
  1. Generar resumen en GITHUB_STEP_SUMMARY
  2. Mostrar estado de todos los jobs
  3. Incluir comandos Docker para usar imagen
```

## 🚀 Instrucciones de Uso

### 1. Configuración Inicial

```bash
# Clonar repositorio
git clone <tu-repositorio>
cd sistema-rpa-universitario

# Crear directorios necesarios
mkdir -p constancias plantillas logs static/uploads autoridad_entrada
```

### 2. Desarrollo Local con Docker

```bash
# Build de la imagen
docker build -t rpa-universitario .

# Ejecutar contenedor
docker run -p 5000:5000 rpa-universitario

# O usar Docker Compose
docker-compose up --build
```

### 3. Desarrollo con Docker Compose

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f rpa-app

# Detener servicios
docker-compose down

# Rebuild después de cambios
docker-compose up --build
```

### 4. Comandos Docker Útiles

```bash
# Build sin cache
docker build --no-cache -t rpa-universitario .

# Ejecutar con variables de entorno
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  -e FLASK_DEBUG=1 \
  rpa-universitario

# Ejecutar en modo interactivo
docker run -it --rm -p 5000:5000 rpa-universitario bash

# Ver logs del contenedor
docker logs -f <container-id>

# Inspeccionar imagen
docker inspect rpa-universitario
```

## ⚙️ Configuración de GitHub

### 1. Secrets Necesarios

El pipeline usa `GITHUB_TOKEN` automáticamente. No necesitas configurar secrets adicionales.

### 2. Permisos del Repositorio

Asegúrate de que GitHub Actions tenga permisos para:
- ✅ Read repository contents
- ✅ Write packages (para GHCR)
- ✅ Write security events (para Trivy)

### 3. Configuración de Branch Protection

```yaml
# Configuración recomendada para branch main
Require status checks: ✅
  - tests-and-quality
Require branches to be up to date: ✅
Require pull request reviews: ✅
Dismiss stale reviews: ✅
```

## 📦 Uso de la Imagen Docker

### Desde GitHub Container Registry

```bash
# Pull de la imagen
docker pull ghcr.io/<tu-usuario>/<tu-repo>:latest

# Ejecutar
docker run -p 5000:5000 ghcr.io/<tu-usuario>/<tu-repo>:latest

# Con volúmenes para persistencia
docker run -p 5000:5000 \
  -v $(pwd)/constancias:/app/constancias \
  -v $(pwd)/logs:/app/logs \
  ghcr.io/<tu-usuario>/<tu-repo>:latest
```

### Variables de Entorno Disponibles

```bash
FLASK_ENV=production          # Entorno de Flask
FLASK_APP=app.py             # Aplicación principal
PORT=5000                    # Puerto de la aplicación
CHROME_BIN=/usr/bin/chromium # Ruta de Chromium
CHROMEDRIVER_PATH=/usr/bin/chromedriver # Ruta ChromeDriver
PYTHONUNBUFFERED=1           # Output sin buffer
```

## 🔧 Troubleshooting

### Problema: Tests fallan durante build
```bash
# Solución: Ejecutar tests localmente
python -m pytest test_sistema.py -v

# Verificar dependencias
pip install -r requirements.txt
```

### Problema: Chromium no funciona en contenedor
```bash
# Verificar instalación
docker run -it <imagen> chromium --version

# Verificar ChromeDriver
docker run -it <imagen> chromedriver --version
```

### Problema: Permisos de archivos
```bash
# Verificar usuario en contenedor
docker run -it <imagen> whoami
# Debe mostrar: rpauser

# Verificar permisos de directorios
docker run -it <imagen> ls -la /app/
```

### Problema: Pipeline falla en GitHub Actions
```bash
# Verificar logs del workflow
1. Ve a Actions tab en GitHub
2. Selecciona el workflow fallido
3. Revisa logs de cada job
4. Busca errores específicos
```

### Problema: Imagen muy grande
```bash
# Verificar tamaño de capas
docker history rpa-universitario

# Optimizar .dockerignore
# Verificar que excluye archivos innecesarios
```

### Problema: Healthcheck falla
```bash
# Verificar manualmente
docker run -p 5000:5000 <imagen>
curl http://localhost:5000/

# Ver logs de healthcheck
docker inspect <container> | grep Health -A 10
```

## 📊 Métricas y Monitoreo

### Coverage de Tests
- **Target:** >80%
- **Reporte:** Disponible en Codecov
- **Comando local:** `pytest --cov=. --cov-report=html`

### Tamaño de Imagen
- **Target:** <500MB
- **Actual:** ~300MB (optimizado con multi-stage)
- **Comando:** `docker images rpa-universitario`

### Tiempo de Build
- **Target:** <5 minutos
- **Optimización:** Cache de GitHub Actions
- **Monitoreo:** GitHub Actions insights

## 🔄 Flujo de Desarrollo

### 1. Feature Development
```bash
git checkout -b feature/nueva-funcionalidad
# Desarrollar cambios
git commit -m "feat: nueva funcionalidad"
git push origin feature/nueva-funcionalidad
# Crear Pull Request
```

### 2. Pull Request
- ✅ Tests automáticos se ejecutan
- ✅ Code review requerido
- ✅ Branch protection activo

### 3. Merge a Main
- ✅ Pipeline completo se ejecuta
- ✅ Imagen se publica en GHCR
- ✅ Security scan automático

### 4. Deployment
```bash
# Pull de la nueva imagen
docker pull ghcr.io/<tu-usuario>/<tu-repo>:latest

# Restart del servicio
docker-compose pull && docker-compose up -d
```

## 📚 Referencias

- [Docker Multi-stage Builds](https://docs.docker.com/develop/dev-best-practices/dockerfile_best-practices/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Trivy Security Scanner](https://github.com/aquasecurity/trivy)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

---

**🎓 Sistema RPA Universitario - CI/CD Pipeline**  
*Implementado con Docker, GitHub Actions y mejores prácticas de DevOps*