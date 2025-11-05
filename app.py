from flask import Flask, request, jsonify, render_template, redirect, send_file
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
    """Redirigir a autenticación"""
    return redirect('/auth')

@app.route('/auth')
def auth():
    """Página de autenticación"""
    return render_template('auth.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard principal - requiere autenticación"""
    return render_template('dashboard.html')

@app.route('/rpa')
def rpa_legacy():
    """Página RPA legacy para compatibilidad"""
    return render_template('index.html')

@app.route('/api/generar-constancia', methods=['POST'])
def generar_constancia():
    """Endpoint para generar constancia académica con validación UNI"""
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['nombre', 'codigo', 'carrera', 'ciclo']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} es requerido'}), 400
        
        # Validar correo institucional si se proporciona
        correo = data.get('correo')
        if correo and not correo.lower().endswith('@uni.pe'):
            return jsonify({'error': 'El correo debe ser institucional (@uni.pe)'}), 400
        
        # Ejecutar flujo RPA con validación completa
        resultado = rpa_service.generar_constancia_completa(
            nombre=data['nombre'],
            codigo=data['codigo'],
            carrera=data['carrera'],
            ciclo=data['ciclo'],
            dni=data.get('dni'),
            correo=correo
        )
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'mensaje': 'Constancia generada exitosamente con validación UNI',
                'archivo_pdf': resultado['archivo_pdf'],
                'registro_id': resultado['registro_id'],
                'datos_validados': resultado.get('datos_validados'),
                'validacion_uni': resultado.get('validacion_uni'),
                'estudiante_validado': resultado.get('validacion_uni', {}).get('success', False)
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error'),
                'validacion_uni': resultado.get('validacion_uni')
            }), 400
        
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

@app.route('/api/validar-estudiante', methods=['POST'])
def validar_estudiante():
    """Endpoint para validar estudiante en portal UNI antes de generar constancia"""
    try:
        data = request.json
        
        codigo = data.get('codigo')
        nombres = data.get('nombres')
        
        if not codigo:
            return jsonify({'error': 'Código de estudiante es requerido'}), 400
        
        # Log de la validación
        print(f"🔍 API: Validando estudiante {codigo}")
        
        # Validar en portal UNI con timeout extendido
        from uni_validation_service import validar_estudiante_uni
        resultado = validar_estudiante_uni(codigo, nombres)
        
        print(f"📋 API: Resultado validación: {resultado.get('success', False)}")
        
        # Respuesta detallada
        response_data = {
            'success': resultado.get('success', False),
            'datos_estudiante': resultado if resultado.get('success') else None,
            'error': resultado.get('error') if not resultado.get('success') else None,
            'mensaje': 'Estudiante validado correctamente' if resultado.get('success') else 'Estudiante no encontrado',
            'debug_info': {
                'codigo_buscado': codigo,
                'timestamp': datetime.now().isoformat(),
                'fuente': resultado.get('fuente', 'Portal UNI DIRCE')
            }
        }
        
        # Si hay información de debug, incluirla
        if 'debug_info' in resultado:
            response_data['debug_info']['detalles'] = resultado['debug_info']
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ API: Error validando estudiante: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}',
            'debug_info': {
                'timestamp': datetime.now().isoformat(),
                'error_type': type(e).__name__
            }
        }), 500

@app.route('/api/validar-dni', methods=['POST'])
def validar_dni():
    """Endpoint para validar DNI"""
    try:
        data = request.json
        
        dni = data.get('dni')
        
        if not dni:
            return jsonify({'error': 'DNI es requerido'}), 400
        
        if len(dni) != 8 or not dni.isdigit():
            return jsonify({'error': 'DNI debe tener exactamente 8 dígitos'}), 400
        
        # Log de la validación
        print(f"🆔 API: Validando DNI {dni}")
        
        # Validar DNI
        from dni_validation_service import validar_dni
        resultado = validar_dni(dni)
        
        print(f"📋 API: Resultado validación DNI: {resultado.get('success', False)}")
        
        return jsonify({
            'success': resultado.get('success', False),
            'datos_persona': resultado if resultado.get('success') else None,
            'error': resultado.get('error') if not resultado.get('success') else None,
            'mensaje': 'DNI validado correctamente' if resultado.get('success') else 'DNI no encontrado'
        })
        
    except Exception as e:
        print(f"❌ API: Error validando DNI: {e}")
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@app.route('/api/eliminar-constancia', methods=['DELETE'])
def eliminar_constancia():
    """Endpoint para eliminar constancia y su archivo PDF"""
    try:
        data = request.json
        
        registro_id = data.get('registro_id') or data.get('id')
        
        if not registro_id:
            return jsonify({'error': 'ID de registro es requerido'}), 400
        
        print(f"🗑️ API: Eliminando constancia {registro_id}")
        
        # Buscar la constancia antes de eliminar para obtener el archivo
        constancias = rpa_service.obtener_seguimiento()
        constancia = next((c for c in constancias if c.get('id') == registro_id), None)
        
        if not constancia:
            return jsonify({
                'success': False,
                'error': 'Constancia no encontrada'
            }), 404
        
        # Eliminar archivo PDF si existe
        pdf_filename = constancia.get('documento') or constancia.get('Documento')
        if pdf_filename:
            possible_paths = [
                os.path.join('autoridad_entrada', pdf_filename),
                os.path.join('PDFs', pdf_filename),
                os.path.join('constancias', pdf_filename)
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                        print(f"🗑️ Archivo PDF eliminado: {path}")
                        break
                    except Exception as e:
                        print(f"⚠️ Error eliminando archivo {path}: {e}")
        
        # Eliminar registro del seguimiento
        resultado = rpa_service.eliminar_constancia(registro_id)
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Constancia y archivo eliminados exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error eliminando registro de seguimiento'
            }), 500
        
    except Exception as e:
        print(f"❌ API: Error eliminando constancia: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

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

@app.route('/api/chat')
def get_chat_content():
    """Servir contenido del chat"""
    return render_template('chat.html')

@app.route('/api/configuracion-page')
def get_configuracion_content():
    """Servir contenido de configuración"""
    return render_template('configuracion.html')

@app.route('/api/constancias/descargar/<constancia_id>')
def descargar_constancia_endpoint(constancia_id):
    """Endpoint para descargar constancia por ID"""
    try:
        print(f"🔍 Buscando constancia para descargar: {constancia_id}")
        
        # Buscar la constancia en el seguimiento
        constancias = rpa_service.obtener_seguimiento()
        print(f"📋 Constancias disponibles: {len(constancias)}")
        
        constancia = None
        for c in constancias:
            if c.get('id') == constancia_id:
                constancia = c
                break
        
        if not constancia:
            print(f"❌ Constancia {constancia_id} no encontrada")
            return jsonify({'error': f'Constancia {constancia_id} no encontrada'}), 404
        
        print(f"✅ Constancia encontrada: {constancia}")
        
        # Buscar archivo PDF - múltiples estrategias
        pdf_filename = constancia.get('documento') or constancia.get('Documento')
        if not pdf_filename:
            print("❌ Nombre de archivo PDF no especificado")
            return jsonify({'error': 'Archivo PDF no especificado en registro'}), 404
        
        print(f"📄 Buscando archivo: {pdf_filename}")
        
        # Buscar en múltiples ubicaciones
        possible_paths = [
            os.path.join('autoridad_entrada', pdf_filename),
            os.path.join('PDFs', pdf_filename),
            os.path.join('constancias', pdf_filename),
            pdf_filename  # Ruta directa
        ]
        
        pdf_path = None
        for path in possible_paths:
            if os.path.exists(path):
                pdf_path = path
                print(f"✅ Archivo encontrado en: {path}")
                break
        
        if not pdf_path:
            print(f"❌ Archivo no encontrado en ninguna ubicación: {possible_paths}")
            return jsonify({
                'error': f'Archivo PDF no encontrado: {pdf_filename}',
                'searched_paths': possible_paths
            }), 404
        
        # Verificar que el archivo sea accesible
        try:
            file_size = os.path.getsize(pdf_path)
            print(f"📊 Tamaño del archivo: {file_size} bytes")
        except Exception as e:
            print(f"❌ Error accediendo al archivo: {e}")
            return jsonify({'error': f'Error accediendo al archivo: {str(e)}'}), 500
        
        print(f"🚀 Enviando archivo: {pdf_path}")
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=pdf_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"❌ Error en descarga: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/validar-uni', methods=['POST'])
def validar_uni():
    """Endpoint para validar código UNI"""
    try:
        data = request.json
        codigo = data.get('codigo')
        
        if not codigo:
            return jsonify({
                'success': False,
                'message': 'Código UNI es requerido'
            }), 400
        
        # Validar formato del código UNI (8 dígitos + 1 letra)
        import re
        if len(codigo) != 9 or not re.match(r'^\d{8}[A-Z]$', codigo):
            return jsonify({
                'success': False,
                'message': 'Código UNI debe tener 8 dígitos seguidos de una letra mayúscula (ej: 20220259H)'
            }), 400
        
        # Validar en portal UNI
        from uni_validation_service import validar_estudiante_uni
        resultado = validar_estudiante_uni(codigo)
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'data': {
                    'codigo': codigo,
                    'nombre': resultado.get('nombre', 'Estudiante UNI'),
                    'carrera': resultado.get('carrera', 'FIEE'),
                    'ciclo': resultado.get('ciclo', '2024-1')
                },
                'message': 'Código UNI válido'
            })
        else:
            return jsonify({
                'success': False,
                'message': resultado.get('error', 'Código UNI no encontrado')
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno: {str(e)}'
        }), 500

@app.route('/api/descargar-constancia/<constancia_id>')
def descargar_constancia_api(constancia_id):
    """API endpoint para descargar constancia"""
    return descargar_constancia_endpoint(constancia_id)

@app.route('/api/ver-constancia/<constancia_id>')
def ver_constancia(constancia_id):
    """Endpoint para ver constancia en el navegador"""
    try:
        # Buscar la constancia
        constancias = rpa_service.obtener_seguimiento()
        constancia = next((c for c in constancias if c.get('id') == constancia_id), None)
        
        if not constancia:
            return jsonify({
                'success': False,
                'error': 'Constancia no encontrada'
            }), 404
        
        # Generar URL para visualización
        pdf_filename = constancia.get('documento') or constancia.get('Documento')
        if pdf_filename:
            view_url = f'/api/constancias/descargar/{constancia_id}'
            return jsonify({
                'success': True,
                'url': view_url
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Archivo PDF no disponible'
            }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tramite-detalle/<tramite_id>')
def tramite_detalle(tramite_id):
    """Endpoint para obtener detalles de un trámite"""
    try:
        # Buscar el trámite
        constancias = rpa_service.obtener_seguimiento()
        tramite = next((c for c in constancias if c.get('id') == tramite_id), None)
        
        if not tramite:
            return jsonify({
                'success': False,
                'error': 'Trámite no encontrado'
            }), 404
        
        # Generar timeline simulado
        timeline = [
            {
                'title': 'Solicitud Recibida',
                'description': 'La solicitud ha sido recibida y está en cola de procesamiento',
                'date': '15/1/2024 10:30',
                'status': 'completed'
            },
            {
                'title': 'Validación de Datos',
                'description': 'Verificación de información del estudiante en el sistema UNI',
                'date': '15/1/2024 10:35',
                'status': 'completed'
            },
            {
                'title': 'Generación de Documento',
                'description': 'Documento generado automáticamente por el sistema RPA',
                'date': '15/1/2024 10:40',
                'status': 'completed'
            },
            {
                'title': 'Firma Digital',
                'description': 'Documento firmado digitalmente por la autoridad competente',
                'date': '15/1/2024 10:45',
                'status': 'completed'
            }
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'id': tramite_id,
                'estudiante': tramite.get('alumno', 'Estudiante'),
                'tipo': 'Constancia de Matrícula',
                'estado': 'Completado',
                'fecha': tramite.get('fecha', '15/1/2024'),
                'timeline': timeline
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Crear carpetas necesarias
    os.makedirs('autoridad_entrada', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Sistema Universitario RPA iniciado")
    print("📋 Accede a: http://localhost:5000")
    app.run(debug=True, port=5000)