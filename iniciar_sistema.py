#!/usr/bin/env python3
"""
Script de inicio rápido para el Sistema Universitario RPA
"""

import os
import sys
import subprocess
import webbrowser
import time

def verificar_python():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def instalar_dependencias():
    """Instalar dependencias automáticamente"""
    print("📦 Instalando dependencias...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def crear_carpetas():
    """Crear carpetas necesarias"""
    carpetas = ["autoridad_entrada", "templates", "static"]
    
    for carpeta in carpetas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print(f"✅ Carpeta creada: {carpeta}")

def iniciar_servidor():
    """Iniciar el servidor Flask"""
    print("\n🚀 Iniciando Sistema Universitario RPA...")
    print("=" * 50)
    
    try:
        # Importar y ejecutar la aplicación
        from app import app
        
        print("🌐 Servidor iniciado en: http://localhost:5000")
        print("📋 Presiona Ctrl+C para detener el servidor")
        print("=" * 50)
        
        # Abrir navegador automáticamente
        time.sleep(2)
        webbrowser.open("http://localhost:5000")
        
        # Iniciar servidor
        app.run(debug=True, port=5000, use_reloader=False)
        
    except ImportError as e:
        print(f"❌ Error importando aplicación: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n👋 Sistema detenido por el usuario")
        return True
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def mostrar_bienvenida():
    """Mostrar mensaje de bienvenida"""
    print("🎓 SISTEMA UNIVERSITARIO RPA")
    print("=" * 50)
    print("Sistema completo de automatización universitaria")
    print("Generación de constancias + RPA + Seguimiento web")
    print("=" * 50)

def mostrar_instrucciones():
    """Mostrar instrucciones de uso"""
    print("\n📋 INSTRUCCIONES DE USO:")
    print("1. Llenar formulario de constancia")
    print("2. Hacer clic en 'Generar Constancia con RPA'")
    print("3. Observar logs de automatización en tiempo real")
    print("4. Ver seguimiento en panel derecho")
    print("5. Simular firma digital con botón 'Firmar'")
    print("\n📁 ARCHIVOS GENERADOS:")
    print("- PDFs: carpeta 'autoridad_entrada/'")
    print("- Seguimiento: archivo 'seguimiento.xlsx'")

def main():
    """Función principal"""
    mostrar_bienvenida()
    
    # Verificaciones previas
    if not verificar_python():
        input("\nPresiona Enter para salir...")
        return False
    
    # Crear carpetas
    crear_carpetas()
    
    # Preguntar si instalar dependencias
    respuesta = input("\n¿Instalar/actualizar dependencias? (s/N): ").lower()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        if not instalar_dependencias():
            input("\nPresiona Enter para salir...")
            return False
    
    # Mostrar instrucciones
    mostrar_instrucciones()
    
    # Confirmar inicio
    input("\nPresiona Enter para iniciar el servidor...")
    
    # Iniciar sistema
    return iniciar_servidor()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Salida por teclado")
        sys.exit(0)