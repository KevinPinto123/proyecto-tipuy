#!/usr/bin/env python3
"""
Script de prueba para verificar el Sistema Universitario RPA
"""

import os
import sys
import requests
import time
from rpa_service import RPAService

def test_rpa_service():
    """Probar el servicio RPA directamente"""
    print("🧪 Probando servicio RPA...")
    
    try:
        rpa = RPAService()
        
        # Datos de prueba
        resultado = rpa.generar_constancia_completa(
            nombre="Kevin Pinto",
            codigo="20241234",
            carrera="Ingeniería de Sistemas", 
            ciclo="2024-2"
        )
        
        print(f"✅ PDF generado: {resultado['archivo_pdf']}")
        print(f"✅ ID registro: {resultado['registro_id']}")
        
        # Verificar archivos generados
        if os.path.exists("seguimiento.xlsx"):
            print("✅ Excel de seguimiento creado")
        
        if os.path.exists("autoridad_entrada"):
            pdfs = [f for f in os.listdir("autoridad_entrada") if f.endswith('.pdf')]
            print(f"✅ {len(pdfs)} PDF(s) en carpeta autoridad")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en RPA: {e}")
        return False

def test_web_server():
    """Probar el servidor web (debe estar corriendo)"""
    print("\n🌐 Probando servidor web...")
    
    try:
        # Probar página principal
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ Página principal accesible")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
        
        # Probar API de seguimiento
        response = requests.get("http://localhost:5000/api/obtener-seguimiento", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API seguimiento: {len(data.get('constancias', []))} constancias")
        else:
            print(f"❌ Error API seguimiento: {response.status_code}")
            return False
        
        # Probar API de generación
        test_data = {
            "nombre": "Test Usuario",
            "codigo": "TEST001",
            "carrera": "Ingeniería de Sistemas",
            "ciclo": "2024-2"
        }
        
        response = requests.post(
            "http://localhost:5000/api/generar-constancia",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ API generación funcionando")
                print(f"   PDF: {result.get('archivo_pdf')}")
            else:
                print(f"❌ Error en generación: {result.get('error')}")
                return False
        else:
            print(f"❌ Error HTTP generación: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("   Asegúrate de que 'python app.py' esté corriendo")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def verificar_dependencias():
    """Verificar que todas las dependencias estén instaladas"""
    print("📦 Verificando dependencias...")
    
    dependencias = [
        'flask',
        'rpaframework', 
        'reportlab',
        'openpyxl',
        'selenium',
        'webdriver_manager'
    ]
    
    faltantes = []
    
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - FALTANTE")
            faltantes.append(dep)
    
    if faltantes:
        print(f"\n⚠️  Instalar dependencias faltantes:")
        print(f"pip install {' '.join(faltantes)}")
        return False
    
    return True

def main():
    """Función principal de pruebas"""
    print("🎓 Sistema Universitario RPA - Pruebas Automáticas")
    print("=" * 50)
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n❌ Faltan dependencias. Ejecuta: pip install -r requirements.txt")
        return False
    
    print("\n" + "=" * 50)
    
    # Probar RPA directamente
    rpa_ok = test_rpa_service()
    
    print("\n" + "=" * 50)
    
    # Probar servidor web si está disponible
    web_ok = test_web_server()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print(f"RPA Service: {'✅ OK' if rpa_ok else '❌ FALLO'}")
    print(f"Web Server: {'✅ OK' if web_ok else '❌ FALLO'}")
    
    if rpa_ok and web_ok:
        print("\n🎉 ¡Todas las pruebas pasaron!")
        print("🚀 El sistema está listo para la demostración")
        print("\n📋 Para usar:")
        print("1. python app.py")
        print("2. Abrir http://localhost:5000")
    elif rpa_ok:
        print("\n⚠️  RPA funciona, pero servidor web no disponible")
        print("   Ejecuta 'python app.py' en otra terminal")
    else:
        print("\n❌ Hay problemas con el sistema")
        print("   Revisa los errores arriba")
    
    return rpa_ok and web_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)