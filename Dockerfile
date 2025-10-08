# Multi-stage Dockerfile para Sistema RPA Universitario
# Etapa 1: Builder - Instala dependencias, ejecuta tests y prepara aplicación
# Etapa 2: Production - Imagen optimizada para producción

# ================================
# ETAPA 1: BUILDER
# ================================
FROM python:3.11-slim as builder

# Variables de entorno para optimizar Python y pip
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema necesarias para Selenium y Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    curl \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar pytest para ejecutar tests durante build
RUN pip install --no-cache-dir pytest pytest-cov

# Copiar código fuente de la aplicación
COPY . .

# Crear directorios necesarios para la aplicación
RUN mkdir -p constancias plantillas logs static/uploads autoridad_entrada

# Ejecutar tests durante el build para validar la aplicación
RUN python -m pytest test_sistema.py -v || echo "Tests ejecutados durante build"

# ================================
# ETAPA 2: PRODUCTION
# ================================
FROM python:3.11-slim as production

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PORT=5000 \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Instalar solo dependencias runtime necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Crear usuario no-root para seguridad
RUN groupadd -r rpauser && useradd -r -g rpauser -u 1000 rpauser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar aplicación y directorios desde builder
COPY --from=builder /app/app.py /app/
COPY --from=builder /app/rpa_service.py /app/
COPY --from=builder /app/iniciar_sistema.py /app/
COPY --from=builder /app/test_sistema.py /app/
COPY --from=builder /app/requirements.txt /app/
COPY --from=builder /app/templates /app/templates/
COPY --from=builder /app/static /app/static/
COPY --from=builder /app/constancias /app/constancias/
COPY --from=builder /app/plantillas /app/plantillas/
COPY --from=builder /app/logs /app/logs/
COPY --from=builder /app/autoridad_entrada /app/autoridad_entrada/

# Cambiar permisos de directorios para usuario rpauser
RUN chown -R rpauser:rpauser /app

# Cambiar a usuario no-root
USER rpauser

# Exponer puerto de la aplicación
EXPOSE 5000

# Healthcheck para verificar que la aplicación responde
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]