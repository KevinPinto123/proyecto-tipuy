from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from datetime import datetime
from rpa_service import RPAService

app = Flask(__name__)
CORS(app)

# Inicializar servicio RPA
rpa_service = RPAService()

@app.route('/')
def index():
    """Página principal del sistema universitario"""
    return render_template('index.html')

@app.route('/api/generar-constancia', methods=['POST'])
def generar_constancia():
    """Endpoint para generar constancia académica"""
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['nombre', 'codigo', 'carrera', 'ciclo']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} es requerido'}), 400
        
        # Ejecutar flujo RPA
        resultado = rpa_service.generar_constancia_completa(
            nombre=data['nombre'],
            codigo=data['codigo'],
            carrera=data['carrera'],
            ciclo=data['ciclo']
        )
        
        return jsonify({
            'success': True,
            'mensaje': 'Constancia generada exitosamente',
            'archivo_pdf': resultado['archivo_pdf'],
            'registro_id': resultado['registro_id']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/obtener-seguimiento', methods=['GET'])
def obtener_seguimiento():
    """Obtener lista de constancias para seguimiento"""
    try:
        constancias = rpa_service.obtener_seguimiento()
        return jsonify({'constancias': constancias})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/firmar-constancia', methods=['POST'])
def firmar_constancia():
    """Simular firma digital de autoridad"""
    try:
        data = request.json
        registro_id = data.get('registro_id')
        
        if not registro_id:
            return jsonify({'error': 'ID de registro requerido'}), 400
        
        resultado = rpa_service.firmar_constancia(registro_id)
        
        return jsonify({
            'success': True,
            'mensaje': 'Constancia firmada exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Crear carpetas necesarias
    os.makedirs('autoridad_entrada', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Sistema Universitario RPA iniciado")
    print("📋 Accede a: http://localhost:5000")
    app.run(debug=True, port=5000)