// Sistema Universitario RPA - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Cargar seguimiento inicial
    cargarSeguimiento();
    
    // Configurar formulario
    document.getElementById('formConstancia').addEventListener('submit', generarConstancia);
});

async function generarConstancia(event) {
    event.preventDefault();
    
    const formData = {
        nombre: document.getElementById('nombre').value,
        codigo: document.getElementById('codigo').value,
        carrera: document.getElementById('carrera').value,
        ciclo: document.getElementById('ciclo').value
    };
    
    // Mostrar loading y logs
    const loadingSection = document.getElementById('loadingSection');
    const rpaLogs = document.getElementById('rpaLogs');
    loadingSection.style.display = 'block';
    rpaLogs.innerHTML = '';
    
    // Simular logs en tiempo real
    mostrarLogRPA('🔄 Iniciando flujo RPA...');
    mostrarLogRPA('🌐 Abriendo navegador para demostración...');
    
    try {
        const response = await fetch('/api/generar-constancia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarLogRPA('✅ Navegador abierto correctamente');
            mostrarLogRPA('✅ Búsqueda de constancia académica realizada');
            mostrarLogRPA('✅ Navegador cerrado correctamente');
            mostrarLogRPA(`✅ PDF generado: ${result.archivo_pdf}`);
            mostrarLogRPA('✅ Constancia enviada a autoridad');
            mostrarLogRPA('✅ Seguimiento actualizado en Excel');
            mostrarLogRPA('✅ Flujo RPA completado exitosamente');
            
            // Limpiar formulario
            document.getElementById('formConstancia').reset();
            
            // Actualizar seguimiento
            setTimeout(() => {
                cargarSeguimiento();
                loadingSection.style.display = 'none';
                mostrarNotificacion('Constancia generada exitosamente', 'success');
            }, 2000);
            
        } else {
            mostrarLogRPA(`❌ Error: ${result.error}`);
            mostrarNotificacion(result.error, 'error');
        }
        
    } catch (error) {
        mostrarLogRPA(`❌ Error de conexión: ${error.message}`);
        mostrarNotificacion('Error de conexión con el servidor', 'error');
        loadingSection.style.display = 'none';
    }
}

function mostrarLogRPA(mensaje) {
    const rpaLogs = document.getElementById('rpaLogs');
    const timestamp = new Date().toLocaleTimeString();
    rpaLogs.innerHTML += `[${timestamp}] ${mensaje}\n`;
    rpaLogs.scrollTop = rpaLogs.scrollHeight;
}

async function cargarSeguimiento() {
    try {
        const response = await fetch('/api/obtener-seguimiento');
        const result = await response.json();
        
        if (result.constancias) {
            mostrarTablaSeguimiento(result.constancias);
            actualizarEstadisticas(result.constancias);
        }
        
    } catch (error) {
        console.error('Error al cargar seguimiento:', error);
    }
}

function mostrarTablaSeguimiento(constancias) {
    const container = document.getElementById('tablaSeguimiento');
    
    if (constancias.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted">
                <i class="fas fa-inbox fa-2x"></i>
                <p>No hay constancias generadas</p>
            </div>
        `;
        return;
    }
    
    let html = `
        <div class="table-responsive">
            <table class="table table-sm">
                <thead class="table-dark">
                    <tr>
                        <th>Alumno</th>
                        <th>Documento</th>
                        <th>Estado</th>
                        <th>Autoridad</th>
                        <th>Firma</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    constancias.forEach(constancia => {
        const estadoBadge = getEstadoBadge(constancia.estado);
        const firmaBadge = getFirmaBadge(constancia.firma);
        const botonFirma = constancia.firma === 'Pendiente' ? 
            `<button class="btn btn-sm btn-outline-success" onclick="firmarConstancia('${constancia.id}')">
                <i class="fas fa-signature"></i> Firmar
            </button>` : 
            '<span class="text-success"><i class="fas fa-check"></i></span>';
        
        html += `
            <tr>
                <td><strong>${constancia.alumno}</strong><br><small>${constancia.codigo}</small></td>
                <td><small>${constancia.documento}</small></td>
                <td>${estadoBadge}</td>
                <td>${constancia.autoridad}</td>
                <td>${firmaBadge}</td>
                <td>${botonFirma}</td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

function getEstadoBadge(estado) {
    const badges = {
        'Enviado': 'badge bg-primary',
        'Firmado y Aprobado': 'badge bg-success'
    };
    const badgeClass = badges[estado] || 'badge bg-secondary';
    return `<span class="${badgeClass} status-badge">${estado}</span>`;
}

function getFirmaBadge(firma) {
    const badges = {
        'Pendiente': 'badge bg-warning text-dark',
        'Firmado': 'badge bg-success'
    };
    const badgeClass = badges[firma] || 'badge bg-secondary';
    return `<span class="${badgeClass} status-badge">${firma}</span>`;
}

async function firmarConstancia(registroId) {
    try {
        const response = await fetch('/api/firmar-constancia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ registro_id: registroId })
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarNotificacion('Constancia firmada exitosamente', 'success');
            cargarSeguimiento();
        } else {
            mostrarNotificacion(result.error, 'error');
        }
        
    } catch (error) {
        mostrarNotificacion('Error al firmar constancia', 'error');
    }
}

function actualizarEstadisticas(constancias) {
    const total = constancias.length;
    const pendientes = constancias.filter(c => c.firma === 'Pendiente').length;
    const firmadas = constancias.filter(c => c.firma === 'Firmado').length;
    
    document.getElementById('totalConstancias').textContent = total;
    document.getElementById('pendientesFirma').textContent = pendientes;
    document.getElementById('firmadas').textContent = firmadas;
}

function mostrarNotificacion(mensaje, tipo) {
    // Crear notificación temporal
    const alertClass = tipo === 'success' ? 'alert-success' : 'alert-danger';
    const icon = tipo === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
    
    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <i class="${icon}"></i> ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}