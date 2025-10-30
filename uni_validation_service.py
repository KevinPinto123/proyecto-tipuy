"""
Servicio de Validación Automática de Estudiantes UNI
Integra con https://dirce.uni.edu.pe/alumnos/busqueda para validar datos
"""

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
from typing import Dict, Any, Optional
import re

class UNIValidationService:
    """
    Servicio para validar estudiantes en el portal oficial de la UNI
    """
    
    def __init__(self):
        self.base_url = "https://dirce.uni.edu.pe/alumnos/busqueda"
        self.logger = logging.getLogger(__name__)
        self.setup_chrome_options()
    
    def setup_chrome_options(self):
        """Configurar opciones de Chrome para scraping"""
        self.chrome_options = Options()
        # DESACTIVAR headless para debug - ver qué está pasando
        # self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        # Desactivar imágenes para cargar más rápido
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)
    
    def validar_estudiante_uni(self, codigo_estudiante: str, nombres: str = None) -> Dict[str, Any]:
        """
        Validar estudiante en el portal oficial de la UNI
        
        Args:
            codigo_estudiante: Código del estudiante (ej: 20220259H - 8 dígitos + 1 letra)
            nombres: Nombres del estudiante (opcional, para validación cruzada)
        
        Returns:
            Dict con información del estudiante validado
        """
        driver = None
        try:
            # Validar formato del código UNI (8 dígitos + 1 letra mayúscula)
            if not re.match(r'^\d{8}[A-Z]$', codigo_estudiante):
                return {
                    'success': False,
                    'error': f'Formato de código inválido. Debe ser 8 dígitos + 1 letra mayúscula (ej: 20220259H)',
                    'codigo': codigo_estudiante
                }
            
            self.logger.info(f"🔍 Iniciando validación UNI para código: {codigo_estudiante}")
            
            # Configurar WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)
            
            # Navegar al portal de búsqueda
            driver.get(self.base_url)
            self.logger.info("✅ Portal UNI cargado correctamente")
            
            # Esperar a que cargue la página completamente
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Esperar un poco más para que cargue JavaScript
            time.sleep(2)
            
            # Debug: Imprimir título de la página
            self.logger.info(f"📄 Título de página: {driver.title}")
            
            # Buscar el campo de código de estudiante con múltiples estrategias
            codigo_field = self._encontrar_campo_codigo_mejorado(driver)
            if not codigo_field:
                # Guardar screenshot para debug
                driver.save_screenshot("debug_uni_page.png")
                self.logger.error("❌ No se encontró campo de código. Screenshot guardado como debug_uni_page.png")
                raise Exception("No se pudo encontrar el campo de código de estudiante")
            
            # Limpiar y escribir código
            codigo_field.clear()
            time.sleep(0.5)
            codigo_field.send_keys(codigo_estudiante)
            self.logger.info(f"�B Código ingresado: {codigo_estudiante}")
            
            # Esperar un momento antes de buscar
            time.sleep(1)
            
            # Buscar y hacer clic en el botón de búsqueda
            boton_buscar = self._encontrar_boton_buscar_mejorado(driver)
            if boton_buscar:
                self.logger.info("🔍 Haciendo clic en botón de búsqueda...")
                driver.execute_script("arguments[0].click();", boton_buscar)  # Click con JavaScript
                time.sleep(1)
            else:
                # Alternativa: presionar Enter
                self.logger.info("🔍 Presionando Enter para buscar...")
                codigo_field.send_keys(Keys.RETURN)
            
            self.logger.info("⏳ Esperando resultados...")
            
            # Esperar más tiempo para resultados
            time.sleep(5)
            
            # Extraer información del estudiante
            datos_estudiante = self._extraer_datos_estudiante_mejorado(driver, codigo_estudiante)
            
            # Validar datos si se proporcionaron nombres
            if nombres and datos_estudiante.get('success'):
                datos_estudiante = self._validar_nombres(datos_estudiante, nombres)
            
            driver.quit()
            
            if datos_estudiante.get('success'):
                self.logger.info(f"✅ Estudiante validado: {datos_estudiante.get('nombre', 'N/A')}")
            else:
                self.logger.warning(f"❌ Estudiante no encontrado: {codigo_estudiante}")
            
            return datos_estudiante
            
        except Exception as e:
            if driver:
                driver.quit()
            
            self.logger.error(f"❌ Error validando estudiante: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'codigo_buscado': codigo_estudiante
            }
    
    def _encontrar_campo_codigo_mejorado(self, driver) -> Optional[Any]:
        """Encontrar el campo de código de estudiante con estrategias mejoradas"""
        
        # Estrategia 1: Selectores específicos para UNI
        selectores_uni = [
            "input[name='codigo']",
            "input[id='codigo']", 
            "input[name='codigoAlumno']",
            "input[id='codigoAlumno']",
            "input[placeholder*='código']",
            "input[placeholder*='Código']",
            "input[placeholder*='alumno']",
            "input[class*='codigo']",
            "input[class*='alumno']"
        ]
        
        self.logger.info("🔍 Buscando campo de código con selectores específicos...")
        for selector in selectores_uni:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                for elemento in elementos:
                    if elemento.is_displayed() and elemento.is_enabled():
                        self.logger.info(f"✅ Campo encontrado con selector: {selector}")
                        return elemento
            except Exception as e:
                self.logger.debug(f"Selector {selector} falló: {e}")
                continue
        
        # Estrategia 2: Buscar todos los inputs de texto
        self.logger.info("🔍 Buscando en todos los inputs de texto...")
        try:
            inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            self.logger.info(f"📝 Encontrados {len(inputs)} inputs de texto")
            
            for i, input_elem in enumerate(inputs):
                if input_elem.is_displayed() and input_elem.is_enabled():
                    # Verificar atributos del input
                    name = input_elem.get_attribute('name') or ''
                    id_attr = input_elem.get_attribute('id') or ''
                    placeholder = input_elem.get_attribute('placeholder') or ''
                    class_attr = input_elem.get_attribute('class') or ''
                    
                    self.logger.info(f"Input {i}: name='{name}', id='{id_attr}', placeholder='{placeholder}', class='{class_attr}'")
                    
                    # Buscar palabras clave
                    keywords = ['codigo', 'alumno', 'estudiante', 'buscar']
                    text_to_check = f"{name} {id_attr} {placeholder} {class_attr}".lower()
                    
                    if any(keyword in text_to_check for keyword in keywords):
                        self.logger.info(f"✅ Campo encontrado por keywords en input {i}")
                        return input_elem
            
            # Si no encuentra por keywords, usar el primer input visible
            if inputs:
                first_input = inputs[0]
                if first_input.is_displayed() and first_input.is_enabled():
                    self.logger.info("✅ Usando primer input de texto disponible")
                    return first_input
                    
        except Exception as e:
            self.logger.error(f"Error buscando inputs: {e}")
        
        # Estrategia 3: Buscar por XPath
        self.logger.info("🔍 Buscando con XPath...")
        xpath_selectors = [
            "//input[contains(@placeholder, 'código') or contains(@placeholder, 'Código')]",
            "//input[contains(@name, 'codigo') or contains(@name, 'alumno')]",
            "//input[@type='text'][1]"  # Primer input de texto
        ]
        
        for xpath in xpath_selectors:
            try:
                elementos = driver.find_elements(By.XPATH, xpath)
                for elemento in elementos:
                    if elemento.is_displayed() and elemento.is_enabled():
                        self.logger.info(f"✅ Campo encontrado con XPath: {xpath}")
                        return elemento
            except Exception as e:
                self.logger.debug(f"XPath {xpath} falló: {e}")
                continue
        
        return None
    
    def _encontrar_boton_buscar_mejorado(self, driver) -> Optional[Any]:
        """Encontrar el botón de búsqueda con estrategias mejoradas"""
        
        # Estrategia 1: Botones específicos
        selectores_botones = [
            "button[type='submit']",
            "input[type='submit']", 
            "button[value*='Buscar']",
            "input[value*='Buscar']",
            "button[value*='BUSCAR']",
            "input[value*='BUSCAR']",
            "button[class*='btn']",
            "input[class*='btn']"
        ]
        
        self.logger.info("🔍 Buscando botón de búsqueda...")
        for selector in selectores_botones:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                for elemento in elementos:
                    if elemento.is_displayed() and elemento.is_enabled():
                        texto = elemento.text.lower() if elemento.text else ''
                        value = elemento.get_attribute('value') or ''
                        
                        self.logger.info(f"Botón encontrado: texto='{texto}', value='{value}', type='{elemento.get_attribute('type')}'")
                        
                        if ('buscar' in texto or 'buscar' in value.lower() or 
                            elemento.get_attribute('type') == 'submit'):
                            self.logger.info(f"✅ Botón de búsqueda encontrado: {selector}")
                            return elemento
            except Exception as e:
                self.logger.debug(f"Selector {selector} falló: {e}")
                continue
        
        # Estrategia 2: Buscar todos los botones
        self.logger.info("🔍 Buscando en todos los botones...")
        try:
            botones = driver.find_elements(By.TAG_NAME, "button")
            inputs_submit = driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
            
            todos_botones = botones + inputs_submit
            self.logger.info(f"📝 Encontrados {len(todos_botones)} botones/inputs")
            
            for i, boton in enumerate(todos_botones):
                if boton.is_displayed() and boton.is_enabled():
                    texto = boton.text.lower() if boton.text else ''
                    value = boton.get_attribute('value') or ''
                    onclick = boton.get_attribute('onclick') or ''
                    
                    self.logger.info(f"Botón {i}: texto='{texto}', value='{value}', onclick='{onclick}'")
                    
                    # Buscar palabras clave
                    keywords = ['buscar', 'search', 'consultar', 'enviar', 'submit']
                    text_to_check = f"{texto} {value} {onclick}".lower()
                    
                    if any(keyword in text_to_check for keyword in keywords):
                        self.logger.info(f"✅ Botón encontrado por keywords: {i}")
                        return boton
            
            # Si no encuentra por keywords, usar el primer botón submit
            for boton in todos_botones:
                if (boton.is_displayed() and boton.is_enabled() and 
                    boton.get_attribute('type') == 'submit'):
                    self.logger.info("✅ Usando primer botón submit disponible")
                    return boton
                    
        except Exception as e:
            self.logger.error(f"Error buscando botones: {e}")
        
        # Estrategia 3: XPath
        self.logger.info("🔍 Buscando con XPath...")
        xpath_selectors = [
            "//button[contains(text(), 'Buscar') or contains(text(), 'BUSCAR')]",
            "//input[@value='Buscar' or @value='BUSCAR']",
            "//button[@type='submit']",
            "//input[@type='submit']"
        ]
        
        for xpath in xpath_selectors:
            try:
                elementos = driver.find_elements(By.XPATH, xpath)
                for elemento in elementos:
                    if elemento.is_displayed() and elemento.is_enabled():
                        self.logger.info(f"✅ Botón encontrado con XPath: {xpath}")
                        return elemento
            except Exception as e:
                self.logger.debug(f"XPath {xpath} falló: {e}")
                continue
        
        return None
    
    def _extraer_datos_estudiante_mejorado(self, driver, codigo_buscado: str) -> Dict[str, Any]:
        """Extraer datos del estudiante desde la página de resultados con estrategias mejoradas"""
        try:
            # Guardar screenshot para debug
            driver.save_screenshot(f"debug_resultados_{codigo_buscado}.png")
            self.logger.info(f"📸 Screenshot guardado: debug_resultados_{codigo_buscado}.png")
            
            # Obtener el HTML completo para análisis
            page_source = driver.page_source
            self.logger.info(f"📄 Tamaño de página: {len(page_source)} caracteres")
            
            # Buscar mensajes de error comunes
            mensajes_error = [
                "no se encontraron resultados",
                "no encontrado", 
                "sin resultados",
                "no existe",
                "error en la búsqueda"
            ]
            
            page_text = page_source.lower()
            for mensaje in mensajes_error:
                if mensaje in page_text:
                    self.logger.warning(f"⚠️ Mensaje de error detectado: {mensaje}")
                    return {
                        'success': False,
                        'error': f'Estudiante no encontrado: {mensaje}',
                        'codigo_buscado': codigo_buscado
                    }
            
            # Buscar información en diferentes formatos
            self.logger.info("🔍 Buscando datos en tablas...")
            datos = self._buscar_datos_en_tabla_mejorado(driver, codigo_buscado)
            
            if not datos:
                self.logger.info("🔍 Buscando datos en divs...")
                datos = self._buscar_datos_en_divs_mejorado(driver, codigo_buscado)
            
            if not datos:
                self.logger.info("🔍 Buscando datos en texto completo...")
                datos = self._buscar_datos_en_texto_mejorado(driver, codigo_buscado)
            
            if not datos:
                self.logger.info("🔍 Buscando con estrategia de fuerza bruta...")
                datos = self._buscar_datos_fuerza_bruta(driver, codigo_buscado)
            
            if datos:
                resultado = {
                    'success': True,
                    'codigo': datos.get('codigo', codigo_buscado),
                    'nombre': datos.get('nombre', ''),
                    'carrera': datos.get('carrera', ''),
                    'facultad': datos.get('facultad', ''),
                    'estado': datos.get('estado', 'Activo'),
                    'ciclo': datos.get('ciclo', ''),
                    'fuente': 'Portal UNI DIRCE',
                    'validado': True
                }
                self.logger.info(f"✅ Datos extraídos: {resultado}")
                return resultado
            else:
                # Guardar HTML para debug
                with open(f"debug_html_{codigo_buscado}.html", "w", encoding="utf-8") as f:
                    f.write(page_source)
                
                return {
                    'success': False,
                    'error': 'No se pudieron extraer datos del estudiante',
                    'codigo_buscado': codigo_buscado,
                    'debug_info': 'HTML guardado para análisis'
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error extrayendo datos: {e}")
            return {
                'success': False,
                'error': f'Error extrayendo datos: {str(e)}',
                'codigo_buscado': codigo_buscado
            }
    
    def _buscar_datos_en_tabla(self, driver, codigo: str) -> Optional[Dict[str, Any]]:
        """Buscar datos en formato de tabla"""
        try:
            tablas = driver.find_elements(By.TAG_NAME, "table")
            
            for tabla in tablas:
                filas = tabla.find_elements(By.TAG_NAME, "tr")
                
                for fila in filas:
                    celdas = fila.find_elements(By.TAG_NAME, "td")
                    if len(celdas) >= 2:
                        texto_fila = fila.text
                        if codigo in texto_fila:
                            return self._parsear_fila_estudiante(celdas, codigo)
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error buscando en tablas: {e}")
            return None
    
    def _buscar_datos_en_divs(self, driver, codigo: str) -> Optional[Dict[str, Any]]:
        """Buscar datos en divs o contenedores"""
        try:
            # Buscar divs que contengan el código
            elementos = driver.find_elements(By.XPATH, f"//*[contains(text(), '{codigo}')]")
            
            for elemento in elementos:
                contenedor = elemento.find_element(By.XPATH, "./..")
                texto_completo = contenedor.text
                
                if codigo in texto_completo:
                    return self._parsear_texto_estudiante(texto_completo, codigo)
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error buscando en divs: {e}")
            return None
    
    def _buscar_datos_en_texto(self, driver, codigo: str) -> Optional[Dict[str, Any]]:
        """Buscar datos en el texto completo de la página"""
        try:
            texto_pagina = driver.page_source
            
            if codigo in texto_pagina:
                # Buscar patrones comunes
                return self._parsear_texto_estudiante(driver.text, codigo)
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error buscando en texto: {e}")
            return None
    
    def _parsear_fila_estudiante(self, celdas, codigo: str) -> Dict[str, Any]:
        """Parsear datos de una fila de tabla"""
        datos = {'codigo': codigo}
        
        textos_celdas = [celda.text.strip() for celda in celdas]
        
        # Patrones comunes para identificar campos
        for i, texto in enumerate(textos_celdas):
            texto_lower = texto.lower()
            
            if len(texto) > 10 and any(palabra in texto_lower for palabra in ['ing', 'ciencias', 'arquitectura']):
                datos['carrera'] = texto
            elif len(texto) > 5 and not texto.isdigit() and codigo not in texto:
                if 'nombre' not in datos:
                    datos['nombre'] = texto
            elif 'activo' in texto_lower or 'inactivo' in texto_lower:
                datos['estado'] = texto
        
        return datos
    
    def _parsear_texto_estudiante(self, texto: str, codigo: str) -> Dict[str, Any]:
        """Parsear datos desde texto libre"""
        datos = {'codigo': codigo}
        
        # Buscar patrones con regex
        lineas = texto.split('\n')
        
        for linea in lineas:
            if codigo in linea:
                # Extraer información de la línea que contiene el código
                partes = linea.split()
                
                # Buscar nombre (palabras que no son números ni el código)
                nombre_partes = []
                for parte in partes:
                    if not parte.isdigit() and parte != codigo and len(parte) > 2:
                        nombre_partes.append(parte)
                
                if nombre_partes:
                    datos['nombre'] = ' '.join(nombre_partes[:3])  # Primeras 3 palabras como nombre
                
                break
        
        # Buscar carrera en líneas cercanas
        for linea in lineas:
            if any(palabra in linea.lower() for palabra in ['ingeniería', 'ing.', 'ciencias', 'arquitectura']):
                datos['carrera'] = linea.strip()
                break
        
        return datos
    
    def _buscar_datos_en_tabla_mejorado(self, driver, codigo: str) -> Optional[Dict[str, Any]]:
        """Buscar datos en formato de tabla con estrategias mejoradas"""
        try:
            tablas = driver.find_elements(By.TAG_NAME, "table")
            self.logger.info(f"📊 Encontradas {len(tablas)} tablas")
            
            for i, tabla in enumerate(tablas):
                try:
                    filas = tabla.find_elements(By.TAG_NAME, "tr")
                    self.logger.info(f"Tabla {i}: {len(filas)} filas")
                    
                    for j, fila in enumerate(filas):
                        texto_fila = fila.text.strip()
                        if codigo in texto_fila:
                            self.logger.info(f"✅ Código encontrado en tabla {i}, fila {j}: {texto_fila}")
                            celdas = fila.find_elements(By.TAG_NAME, "td")
                            if celdas:
                                return self._parsear_fila_estudiante_mejorado(celdas, codigo)
                except Exception as e:
                    self.logger.debug(f"Error procesando tabla {i}: {e}")
                    continue
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error buscando en tablas: {e}")
            return None
    
    def _buscar_datos_en_divs_mejorado(self, driver, codigo: str) -> Optional[Dict[str, Any]]:
        """Buscar datos en divs con estrategias mejoradas"""
        try:
            # Buscar elementos que contengan el código
            elementos = driver.find_elements(By.XPATH, f"//*[contains(text(), '{codigo}')]")
            self.logger.info(f"📦 Encontrados {len(elementos)} elementos con el código")
            
            for i, elemento in enumerate(elementos):
                try:
                    # Obtener el contenedor padre
                    contenedor = elemento.find_element(By.XPATH, "./..")
                    texto_completo = contenedor.text.strip()
                    
                    self.logger.info(f"Elemento {i}: {texto_completo[:100]}...")
                    
                    if len(texto_completo) > 20:  # Debe tener información suficiente
                        datos = self._parsear_texto_estudiante_mejorado(texto_completo, codigo)
                        if datos and datos.get('nombre'):
                            return datos
                            
                except Exception as e:
                    self.logger.debug(f"Error procesando elemento {i}: {e}")
                    continue
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error buscando en divs: {e}")
            return None
    
    def _buscar_datos_en_texto_mejorado(self, driver, codigo: str) -> Optional[Dict[str, Any]]:
        """Buscar datos en el texto completo con estrategias mejoradas"""
        try:
            texto_pagina = driver.find_element(By.TAG_NAME, "body").text
            
            if codigo in texto_pagina:
                self.logger.info("✅ Código encontrado en el texto de la página")
                return self._parsear_texto_estudiante_mejorado(texto_pagina, codigo)
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error buscando en texto: {e}")
            return None
    
    def _buscar_datos_fuerza_bruta(self, driver, codigo: str) -> Optional[Dict[str, Any]]:
        """Estrategia de fuerza bruta para encontrar datos"""
        try:
            # Buscar todos los elementos de texto
            elementos_texto = driver.find_elements(By.XPATH, "//*[text()]")
            
            datos_encontrados = {'codigo': codigo}
            
            for elemento in elementos_texto:
                texto = elemento.text.strip()
                if len(texto) > 5 and codigo not in texto:
                    # Buscar patrones de nombre (palabras capitalizadas)
                    if self._parece_nombre(texto) and 'nombre' not in datos_encontrados:
                        datos_encontrados['nombre'] = texto
                    
                    # Buscar patrones de carrera
                    if self._parece_carrera(texto) and 'carrera' not in datos_encontrados:
                        datos_encontrados['carrera'] = texto
            
            if len(datos_encontrados) > 1:  # Más que solo el código
                self.logger.info(f"✅ Datos encontrados por fuerza bruta: {datos_encontrados}")
                return datos_encontrados
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error en búsqueda de fuerza bruta: {e}")
            return None
    
    def _parsear_fila_estudiante_mejorado(self, celdas, codigo: str) -> Dict[str, Any]:
        """Parsear datos de una fila de tabla con lógica mejorada"""
        datos = {'codigo': codigo}
        
        textos_celdas = [celda.text.strip() for celda in celdas if celda.text.strip()]
        self.logger.info(f"📝 Celdas: {textos_celdas}")
        
        for texto in textos_celdas:
            if texto == codigo:
                continue
                
            # Identificar nombre (palabras con mayúsculas)
            if self._parece_nombre(texto) and 'nombre' not in datos:
                datos['nombre'] = texto
            
            # Identificar carrera
            elif self._parece_carrera(texto) and 'carrera' not in datos:
                datos['carrera'] = texto
            
            # Identificar estado
            elif texto.lower() in ['activo', 'inactivo', 'egresado', 'graduado']:
                datos['estado'] = texto
        
        return datos
    
    def _parsear_texto_estudiante_mejorado(self, texto: str, codigo: str) -> Dict[str, Any]:
        """Parsear datos desde texto libre con lógica mejorada"""
        datos = {'codigo': codigo}
        
        lineas = [linea.strip() for linea in texto.split('\n') if linea.strip()]
        
        # Buscar la línea que contiene el código
        linea_codigo = None
        for i, linea in enumerate(lineas):
            if codigo in linea:
                linea_codigo = i
                break
        
        if linea_codigo is not None:
            # Analizar líneas cercanas al código
            inicio = max(0, linea_codigo - 2)
            fin = min(len(lineas), linea_codigo + 3)
            
            for linea in lineas[inicio:fin]:
                if codigo in linea:
                    continue
                
                # Buscar nombre
                if self._parece_nombre(linea) and 'nombre' not in datos:
                    datos['nombre'] = linea
                
                # Buscar carrera
                elif self._parece_carrera(linea) and 'carrera' not in datos:
                    datos['carrera'] = linea
        
        return datos if len(datos) > 1 else None
    
    def _parece_nombre(self, texto: str) -> bool:
        """Determinar si un texto parece ser un nombre"""
        if not texto or len(texto) < 3:
            return False
        
        # Debe tener al menos 2 palabras
        palabras = texto.split()
        if len(palabras) < 2:
            return False
        
        # Las palabras deben empezar con mayúscula
        if not all(palabra[0].isupper() for palabra in palabras if palabra):
            return False
        
        # No debe contener números
        if any(char.isdigit() for char in texto):
            return False
        
        # No debe ser muy largo
        if len(texto) > 50:
            return False
        
        return True
    
    def _parece_carrera(self, texto: str) -> bool:
        """Determinar si un texto parece ser una carrera"""
        if not texto or len(texto) < 5:
            return False
        
        keywords_carrera = [
            'ingeniería', 'ing.', 'ciencias', 'arquitectura', 
            'administración', 'economía', 'derecho', 'medicina',
            'sistemas', 'industrial', 'civil', 'mecánica', 'eléctrica'
        ]
        
        texto_lower = texto.lower()
        return any(keyword in texto_lower for keyword in keywords_carrera)
    
    def _validar_nombres(self, datos_estudiante: Dict[str, Any], nombres_esperados: str) -> Dict[str, Any]:
        """Validar que los nombres coincidan"""
        if not datos_estudiante.get('success'):
            return datos_estudiante
        
        nombre_encontrado = datos_estudiante.get('nombre', '').lower()
        nombres_esperados = nombres_esperados.lower()
        
        # Verificar coincidencia parcial (al menos 60% de las palabras)
        palabras_encontradas = set(nombre_encontrado.split())
        palabras_esperadas = set(nombres_esperados.split())
        
        if palabras_encontradas and palabras_esperadas:
            coincidencia = len(palabras_encontradas.intersection(palabras_esperadas))
            total_palabras = len(palabras_esperadas)
            
            porcentaje_coincidencia = (coincidencia / total_palabras) * 100
            
            datos_estudiante['coincidencia_nombres'] = porcentaje_coincidencia
            datos_estudiante['nombres_validados'] = porcentaje_coincidencia >= 60
            
            if porcentaje_coincidencia < 60:
                datos_estudiante['warning'] = f"Los nombres no coinciden completamente ({porcentaje_coincidencia:.1f}% coincidencia)"
        
        return datos_estudiante


# Función de utilidad para integración fácil
def validar_estudiante_uni(codigo: str, nombres: str = None) -> Dict[str, Any]:
    """
    Función de utilidad para validar estudiante UNI
    
    Args:
        codigo: Código del estudiante
        nombres: Nombres del estudiante (opcional)
    
    Returns:
        Datos del estudiante validado
    """
    validator = UNIValidationService()
    return validator.validar_estudiante_uni(codigo, nombres)


# Ejemplo de uso
if __name__ == "__main__":
    # Test de validación
    codigo_test = "20241234"  # Cambiar por un código real para probar
    nombres_test = "Juan Pérez García"
    
    print(f"🔍 Validando estudiante: {codigo_test}")
    resultado = validar_estudiante_uni(codigo_test, nombres_test)
    
    print("\n📋 Resultado:")
    for key, value in resultado.items():
        print(f"  {key}: {value}")