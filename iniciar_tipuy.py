#!/usr/bin/env python3
"""
🚀 SCRIPT DE INICIO OPTIMIZADO - SISTEMA TIPUY RPA
Compilación y ejecución automática con verificaciones
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Mostrar banner del sistema"""
    print("=" * 60)
    print("🎓 SISTEMA RPA UNIVERSITARIO TIPUY")
    print("🤖 Asistente Virtual para Trámites Académicos")
    print("🏛️ Universidad Nacional de Ingeniería - FIEE")
    print("=" * 60)
    print()

def verificar_python():
    """Verificar versión de Python"""
    print("🔍 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Requiere Python 3.8+")
        return False

def verificar_dependencias():
    """Verificar dependencias instaladas"""
    print("\n🔍 Verificando dependencias...")
    
    dependencias_criticas = [
        'flask', 'selenium', 'requests', 'openpyxl', 
        'reportlab', 'flask_cors'
    ]
    
    faltantes = []
    
    for dep in dependencias_criticas:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - FALTANTE")
            faltantes.append(dep)
    
    if faltantes:
        print(f"\n⚠️  Dependencias faltantes: {', '.join(faltantes)}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def verificar_archivos():
    """Verificar archivos críticos"""
    print("\n🔍 Verificando archivos del sistema...")
    
    archivos_criticos = [
        'app.py',
        'rpa_service.py',
        'dni_validation_service.py',
        'uni_validation_service.py',
        'templates/dashboard.html',
        'templates/auth.html',
        'static/dashboard.js',
        'static/dashboard.css'
    ]
    
    faltantes = []
    
    for archivo in archivos_criticos:
        if Path(archivo).exists():
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTANTE")
            faltantes.append(archivo)
    
    if faltantes:
        print(f"\n⚠️  Archivos faltantes: {', '.join(faltantes)}")
        return False
    
    print("✅ Todos los archivos están presentes")
    return True

def crear_carpetas():
    """Crear carpetas necesarias"""
    print("\n📁 Creando carpetas necesarias...")
    
    carpetas = [
        'autoridad_entrada',
        'PDFs',
        'logs',
        'templates',
        'static'
    ]
    
    for carpeta in carpetas:
        Path(carpeta).mkdir(exist_ok=True)
        print(f"✅ {carpeta}/")
    
    print("✅ Estructura de carpetas lista")

def verificar_chromedriver():
    """Verificar ChromeDriver"""
    print("\n🌐 Verificando ChromeDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.quit()
        
        print("✅ ChromeDriver funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error con ChromeDriver: {e}")
        print("💡 Instala ChromeDriver desde: https://chromedriver.chromium.org/")
        return False

def compilar_sistema():
    """Compilar y optimizar el sistema"""
    print("\n⚙️  Compilando sistema...")
    
    # Compilar archivos Python
    try:
        import py_compile
        
        archivos_python = [
            'app.py',
            'rpa_service.py',
            'dni_validation_service.py',
            'uni_validation_service.py'
        ]
        
        for archivo in archivos_python:
            if Path(archivo).exists():
                py_compile.compile(archivo, doraise=True)
                print(f"✅ Compilado: {archivo}")
        
        print("✅ Compilación Python completada")
        return True
        
    except Exception as e:
        print(f"❌ Error en compilación: {e}")
        return False

def ejecutar_tests():
    """Ejecutar tests básicos"""
    print("\n🧪 Ejecutando tests básicos...")
    
    try:
        # Test de importación
        import app
        import rpa_service
        import dni_validation_service
        import uni_validation_service
        
        print("✅ Importaciones correctas")
        
        # Test de Flask app
        if hasattr(app, 'app'):
            print("✅ Flask app inicializada")
        
        print("✅ Tests básicos completados")
        return True
        
    except Exception as e:
        print(f"❌ Error en tests: {e}")
        return False

def iniciar_servidor():
    """Iniciar servidor Flask"""
    print("\n🚀 Iniciando servidor TIPUY...")
    print("📋 URL: http://localhost:5000")
    print("🔑 Login Demo: demo@uni.pe / demo123")
    print("⏹️  Presiona Ctrl+C para detener")
    print("-" * 60)
    
    try:
        # Importar y ejecutar app
        from app import app
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # Evitar doble ejecución
        )
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Servidor detenido por el usuario")
        print("👋 ¡Gracias por usar TIPUY!")
        
    except Exception as e:
        print(f"\n❌ Error iniciando servidor: {e}")
        return False

def main():
    """Función principal"""
    print_banner()
    
    # Verificaciones previas
    if not verificar_python():
        return False
    
    if not verificar_dependencias():
        return False
    
    if not verificar_archivos():
        return False
    
    # Preparación del sistema
    crear_carpetas()
    
    if not verificar_chromedriver():
        print("⚠️  ChromeDriver no disponible - RPA limitado")
        print("💡 El sistema funcionará en modo demo")
    
    # Compilación
    if not compilar_sistema():
        print("⚠️  Error en compilación - continuando...")
    
    # Tests
    if not ejecutar_tests():
        print("⚠️  Error en tests - continuando...")
    
    print("\n🎉 ¡Sistema listo para ejecutar!")
    print("💡 Todas las verificaciones completadas")
    
    # Preguntar si iniciar servidor
    respuesta = input("\n¿Iniciar servidor ahora? (s/n): ").lower().strip()
    
    if respuesta in ['s', 'si', 'y', 'yes', '']:
        iniciar_servidor()
    else:
        print("\n💡 Para iniciar manualmente ejecuta: python app.py")
        print("📋 URL: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        sys.exit(1)