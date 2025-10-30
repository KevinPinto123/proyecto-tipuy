// Datos de demostración para el sistema RPA universitario
window.demoData = {
    // Datos de estudiantes para validación UNI
    estudiantes: {
        '20210001A': {
            codigo: '20210001A',
            nombre: 'Juan Carlos Pérez Rodríguez',
            carrera: 'Ingeniería Eléctrica',
            ciclo: '2024-1',
            estado: 'Activo',
            correo: 'juan.perez@uni.pe'
        },
        '20210002B': {
            codigo: '20210002B',
            nombre: 'María García López',
            carrera: 'Ingeniería Electrónica',
            ciclo: '2024-1',
            estado: 'Activo',
            correo: 'maria.garcia@uni.pe'
        },
        '20220259H': {
            codigo: '20220259H',
            nombre: 'Kevin Eduardo Pinto Acevedo',
            carrera: 'Ingeniería de Telecomunicaciones',
            ciclo: '2024-1',
            estado: 'Activo',
            correo: 'kevin.pinto@uni.pe'
        },
        '20230001C': {
            codigo: '20230001C',
            nombre: 'Ana Sofía Mendoza Torres',
            carrera: 'Ingeniería de Ciberseguridad',
            ciclo: '2024-1',
            estado: 'Activo',
            correo: 'ana.mendoza@uni.pe'
        }
    },
    
    // Datos de DNI para validación
    dnis: {
        '12345678': {
            dni: '12345678',
            nombre_completo: 'Juan Carlos Pérez Rodríguez',
            fecha_nacimiento: '15/03/1998',
            estado: 'Válido'
        },
        '87654321': {
            dni: '87654321',
            nombre_completo: 'María García López',
            fecha_nacimiento: '22/07/1999',
            estado: 'Válido'
        },
        '77804421': {
            dni: '77804421',
            nombre_completo: 'Kevin Eduardo Pinto Acevedo',
            fecha_nacimiento: '10/12/2000',
            estado: 'Válido'
        },
        '11223344': {
            dni: '11223344',
            nombre_completo: 'Ana Sofía Mendoza Torres',
            fecha_nacimiento: '05/09/2001',
            estado: 'Válido'
        }
    },
    
    // Constancias generadas (simuladas)
    constancias: [
        {
            id: '4b8e37ed',
            alumno: 'Juan Carlos Pérez Rodríguez',
            codigo: '20210001A',
            documento: 'Constancia_Matricula_20210001A.pdf',
            fecha: '15/1/2024',
            estado: 'Completado',
            tipo: 'Constancia de Matrícula'
        },
        {
            id: '7c9f28ae',
            alumno: 'María García López',
            codigo: '20210002B',
            documento: 'Constancia_Matricula_20210002B.pdf',
            fecha: '14/1/2024',
            estado: 'Completado',
            tipo: 'Constancia de Matrícula'
        },
        {
            id: 'a1b2c3d4',
            alumno: 'Kevin Eduardo Pinto Acevedo',
            codigo: '20220259H',
            documento: 'Constancia_Matricula_20220259H.pdf',
            fecha: '13/1/2024',
            estado: 'Completado',
            tipo: 'Constancia de Matrícula'
        }
    ],
    
    // Configuración del sistema
    config: {
        universidad: 'Universidad Nacional de Ingeniería',
        facultad: 'Facultad de Ingeniería Eléctrica y Electrónica',
        ciclo_actual: '2024-1',
        autoridad_firma: 'Dr. Carlos Rodríguez Mendoza',
        cargo_autoridad: 'Decano de la FIEE',
        version_sistema: '2.1.0'
    },
    
    // Mensajes del chatbot TIPUY
    chatResponses: {
        'constancia': [
            '¡Perfecto! Te ayudo con tu constancia de matrícula. 📄',
            'Para generar tu constancia necesito que:',
            '1. Verifiques que tus datos estén actualizados en Configuración',
            '2. Confirmes tu información personal',
            '¿Quieres que inicie el proceso ahora?'
        ],
        'certificado': [
            'Te ayudo con tu certificado de notas. 📊',
            'Puedo generar certificados de:',
            '• Notas parciales del ciclo actual',
            '• Historial académico completo',
            '• Ranking académico',
            '¿Cuál necesitas?'
        ],
        'retiro': [
            'Entiendo que necesitas hacer un retiro de curso. 📝',
            'Para procesar tu solicitud de retiro necesito:',
            '• Código del curso a retirar',
            '• Motivo del retiro',
            '• Confirmación de que entiendes las implicaciones académicas',
            '¿Tienes esta información lista?'
        ],
        'estado': [
            'Te muestro el estado de tus trámites actuales. 📋',
            'Según mi consulta al sistema:',
            '• Tienes 2 solicitudes completadas',
            '• 1 solicitud en proceso de revisión',
            '• 0 solicitudes pendientes de documentación',
            '¿Quieres ver los detalles de alguna en particular?'
        ],
        'default': [
            'Entiendo tu consulta. Como asistente virtual de la FIEE-UNI, puedo ayudarte con:',
            '📄 Constancias de matrícula',
            '📊 Certificados de notas',
            '🚪 Retiros de curso',
            '📅 Agendar citas',
            '❓ Consultas generales',
            '¿Con cuál de estos te gustaría que te ayude?'
        ]
    }
};

// Función para obtener datos de demostración
window.getDemoData = function(type, key) {
    if (!window.demoData[type]) return null;
    if (key) {
        return window.demoData[type][key] || null;
    }
    return window.demoData[type];
};

// Función para simular delay de red
window.simulateNetworkDelay = function(min = 500, max = 1500) {
    const delay = Math.random() * (max - min) + min;
    return new Promise(resolve => setTimeout(resolve, delay));
};

console.log('📊 Datos de demostración cargados correctamente');