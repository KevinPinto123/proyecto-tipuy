@echo off
echo ============================================================
echo 🧪 TESTS AUTOMATIZADOS - TIPUY RPA
echo ============================================================
echo.

echo 🔍 Ejecutando tests del sistema...
python test_sistema.py

echo.
echo 🔍 Verificando APIs...
python -c "
import requests
import time
print('⏳ Esperando servidor...')
time.sleep(2)
try:
    r = requests.get('http://localhost:5000/api/obtener-seguimiento', timeout=5)
    print(f'✅ API Status: {r.status_code}')
except:
    print('❌ Servidor no disponible')
"

pause