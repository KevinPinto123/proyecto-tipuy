// Configuración de Supabase
const supabaseUrl = 'https://ayydmyayghpdvgqhbyvr.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF5eWRteWF5Z2hwZHZncWhieXZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEyNTUyMzMsImV4cCI6MjA3NjgzMTIzM30.xAJ-Zm9yIC2VBPr3fiCToJXFxplffnya_7g7c-IxymI';
const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);

// Estado global
let currentUser = null;
let currentPage = 'chat';

// Variables globales para el estado de validación
let validationState = {
    dniValid: false,
    uniValid: false,
    dniData: null,
    uniData: null
};

// Inicialización
document.addEventListener('DOMContentLoaded', async function () {
    await checkAuth();
    loadChatPage();
    setupEventListeners();
});

// Verificar autenticación
async function checkAuth() {
    const user = localStorage.getItem('user');
    if (!user) {
        window.location.href = '/auth';
        return;
    }
    try {
        currentUser = JSON.parse(user);
        updateUserProfile();
    } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('user');
        window.location.href = '/auth';
    }
}

// Actualizar perfil de usuario
function updateUserProfile() {
    if (!currentUser) return;
    const userName = document.getElementById('userName');
    const userInitials = document.getElementById('userInitials');
    const fullName = currentUser.user_metadata?.full_name || currentUser.email;
    const initials = fullName.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);
    if (userName) userName.textContent = fullName;
    if (userInitials) userInitials.textContent = initials;
}

// Configurar event listeners
function setupEventListeners() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const page = this.dataset.page;
            if (page) {
                navigateToPage(page);
            }
        });
    });
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
}

// Navegación entre páginas
function navigateToPage(page) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`[data-page="${page}"]`).classList.add('active');
    currentPage = page;
    loadPageContent(page);
}

// Cargar contenido de página
async function loadPageContent(page) {
    const pageContent = document.getElementById('pageContent');
    try {
        let content = '';
        switch (page) {
            case 'chat':
                content = await loadChatPage();
                break;
            case 'dashboard-home':
                content = await loadDashboardHome();
                break;
            case 'tramites':
                content = await loadTramites();
                break;
            case 'notificaciones':
                content = await loadNotificaciones();
                break;
            case 'configuracion':
                content = await loadConfiguracion();
                break;
            default:
                content = '<div class="text-center p-5"><h3>Página no encontrada</h3></div>';
        }
        pageContent.innerHTML = content;

        // Cargar historial si es configuración
        if (page === 'configuracion') {
            setTimeout(() => {
                loadConstanciasHistory();
            }, 500);
        }
    } catch (error) {
        console.error('Error loading page:', error);
        pageContent.innerHTML = '<div class="alert alert-danger">Error cargando la página</div>';
    }
}

// Cargar página de chat
async function loadChatPage() {
    return `
        <div class="chat-container" style="height: calc(100vh - 120px); display: flex; flex-direction: column; background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); overflow: hidden;">
            <div class="chat-header" style="padding: 20px 24px; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; gap: 16px; background: white;">
                <div class="chat-avatar" style="width: 48px; height: 48px; background: #3b82f6; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="chat-info">
                    <h4 style="margin: 0; font-weight: 700; color: #1f2937;">TIPUY</h4>
                    <div class="status-indicator" style="display: flex; align-items: center; gap: 6px; font-size: 13px; color: #6b7280;">
                        <span class="status-dot" style="width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></span>
                        <span>En línea • IA Activa</span>
                    </div>
                </div>
            </div>
            
            <div class="chat-welcome" style="padding: 40px 24px; text-align: center; border-bottom: 1px solid #e2e8f0;">
                <h3 style="font-size: 24px; font-weight: 700; color: #1f2937; margin-bottom: 8px;">¿Qué necesitas hacer hoy?</h3>
                <p style="color: #6b7280; margin-bottom: 32px;">Selecciona una acción rápida para comenzar</p>
                
                <div class="quick-actions" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; max-width: 800px; margin: 0 auto;">
                    <div class="action-card" onclick="selectQuickAction('constancia')" style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; text-align: center; cursor: pointer; transition: all 0.2s;">
                        <div class="action-icon" style="width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-size: 20px; color: white; background: #3b82f6;">
                            <i class="fas fa-file-alt"></i>
                        </div>
                        <h5 style="font-weight: 600; color: #1f2937; margin-bottom: 4px;">Constancia de Matrícula</h5>
                        <p style="color: #6b7280; font-size: 14px; margin: 0;">Generar constancia oficial</p>
                    </div>
                    
                    <div class="action-card" onclick="selectQuickAction('certificado')" style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; text-align: center; cursor: pointer; transition: all 0.2s;">
                        <div class="action-icon" style="width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-size: 20px; color: white; background: #10b981;">
                            <i class="fas fa-certificate"></i>
                        </div>
                        <h5 style="font-weight: 600; color: #1f2937; margin-bottom: 4px;">Certificado de Notas</h5>
                        <p style="color: #6b7280; font-size: 14px; margin: 0;">Descargar certificado</p>
                    </div>
                    
                    <div class="action-card" onclick="selectQuickAction('estado')" style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; text-align: center; cursor: pointer; transition: all 0.2s;">
                        <div class="action-icon" style="width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-size: 20px; color: white; background: #f59e0b;">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <h5 style="font-weight: 600; color: #1f2937; margin-bottom: 4px;">Estado de Trámites</h5>
                        <p style="color: #6b7280; font-size: 14px; margin: 0;">Ver progreso actual</p>
                    </div>
                </div>
            </div>
            
            <div class="chat-messages" id="chatMessages" style="flex: 1; padding: 24px; overflow-y: auto; background: #fafbfc;">
                <div class="message bot-message" style="display: flex; gap: 12px; margin-bottom: 20px;">
                    <div class="message-avatar" style="width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; background: #3b82f6; color: white;">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content" style="flex: 1;">
                        <div class="message-text" style="background: white; padding: 12px 16px; border-radius: 12px; border: 1px solid #e2e8f0; line-height: 1.5;">
                            ¡Hola! Soy TIPUY, tu asistente virtual de la FIEE-UNI. 🎓
                            <br><br>
                            Estoy aquí para ayudarte con todos tus trámites académicos de forma rápida y eficiente. Mi inteligencia artificial está entrenada específicamente para resolver consultas universitarias.
                            <br><br>
                            💡 ¿En qué puedo asistirte hoy?
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="chat-input-container" style="padding: 20px 24px; border-top: 1px solid #e2e8f0; background: white;">
                <div class="chat-input" style="display: flex; align-items: center; gap: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 24px; padding: 8px 12px;">
                    <button class="btn-attachment" style="background: none; border: none; color: #6b7280; padding: 8px; border-radius: 50%; cursor: pointer;">
                        <i class="fas fa-paperclip"></i>
                    </button>
                    <input type="text" id="messageInput" placeholder="Escribe tu consulta aquí... (Ej: 'Necesito mi constancia de matrícula')" style="flex: 1; border: none; background: none; padding: 8px 12px; font-size: 14px; outline: none;">
                    <button class="btn-send" onclick="sendMessage()" style="background: #3b82f6; color: white; border: none; padding: 8px; border-radius: 50%; cursor: pointer; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
                <div class="security-notice" style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 12px; font-size: 12px; color: white; background: #dc2626; padding: 6px 12px; border-radius: 16px; width: fit-content; margin: 12px auto 0;">
                    <i class="fas fa-shield-alt"></i>
                    <span>Conexión segura • Cifrado extremo a extremo</span>
                </div>
            </div>
        </div>
    `;
}

// Cargar configuración con validaciones visibles
async function loadConfiguracion() {
    return `
        <div class="configuracion-page" style="max-width: 1200px; margin: 0 auto; padding: 20px;">
            <div class="page-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                <div style="display: flex; align-items: center; gap: 20px;">
                    <div class="header-icon" style="width: 80px; height: 80px; background: rgba(255,255,255,0.2); border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 36px;">
                        <i class="fas fa-cogs"></i>
                    </div>
                    <div>
                        <h1 style="margin: 0; font-size: 32px; font-weight: 700;">Centro de Validaciones</h1>
                        <p style="margin: 8px 0 0; font-size: 18px; opacity: 0.9;">Valida DNI y Código UNI para generar constancias oficiales</p>
                    </div>
                </div>
            </div>

            <div class="validation-form" style="background: white; border-radius: 20px; padding: 40px; margin-bottom: 30px; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 40px;">
                    <h2 style="color: #1f2937; font-size: 28px; margin-bottom: 10px;">🔐 Validación de Identidad</h2>
                    <p style="color: #6b7280; font-size: 16px;">Completa los datos para verificar tu identidad y generar constancias</p>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px;">
                    <div class="validation-card" style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); padding: 30px; border-radius: 16px; color: white;">
                        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                            <div style="width: 50px; height: 50px; background: rgba(255,255,255,0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                                <i class="fas fa-id-card"></i>
                            </div>
                            <div>
                                <h3 style="margin: 0; font-size: 20px;">Validación DNI</h3>
                                <p style="margin: 0; opacity: 0.9; font-size: 14px;">Verificación con RENIEC</p>
                            </div>
                        </div>
                        
                        <div class="input-group" style="margin-bottom: 20px;">
                            <input type="text" id="validationDNI" placeholder="Ingresa tu DNI (8 dígitos)" maxlength="8" 
                                   style="width: 100%; padding: 15px; border: none; border-radius: 12px; font-size: 16px; background: rgba(255,255,255,0.9); color: #1f2937;">
                        </div>
                        
                        <button onclick="validateDNI()" class="btn-validate" 
                                style="width: 100%; padding: 15px; background: rgba(255,255,255,0.2); border: 2px solid rgba(255,255,255,0.3); color: white; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.3s;">
                            <i class="fas fa-search"></i> Validar DNI
                        </button>
                        
                        <div id="dniResult" class="validation-result" style="margin-top: 15px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px; display: none;">
                            <div class="result-content"></div>
                        </div>
                    </div>

                    <div class="validation-card" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 30px; border-radius: 16px; color: #1f2937;">
                        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                            <div style="width: 50px; height: 50px; background: rgba(255,255,255,0.7); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; color: #3b82f6;">
                                <i class="fas fa-university"></i>
                            </div>
                            <div>
                                <h3 style="margin: 0; font-size: 20px;">Validación UNI</h3>
                                <p style="margin: 0; opacity: 0.8; font-size: 14px;">Portal Institucional</p>
                            </div>
                        </div>
                        
                        <div class="input-group" style="margin-bottom: 20px;">
                            <input type="text" id="validationUNI" placeholder="Código de estudiante (ej: 20220259H)" maxlength="9" 
                                   style="width: 100%; padding: 15px; border: none; border-radius: 12px; font-size: 16px; background: rgba(255,255,255,0.9);">
                        </div>
                        
                        <button onclick="validateUNI()" class="btn-validate" 
                                style="width: 100%; padding: 15px; background: #3b82f6; border: none; color: white; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.3s;">
                            <i class="fas fa-graduation-cap"></i> Validar Código UNI
                        </button>
                        
                        <div id="uniResult" class="validation-result" style="margin-top: 15px; padding: 15px; background: rgba(255,255,255,0.7); border-radius: 8px; display: none;">
                            <div class="result-content"></div>
                        </div>
                    </div>
                </div>

                <div class="validation-status" style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 25px; border-radius: 16px; margin-bottom: 30px;">
                    <h4 style="margin: 0 0 15px; color: #1f2937; display: flex; align-items: center; gap: 10px;">
                        <i class="fas fa-shield-check"></i> Estado de Validación
                    </h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
                        <div class="status-item" id="statusDNI" style="display: flex; align-items: center; gap: 10px; padding: 15px; background: rgba(255,255,255,0.7); border-radius: 12px;">
                            <i class="fas fa-times-circle" style="color: #ef4444; font-size: 20px;"></i>
                            <span style="font-weight: 500;">DNI Pendiente</span>
                        </div>
                        <div class="status-item" id="statusUNI" style="display: flex; align-items: center; gap: 10px; padding: 15px; background: rgba(255,255,255,0.7); border-radius: 12px;">
                            <i class="fas fa-times-circle" style="color: #ef4444; font-size: 20px;"></i>
                            <span style="font-weight: 500;">UNI Pendiente</span>
                        </div>
                        <div class="status-item" id="statusGeneral" style="display: flex; align-items: center; gap: 10px; padding: 15px; background: rgba(255,255,255,0.7); border-radius: 12px;">
                            <i class="fas fa-clock" style="color: #f59e0b; font-size: 20px;"></i>
                            <span style="font-weight: 500;">Esperando Validación</span>
                        </div>
                    </div>
                </div>

                <div class="generator-section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 16px; color: white;">
                    <h4 style="margin: 0 0 20px; display: flex; align-items: center; gap: 10px; font-size: 22px;">
                        <i class="fas fa-magic"></i> Generador de Constancias RPA
                    </h4>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px;">
                        <div>
                            <label style="display: block; margin-bottom: 8px; font-weight: 500;">Carrera:</label>
                            <select id="generatorCarrera" style="width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 14px;">
                                <option value="">Seleccionar carrera</option>
                                <option value="Ingeniería Eléctrica">Ingeniería Eléctrica</option>
                                <option value="Ingeniería Electrónica">Ingeniería Electrónica</option>
                                <option value="Ingeniería de Telecomunicaciones">Ingeniería de Telecomunicaciones</option>
                                <option value="Ingeniería de Ciberseguridad">Ingeniería de Ciberseguridad</option>
                            </select>
                        </div>
                        <div>
                            <label style="display: block; margin-bottom: 8px; font-weight: 500;">Ciclo Académico:</label>
                            <select id="generatorCiclo" style="width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 14px;">
                                <option value="">Seleccionar ciclo</option>
                                <option value="2024-1">2024-1</option>
                                <option value="2024-2">2024-2</option>
                                <option value="2025-1">2025-1</option>
                            </select>
                        </div>
                    </div>
                    
                    <div style="text-align: center;">
                        <button id="btnGenerateConstancia" onclick="generateConstanciaComplete()" disabled
                                style="padding: 15px 40px; background: rgba(255,255,255,0.2); border: 2px solid rgba(255,255,255,0.3); color: white; border-radius: 12px; font-size: 18px; font-weight: 600; cursor: not-allowed; transition: all 0.3s;">
                            <i class="fas fa-lock"></i> Validar Datos Primero
                        </button>
                        <p style="margin: 10px 0 0; font-size: 14px; opacity: 0.8;">* Completa las validaciones DNI y UNI para habilitar</p>
                    </div>
                </div>
            </div>

            <div class="history-section" style="background: white; border-radius: 20px; padding: 30px; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                    <h3 style="margin: 0; color: #1f2937; display: flex; align-items: center; gap: 10px;">
                        <i class="fas fa-history"></i> Mis Constancias Generadas
                    </h3>
                    <button onclick="loadConstanciasHistory()" style="padding: 10px 20px; background: #3b82f6; color: white; border: none; border-radius: 8px; cursor: pointer;">
                        <i class="fas fa-sync"></i> Actualizar
                    </button>
                </div>
                
                <div id="constanciasHistory" style="min-height: 200px;">
                    <div style="text-align: center; padding: 60px; color: #6b7280;">
                        <i class="fas fa-file-alt" style="font-size: 48px; margin-bottom: 15px; opacity: 0.5;"></i>
                        <p style="font-size: 16px;">Cargando historial de constancias...</p>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Funciones de validación
async function validateDNI() {
    const dniInput = document.getElementById('validationDNI');
    const resultDiv = document.getElementById('dniResult');
    const statusDiv = document.getElementById('statusDNI');

    if (!dniInput || !dniInput.value) {
        showNotification('Por favor ingresa un DNI', 'warning');
        return;
    }

    const dni = dniInput.value.trim();

    if (dni.length !== 8 || !/^\d+$/.test(dni)) {
        showNotification('El DNI debe tener exactamente 8 dígitos', 'error');
        return;
    }

    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
        <div style="text-align: center; color: white;">
            <i class="fas fa-spinner fa-spin" style="font-size: 20px; margin-bottom: 10px;"></i>
            <p style="margin: 0;">Validando DNI en RENIEC...</p>
        </div>
    `;

    try {
        const response = await fetch('/api/validar-dni', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dni: dni })
        });

        const result = await response.json();

        if (result.success && result.datos_persona) {
            validationState.dniValid = true;
            validationState.dniData = result.datos_persona;

            resultDiv.className = 'validation-result success';
            resultDiv.innerHTML = `
                <div style="color: #065f46;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <i class="fas fa-check-circle" style="color: #10b981; font-size: 20px;"></i>
                        <strong>DNI Validado Correctamente</strong>
                    </div>
                    <p style="margin: 5px 0;"><strong>Nombre:</strong> ${result.datos_persona.nombre_completo}</p>
                    <p style="margin: 5px 0;"><strong>DNI:</strong> ${dni}</p>
                    <small style="opacity: 0.8;">✓ Verificado con RENIEC</small>
                </div>
            `;

            statusDiv.innerHTML = `
                <i class="fas fa-check-circle" style="color: #10b981; font-size: 20px;"></i>
                <span style="font-weight: 500; color: #065f46;">DNI Validado</span>
            `;

            showNotification('✅ DNI validado correctamente', 'success');

        } else {
            validationState.dniValid = false;
            validationState.dniData = null;

            resultDiv.className = 'validation-result error';
            resultDiv.innerHTML = `
                <div style="color: #991b1b;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <i class="fas fa-exclamation-circle" style="color: #ef4444; font-size: 20px;"></i>
                        <strong>Error en Validación</strong>
                    </div>
                    <p style="margin: 0;">${result.error || 'DNI no encontrado en RENIEC'}</p>
                </div>
            `;

            showNotification('❌ Error validando DNI', 'error');
        }

    } catch (error) {
        validationState.dniValid = false;
        resultDiv.className = 'validation-result error';
        resultDiv.innerHTML = `
            <div style="color: #991b1b;">
                <i class="fas fa-exclamation-triangle"></i>
                <p style="margin: 0;">Error de conexión. Intenta nuevamente.</p>
            </div>
        `;
        showNotification('Error de conexión', 'error');
    }

    updateGeneratorButton();
}

async function validateUNI() {
    const uniInput = document.getElementById('validationUNI');
    const resultDiv = document.getElementById('uniResult');
    const statusDiv = document.getElementById('statusUNI');

    if (!uniInput || !uniInput.value) {
        showNotification('Por favor ingresa un código UNI', 'warning');
        return;
    }

    const codigo = uniInput.value.trim();

    if (codigo.length !== 9 || !/^\d{8}[A-Z]$/.test(codigo)) {
        showNotification('El código UNI debe tener 8 dígitos seguidos de una letra mayúscula (ej: 20220259H)', 'error');
        return;
    }

    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
        <div style="text-align: center; color: #1f2937;">
            <i class="fas fa-spinner fa-spin" style="font-size: 20px; margin-bottom: 10px;"></i>
            <p style="margin: 0;">Validando en Portal UNI...</p>
        </div>
    `;

    try {
        const response = await fetch('/api/validar-uni', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo: codigo })
        });

        const result = await response.json();

        if (result.success && result.data) {
            validationState.uniValid = true;
            validationState.uniData = result.data;

            resultDiv.className = 'validation-result success';
            resultDiv.innerHTML = `
                <div style="color: #065f46;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <i class="fas fa-check-circle" style="color: #10b981; font-size: 20px;"></i>
                        <strong>Estudiante UNI Validado</strong>
                    </div>
                    <p style="margin: 5px 0;"><strong>Nombre:</strong> ${result.data.nombre}</p>
                    <p style="margin: 5px 0;"><strong>Código:</strong> ${codigo}</p>
                    <p style="margin: 5px 0;"><strong>Carrera:</strong> ${result.data.carrera}</p>
                    <small style="opacity: 0.8;">✓ Verificado en Portal UNI</small>
                </div>
            `;

            statusDiv.innerHTML = `
                <i class="fas fa-check-circle" style="color: #10b981; font-size: 20px;"></i>
                <span style="font-weight: 500; color: #065f46;">UNI Validado</span>
            `;

            const carreraSelect = document.getElementById('generatorCarrera');
            if (carreraSelect && result.data.carrera) {
                const options = carreraSelect.options;
                for (let i = 0; i < options.length; i++) {
                    if (options[i].value.includes(result.data.carrera) || result.data.carrera.includes(options[i].value)) {
                        carreraSelect.selectedIndex = i;
                        break;
                    }
                }
            }

            showNotification('✅ Código UNI validado correctamente', 'success');

        } else {
            validationState.uniValid = false;
            validationState.uniData = null;

            resultDiv.className = 'validation-result error';
            resultDiv.innerHTML = `
                <div style="color: #991b1b;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <i class="fas fa-exclamation-circle" style="color: #ef4444; font-size: 20px;"></i>
                        <strong>Error en Validación</strong>
                    </div>
                    <p style="margin: 0;">${result.message || 'Código no encontrado en Portal UNI'}</p>
                </div>
            `;

            showNotification('❌ Error validando código UNI', 'error');
        }

    } catch (error) {
        validationState.uniValid = false;
        resultDiv.className = 'validation-result error';
        resultDiv.innerHTML = `
            <div style="color: #991b1b;">
                <i class="fas fa-exclamation-triangle"></i>
                <p style="margin: 0;">Error de conexión. Intenta nuevamente.</p>
            </div>
        `;
        showNotification('Error de conexión', 'error');
    }

    updateGeneratorButton();
}

function updateGeneratorButton() {
    const button = document.getElementById('btnGenerateConstancia');
    const statusGeneral = document.getElementById('statusGeneral');

    if (!button || !statusGeneral) return;

    if (validationState.dniValid && validationState.uniValid) {
        button.disabled = false;
        button.style.cursor = 'pointer';
        button.style.background = 'rgba(16, 185, 129, 0.9)';
        button.style.borderColor = 'rgba(16, 185, 129, 0.9)';
        button.innerHTML = '<i class="fas fa-magic"></i> Generar Constancia RPA';

        statusGeneral.innerHTML = `
            <i class="fas fa-check-circle" style="color: #10b981; font-size: 20px;"></i>
            <span style="font-weight: 500; color: #065f46;">Listo para Generar</span>
        `;

        showNotification('🎉 ¡Validaciones completadas! Ya puedes generar tu constancia', 'success');

    } else if (validationState.dniValid || validationState.uniValid) {
        statusGeneral.innerHTML = `
            <i class="fas fa-clock" style="color: #f59e0b; font-size: 20px;"></i>
            <span style="font-weight: 500;">Validación Parcial</span>
        `;
    }
}

async function generateConstanciaComplete() {
    if (!validationState.dniValid || !validationState.uniValid) {
        showNotification('Completa las validaciones DNI y UNI primero', 'warning');
        return;
    }

    const carrera = document.getElementById('generatorCarrera')?.value;
    const ciclo = document.getElementById('generatorCiclo')?.value;

    if (!carrera || !ciclo) {
        showNotification('Selecciona carrera y ciclo académico', 'warning');
        return;
    }

    const button = document.getElementById('btnGenerateConstancia');
    const originalText = button.innerHTML;

    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generando Constancia...';

    try {
        const requestData = {
            nombre: validationState.dniData.nombre_completo,
            codigo: validationState.uniData.codigo,
            dni: validationState.dniData.dni || document.getElementById('validationDNI').value,
            carrera: carrera,
            ciclo: ciclo,
            correo: `${validationState.uniData.codigo}@uni.pe`
        };

        const response = await fetch('/api/generar-constancia', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();

        if (result.success) {
            showNotification('🎉 ¡Constancia generada exitosamente!', 'success');

            const modalContent = `
                <div style="text-align: center; padding: 20px;">
                    <div style="width: 80px; height: 80px; background: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; color: white; font-size: 36px;">
                        <i class="fas fa-check"></i>
                    </div>
                    <h3 style="color: #1f2937; margin-bottom: 15px;">¡Constancia Generada!</h3>
                    <p style="color: #6b7280; margin-bottom: 25px;">Tu constancia de matrícula ha sido generada exitosamente con validación completa DNI + UNI.</p>
                    
                    <div style="background: #f8fafc; padding: 20px; border-radius: 12px; margin-bottom: 25px; text-align: left;">
                        <h5 style="margin: 0 0 10px; color: #1f2937;">Detalles del Documento:</h5>
                        <p style="margin: 5px 0;"><strong>Estudiante:</strong> ${requestData.nombre}</p>
                        <p style="margin: 5px 0;"><strong>Código:</strong> ${requestData.codigo}</p>
                        <p style="margin: 5px 0;"><strong>Carrera:</strong> ${requestData.carrera}</p>
                        <p style="margin: 5px 0;"><strong>Ciclo:</strong> ${requestData.ciclo}</p>
                    </div>
                    
                    <div style="display: flex; gap: 15px; justify-content: center;">
                        <button onclick="loadConstanciasHistory(); closeModal();" style="padding: 12px 24px; background: #3b82f6; color: white; border: none; border-radius: 8px; cursor: pointer;">
                            <i class="fas fa-list"></i> Ver Historial
                        </button>
                        <button onclick="closeModal();" style="padding: 12px 24px; background: #6b7280; color: white; border: none; border-radius: 8px; cursor: pointer;">
                            <i class="fas fa-times"></i> Cerrar
                        </button>
                    </div>
                </div>
            `;

            showModal('Constancia Generada', modalContent);

            setTimeout(() => {
                loadConstanciasHistory();
            }, 1000);

        } else {
            showNotification(`❌ Error: ${result.error}`, 'error');
        }

    } catch (error) {
        showNotification('Error generando constancia', 'error');
        console.error('Error:', error);
    } finally {
        button.disabled = false;
        button.innerHTML = originalText;
    }
}

async function loadConstanciasHistory() {
    const historyDiv = document.getElementById('constanciasHistory');
    if (!historyDiv) return;

    historyDiv.innerHTML = `
        <div style="text-align: center; padding: 40px; color: #6b7280;">
            <i class="fas fa-spinner fa-spin" style="font-size: 32px; margin-bottom: 15px;"></i>
            <p>Cargando constancias...</p>
        </div>
    `;

    try {
        const response = await fetch('/api/obtener-seguimiento');
        const result = await response.json();

        if (result.constancias && result.constancias.length > 0) {
            let html = '<div style="display: grid; gap: 15px;">';

            result.constancias.forEach((constancia, index) => {
                const gradientColors = [
                    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
                ];

                const gradient = gradientColors[index % gradientColors.length];

                html += `
                    <div style="background: ${gradient}; padding: 25px; border-radius: 16px; color: white; display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <h5 style="margin: 0 0 8px; font-size: 18px; font-weight: 600;">${constancia.documento || 'Constancia de Matrícula'}</h5>
                            <p style="margin: 0 0 5px; opacity: 0.9;">${constancia.alumno}</p>
                            <small style="opacity: 0.8;">📅 ${constancia.fecha || 'Fecha no disponible'} • 🆔 ${constancia.codigo || 'N/A'}</small>
                        </div>
                        <div style="display: flex; gap: 10px;">
                            <button onclick="downloadConstanciaFromHistory('${constancia.id}')" 
                                    style="padding: 10px 15px; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); color: white; border-radius: 8px; cursor: pointer; transition: all 0.3s;">
                                <i class="fas fa-download"></i> Descargar
                            </button>
                            <button onclick="viewConstanciaDetails('${constancia.id}')" 
                                    style="padding: 10px 15px; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); color: white; border-radius: 8px; cursor: pointer; transition: all 0.3s;">
                                <i class="fas fa-eye"></i> Ver
                            </button>
                        </div>
                    </div>
                `;
            });

            html += '</div>';
            historyDiv.innerHTML = html;

        } else {
            historyDiv.innerHTML = `
                <div style="text-align: center; padding: 60px; color: #6b7280;">
                    <i class="fas fa-file-alt" style="font-size: 48px; margin-bottom: 15px; opacity: 0.5;"></i>
                    <h4 style="margin: 0 0 10px;">No hay constancias generadas</h4>
                    <p style="margin: 0;">Completa las validaciones y genera tu primera constancia</p>
                </div>
            `;
        }

    } catch (error) {
        historyDiv.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #ef4444;">
                <i class="fas fa-exclamation-triangle" style="font-size: 32px; margin-bottom: 15px;"></i>
                <p>Error cargando el historial</p>
            </div>
        `;
    }
}

// Funciones de chat
function sendMessage() {
    const input = document.getElementById('messageInput');
    if (!input || !input.value.trim()) return;

    const message = input.value.trim();
    input.value = '';

    addMessage(message, 'user');

    setTimeout(() => {
        const botResponse = generateBotResponse(message);
        addMessage(botResponse, 'bot');
    }, 1000);
}

function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-text">${text}</div>
        </div>
    `;

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function generateBotResponse(userMessage) {
    const message = userMessage.toLowerCase();

    if (message.includes('constancia')) {
        return `¡Perfecto! Te ayudo con tu constancia de matrícula. 📄
                <br><br>
                Para generar tu constancia necesito que:
                <br>
                1. Verifiques que tus datos estén actualizados en Configuración
                <br>
                2. Confirmes tu información personal
                <br><br>
                ¿Quieres que inicie el proceso ahora?`;
    }

    if (message.includes('notas') || message.includes('certificado')) {
        return `Te ayudo con tu certificado de notas. 📊
                <br><br>
                Puedo generar certificados de:
                <br>
                • Notas parciales del ciclo actual
                <br>
                • Historial académico completo
                <br>
                • Ranking académico
                <br><br>
                ¿Cuál necesitas?`;
    }

    return `Entiendo tu consulta. Como asistente virtual de la FIEE-UNI, puedo ayudarte con:
            <br><br>
            📄 Constancias de matrícula
            <br>
            📊 Certificados de notas
            <br>
            🚪 Retiros de curso
            <br>
            📅 Agendar citas
            <br>
            ❓ Consultas generales
            <br><br>
            ¿Con cuál de estos te gustaría que te ayude?`;
}

function selectQuickAction(action) {
    const actions = {
        'constancia': 'Necesito generar mi constancia de matrícula',
        'certificado': 'Quiero descargar mi certificado de notas',
        'retiro': 'Necesito hacer un retiro de curso',
        'estado': 'Quiero ver el estado de mis trámites',
        'consulta': 'Tengo una consulta general',
        'cita': 'Quiero agendar una cita'
    };

    const message = actions[action] || 'Hola, necesito ayuda';

    const input = document.getElementById('messageInput');
    if (input) {
        input.value = message;
        sendMessage();
    }
}

// Funciones de utilidad
async function generateConstancia() {
    navigateToPage('configuracion');
    showNotification('Redirigiendo al generador de constancias...', 'info');
}

async function downloadConstancias() {
    try {
        const response = await fetch('/api/obtener-seguimiento');
        const result = await response.json();

        if (result.constancias && result.constancias.length > 0) {
            let downloadList = '<div class="download-modal"><h4>Constancias Disponibles</h4><ul>';

            result.constancias.forEach(constancia => {
                downloadList += `
                    <li>
                        <span>${constancia.alumno} - ${constancia.documento}</span>
                        <button onclick="downloadSingleConstancia('${constancia.id}')" class="btn-sm btn-primary">
                            <i class="fas fa-download"></i> Descargar
                        </button>
                    </li>
                `;
            });

            downloadList += '</ul></div>';

            showModal('Descargar Constancias', downloadList);
        } else {
            showNotification('No hay constancias disponibles para descargar', 'warning');
        }
    } catch (error) {
        showNotification('Error al obtener constancias', 'error');
    }
}

async function downloadConstanciaFromHistory(id) {
    try {
        showNotification('Descargando constancia...', 'info');

        const response = await fetch(`/api/descargar-constancia/${id}`);

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `constancia_${id}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            showNotification('✅ Constancia descargada exitosamente', 'success');
        } else {
            showNotification('❌ Error al descargar la constancia', 'error');
        }
    } catch (error) {
        showNotification('Error en la descarga', 'error');
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

async function logout() {
    try {
        localStorage.removeItem('user');
        window.location.href = '/auth';
    } catch (error) {
        console.error('Error logging out:', error);
    }
}

function closeModal() {
    const modal = document.querySelector('.modal-overlay');
    if (modal) {
        modal.remove();
    }
}

// Sistema de notificaciones mejorado
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;

    const icons = {
        'info': 'fas fa-info-circle',
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-circle',
        'warning': 'fas fa-exclamation-triangle'
    };

    const colors = {
        'info': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'success': 'linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%)',
        'error': 'linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%)',
        'warning': 'linear-gradient(135deg, #f7971e 0%, #ffd200 100%)'
    };

    notification.innerHTML = `
        <div class="notification-content" style="display: flex; align-items: center; gap: 15px;">
            <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px;">
                <i class="${icons[type]}"></i>
            </div>
            <div style="flex: 1; color: white;">
                <p style="margin: 0; font-weight: 500; font-size: 14px;">${message}</p>
            </div>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()" style="position: absolute; top: 10px; right: 10px; background: none; border: none; color: rgba(255,255,255,0.8); cursor: pointer; font-size: 16px;">
            <i class="fas fa-times"></i>
        </button>
    `;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type]};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 1000;
        min-width: 350px;
        max-width: 400px;
        animation: slideInRight 0.4s ease;
        backdrop-filter: blur(10px);
    `;

    if (!document.getElementById('notification-animations')) {
        const styles = document.createElement('style');
        styles.id = 'notification-animations';
        styles.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            .notification:hover {
                transform: translateY(-2px);
                transition: transform 0.2s ease;
            }
        `;
        document.head.appendChild(styles);
    }

    document.body.appendChild(notification);

    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideInRight 0.4s ease reverse';
            setTimeout(() => notification.remove(), 400);
        }
    }, 5000);
}

// Sistema de modales mejorado
function showModal(title, content) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-container" style="background: white; border-radius: 20px; max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto; animation: modalSlideUp 0.4s ease; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
            <div class="modal-header" style="padding: 25px 30px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 20px 20px 0 0;">
                <h4 style="margin: 0; font-size: 20px; font-weight: 600;">${title}</h4>
                <button class="modal-close" onclick="closeModal()" style="background: rgba(255,255,255,0.2); border: none; color: white; cursor: pointer; font-size: 18px; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
        </div>
    `;

    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        animation: fadeIn 0.4s ease;
        backdrop-filter: blur(5px);
    `;

    if (!document.getElementById('modal-animations')) {
        const styles = document.createElement('style');
        styles.id = 'modal-animations';
        styles.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes modalSlideUp {
                from { transform: translateY(50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        `;
        document.head.appendChild(styles);
    }

    document.body.appendChild(modal);

    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            closeModal();
        }
    });
}

// Responsive
window.addEventListener('resize', function () {
    if (window.innerWidth <= 768) {
        const sidebar = document.getElementById('sidebar');
        sidebar.classList.remove('open');
    }
});

// Cargar páginas adicionales (simplificadas para evitar errores)
async function loadDashboardHome() {
    return `<div style="padding: 40px; text-align: center;"><h2>Dashboard Principal</h2><p>Bienvenido al sistema TIPUY</p></div>`;
}

async function loadTramites() {
    return `<div style="padding: 40px; text-align: center;"><h2>Gestión de Trámites</h2><p>Administra tus solicitudes</p></div>`;
}

async function loadNotificaciones() {
    return `<div style="padding: 40px; text-align: center;"><h2>Notificaciones</h2><p>Centro de notificaciones</p></div>`;
}