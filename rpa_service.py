from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
import uuid
from datetime import datetime
import openpyxl
from openpyxl import Workbook
import time

class RPAService:
    def __init__(self):
        self.excel_file = "seguimiento.xlsx"
        self.pdf_folder = "autoridad_entrada"
        self._inicializar_excel()
    
    def _inicializar_excel(self):
        """Crear archivo Excel de seguimiento si no existe"""
        if not os.path.exists(self.excel_file):
            wb = Workbook()
            ws = wb.active
            ws.title = "Seguimiento_Constancias"
            
            # Encabezados
            headers = ["ID", "Alumno", "Codigo", "Carrera", "Ciclo", 
                      "Documento", "Estado", "Autoridad", "Firma", "Fecha_Creacion"]
            ws.append(headers)
            
            wb.save(self.excel_file)
            print("✅ Archivo de seguimiento Excel creado")
    
    def generar_constancia_completa(self, nombre, codigo, carrera, ciclo):
        """Flujo RPA completo para generar constancia"""
        print(f"🔄 Iniciando flujo RPA para {nombre}...")
        
        # 1. Abrir navegador (simulación)
        self._ejecutar_navegador_demo()
        
        # 2. Generar PDF
        archivo_pdf = self._generar_pdf_constancia(nombre, codigo, carrera, ciclo)
        
        # 3. Registrar en Excel
        registro_id = self._registrar_en_excel(nombre, codigo, carrera, ciclo, archivo_pdf)
        
        print("✅ Flujo RPA completado exitosamente")
        
        return {
            'archivo_pdf': archivo_pdf,
            'registro_id': registro_id
        }
    
    def _ejecutar_navegador_demo(self):
        """Demostración de automatización con navegador usando Selenium"""
        browser = None
        try:
            print("🌐 Abriendo navegador para demostración...")
            
            # Configurar ChromeDriver
            service = Service(ChromeDriverManager().install())
            browser = webdriver.Chrome(service=service)
            
            # Abrir Google como demo
            browser.get("https://www.google.com")
            print("✅ Navegador abierto correctamente")
            
            time.sleep(1)
            
            # Buscar el campo de búsqueda y realizar búsqueda
            search_box = browser.find_element(By.NAME, "q")
            search_box.send_keys("constancia académica universidad")
            search_box.send_keys(Keys.RETURN)
            print("✅ Búsqueda de constancia académica realizada")
            
            time.sleep(2)
            
            # Cerrar navegador
            browser.quit()
            print("✅ Navegador cerrado correctamente")
            
        except Exception as e:
            print(f"⚠️ Error en navegador (continuando): {e}")
            if browser:
                try:
                    browser.quit()
                except:
                    pass
    
    def _generar_pdf_constancia(self, nombre, codigo, carrera, ciclo):
        """Generar PDF de constancia académica"""
        # Crear nombre único para el archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_pdf = f"constancia_{codigo}_{timestamp}.pdf"
        ruta_completa = os.path.join(self.pdf_folder, archivo_pdf)
        
        # Crear PDF con reportlab
        c = canvas.Canvas(ruta_completa, pagesize=letter)
        width, height = letter
        
        # Encabezado
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width/2, height-100, "UNIVERSIDAD NACIONAL DE INGENIERÍA")
        
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height-140, "CONSTANCIA DE ESTUDIOS")
        
        # Contenido
        c.setFont("Helvetica", 12)
        y_position = height - 200
        
        contenido = [
            f"Por medio de la presente se hace constar que:",
            "",
            f"Nombre del Estudiante: {nombre}",
            f"Código de Alumno: {codigo}",
            f"Carrera: {carrera}",
            f"Ciclo Académico: {ciclo}",
            "",
            f"Se encuentra matriculado y cursando estudios regulares",
            f"en esta casa de estudios superiores.",
            "",
            f"Se expide la presente constancia a solicitud del interesado",
            f"para los fines que estime conveniente.",
            "",
            f"Lima, {datetime.now().strftime('%d de %B de %Y')}"
        ]
        
        for linea in contenido:
            c.drawString(100, y_position, linea)
            y_position -= 25
        
        # Pie de página
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width/2, 150, "Firma pendiente de autoridad competente")
        c.drawCentredString(width/2, 130, "Coordinación Académica")
        
        c.save()
        
        print(f"✅ PDF generado: {archivo_pdf}")
        return archivo_pdf
    
    def _registrar_en_excel(self, nombre, codigo, carrera, ciclo, archivo_pdf):
        """Registrar constancia en Excel de seguimiento"""
        try:
            wb = openpyxl.load_workbook(self.excel_file)
            ws = wb.active
            
            # Generar ID único
            registro_id = str(uuid.uuid4())[:8]
            
            # Agregar nueva fila
            nueva_fila = [
                registro_id,
                nombre,
                codigo,
                carrera,
                ciclo,
                archivo_pdf,
                "Enviado",
                "Coordinador Académico",
                "Pendiente",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]
            
            ws.append(nueva_fila)
            wb.save(self.excel_file)
            
            print("✅ Constancia enviada a autoridad")
            print("✅ Seguimiento actualizado en Excel")
            
            return registro_id
            
        except Exception as e:
            print(f"❌ Error al registrar en Excel: {e}")
            raise
    
    def obtener_seguimiento(self):
        """Obtener lista de constancias para mostrar en web"""
        try:
            if not os.path.exists(self.excel_file):
                return []
            
            wb = openpyxl.load_workbook(self.excel_file)
            ws = wb.active
            
            constancias = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[0]:  # Si hay ID
                    constancias.append({
                        'id': row[0],
                        'alumno': row[1],
                        'codigo': row[2],
                        'carrera': row[3],
                        'ciclo': row[4],
                        'documento': row[5],
                        'estado': row[6],
                        'autoridad': row[7],
                        'firma': row[8],
                        'fecha': row[9]
                    })
            
            return constancias
            
        except Exception as e:
            print(f"❌ Error al obtener seguimiento: {e}")
            return []
    
    def firmar_constancia(self, registro_id):
        """Simular firma digital de autoridad"""
        try:
            wb = openpyxl.load_workbook(self.excel_file)
            ws = wb.active
            
            # Buscar y actualizar registro
            for row_num, row in enumerate(ws.iter_rows(min_row=2), start=2):
                if row[0].value == registro_id:
                    ws.cell(row=row_num, column=9).value = "Firmado"  # Columna Firma
                    ws.cell(row=row_num, column=7).value = "Firmado y Aprobado"  # Columna Estado
                    break
            
            wb.save(self.excel_file)
            print(f"✅ Constancia {registro_id} firmada digitalmente")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al firmar constancia: {e}")
            raise