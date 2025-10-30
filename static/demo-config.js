// Configuración de demo para TIPUY
// Permite que el sistema funcione sin Supabase real

// Mock de autenticación
window.mockAuth = {
    currentUser: null,
    
    login: function(email, password) {
        if (email && password) {
            this.currentUser = {
                id: '123',
                email: email,
                user_metadata: {
                    full_name: email.split('@')[0].replace('.', ' ').toUpperCase()
                }
            };
            localStorage.setItem('user', JSON.stringify(this.currentUser));
            return true;
        }
        return false;
    },
    
    logout: function() {
        this.currentUser = null;
        localStorage.removeItem('user');
    },
    
    isAuthenticated: function() {
        const user = localStorage.getItem('user');
        if (user) {
            this.currentUser = JSON.parse(user);
            return true;
        }
        return false;
    }
};

// Datos de demo para constancias
window.demoData = {
    constancias: [
        {
            id: 'const001',
            alumno: 'Kevin Eduardo Pinto',
            codigo: '20220259H',
            documento: 'constancia_20220259H_20241023.pdf',
            estado: 'Firmado y Aprobado',
            firma: 'Firmado',
            fecha: '23/10/2024 19:30',
            carrera: 'Ingeniería Eléctrica',
            validado_uni: 'SÍ'
        },
        {
            id: 'const002',
            alumno: 'María García López',
            codigo: '20210002',
            documento: 'constancia_20210002_20241022.pdf',
            estado: 'Enviado',
            firma: 'Pendiente',
            fecha: '22/10/2024 14:20',
            carrera: 'Ingeniería Electrónica',
            validado_uni: 'SÍ'
        }
    ]
};

console.log('✅ Configuración de demo cargada');