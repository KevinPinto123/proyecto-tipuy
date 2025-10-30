@echo off
echo ============================================================
echo 🛠️  MODO DESARROLLO - TIPUY RPA
echo ============================================================
echo.

echo 🔍 Verificando sistema...
python -c "import app; print('✅ App OK')"
python -c "import rpa_service; print('✅ RPA OK')"
python -c "import selenium; print('✅ Selenium OK')"

echo.
echo 🚀 Iniciando en modo desarrollo...
python app.py

pause