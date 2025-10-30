#!/usr/bin/env python3
"""
🏗️ BUILDER - Crear ejecutable standalone de TIPUY
"""

import os
import subprocess
import shutil
from pathlib import Path

def crear_ejecutable():
    """Crear ejecutable con PyInstaller"""
    print("🏗️ Creando ejecutable standalone...")
    
    # Comando PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',                    # Un solo archivo
        '--windowed',                   # Sin consola (opcional)
        '--name=TIPUY-RPA',            # Nombre del ejecutable
        '--icon=static/favicon.ico',    # Icono (si existe)
        '--add-data=templates;templates',  # Incluir templates
        '--add-data=static;static',        # Incluir static
        '--hidden-import=selenium',        # Importaciones ocultas
        '--hidden-import=flask',
        '--hidden-import=openpyxl',
        '--hidden-import=reportlab',
        'app.py'                          # Archivo principal
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Ejecutable creado en dist/TIPUY-RPA.exe")
        
        # Copiar archivos necesarios
        dist_path = Path('dist')
        if dist_path.exists():
            # Copiar carpetas necesarias
            for carpeta in ['templates', 'static']:
                if Path(carpeta).exists():
                    shutil.copytree(carpeta, dist_path / carpeta, dirs_exist_ok=True)
                    print(f"✅ Copiado: {carpeta}/")
        
        print("\n🎉 ¡Ejecutable listo!")
        print("📁 Ubicación: dist/TIPUY-RPA.exe")
        print("💡 Ejecuta directamente sin Python")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando ejecutable: {e}")
        return False
    
    return True

def crear_instalador():
    """Crear instalador con NSIS (opcional)"""
    print("\n📦 Para crear instalador:")
    print("1. Instala NSIS: https://nsis.sourceforge.io/")
    print("2. Crea script .nsi")
    print("3. Compila con makensis")

if __name__ == "__main__":
    print("🏗️ BUILDER TIPUY RPA")
    print("=" * 40)
    
    # Verificar PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller disponible")
    except ImportError:
        print("❌ PyInstaller no instalado")
        print("💡 Ejecuta: pip install pyinstaller")
        exit(1)
    
    # Crear ejecutable
    if crear_ejecutable():
        crear_instalador()