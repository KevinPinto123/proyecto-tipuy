#!/usr/bin/env python3
"""
🧪 TEST - Validación de Códigos UNI con formato correcto
Prueba códigos con formato: 8 dígitos + 1 letra mayúscula
"""

import requests
import json
import time

# Códigos de prueba con formato correcto
CODIGOS_PRUEBA = [
    '20220259H',  # Kevin Eduardo Pinto
    '20210001A',  # Juan Carlos Pérez
    '20210002B',  # María García López
    '20230001C',  # Ana Sofía Mendoza
    '20241234X',  # Código ficticio
]

def test_formato_codigo(codigo):
    """Probar formato de código UNI"""
    import re
    
    print(f"\n🔍 Probando código: {codigo}")
    
    # Validar formato
    if re.match(r'^\d{8}[A-Z]$', codigo):
        print(f"✅ Formato válido: {len(codigo)} caracteres (8 dígitos + 1 letra)")
        return True
    else:
        print(f"❌ Formato inválido: {codigo}")
        print(f"   Longitud: {len(codigo)}")
        print(f"   Formato esperado: 8 dígitos + 1 letra mayúscula")
        return False

def test_api_validacion(codigo):
    """Probar API de validación"""
    url = 'http://localhost:5000/api/validar-uni'
    
    try:
        response = requests.post(url, 
                               json={'codigo': codigo}, 
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ API: Código válido")
                print(f"   Nombre: {result.get('data', {}).get('nombre', 'N/A')}")
                print(f"   Carrera: {result.get('data', {}).get('carrera', 'N/A')}")
            else:
                print(f"❌ API: {result.get('message', 'Error desconocido')}")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Asegúrate de que el servidor esté corriendo en localhost:5000")

def main():
    """Función principal"""
    print("🧪 TEST DE CÓDIGOS UNI - FORMATO CORRECTO")
    print("=" * 50)
    print("📋 Formato esperado: 8 dígitos + 1 letra mayúscula")
    print("📋 Ejemplos válidos: 20220259H, 20210001A, 20230001C")
    print("=" * 50)
    
    # Probar formatos
    print("\n1️⃣ PRUEBAS DE FORMATO:")
    for codigo in CODIGOS_PRUEBA:
        test_formato_codigo(codigo)
    
    # Probar API (si el servidor está corriendo)
    print("\n2️⃣ PRUEBAS DE API:")
    print("⏳ Esperando servidor...")
    time.sleep(1)
    
    for codigo in CODIGOS_PRUEBA[:3]:  # Solo los primeros 3
        test_api_validacion(codigo)
        time.sleep(1)  # Evitar spam
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")
    print("💡 Usa códigos con formato: 20220259H")

if __name__ == "__main__":
    main()