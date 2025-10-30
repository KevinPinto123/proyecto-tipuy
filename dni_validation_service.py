"""
Servicio de Validación de DNI usando eldni.com
Integra con https://eldni.com/pe/buscar-datos-por-dni para validar DNI
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

class DNIValidationService:
    """
    Servicio para validar DNI en eldni.com
    """
    
    def __init__(self):
        self.base_url = "https://eldni.com/pe/buscar-datos-por-dni"
        self.logger = logging.getLogger(__name__)
        self.setup_chrome_options()
    
    def setup_chrome_options(self):
        """Configurar opciones de Chrome para scraping"""
        self.chrome_options = Options()
        # Usar headless para DNI (más rápido)
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        # Desactivar imágenes para cargar más rápido
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)
    
    def validar_dni(self, dni: str) -> Dict[str, Any]:
        """
        Validar DNI en eldni.com
        
        Args:
            dni: Número de DNI (8 dígitos)
        
        Returns:
            Dict con información de la persona
        """
        driver = None
        try:
            # Validar formato de DNI
            if not self._validar_formato_dni(dni):
                return {
                    'success': False,
                    'error': 'DNI debe tener exactamente 8 dígitos',
                    'dni_buscado': dni
                }
            
            self.logger.info(f"🔍 Iniciando validación DNI: {dni}")
            
            # Configurar WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)
            
            # Navegar al sitio de validación
            driver.get(self.base_url)
            self.logger.info("✅ Sitio eldni.com cargado correctamente")
            
            # Esperar a que cargue la página
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(2)  # Esperar carga completa
            
            # Buscar el campo de DNI
            dni_field = self._encontrar_campo_dni(driver)
            if not dni_field:
                raise Exception("No se pudo encontrar el campo de DNI")
            
            # Limpiar y escribir DNI
            dni_field.clear()
            time.sleep(0.5)
            dni_field.send_keys(dni)
            self.logger.info(f"📝 DNI ingresado: {dni}")
            
            # Buscar y hacer clic en el botón de búsqueda
            boton_buscar = self._encontrar_boton_buscar(driver)
            if boton_buscar:
                self.logger.info("🔍 Haciendo clic en botón de búsqueda...")
                driver.execute_script("arguments[0].click();", boton_buscar)
                time.sleep(1)
            else:
                # Alternativa: presionar Enter
                self.logger.info("🔍 Presionando Enter para buscar...")
                dni_field.send_keys(Keys.RETURN)
            
            self.logger.info("⏳ Esperando resultados...")
            
            # Esperar resultados
            time.sleep(5)
            
            # Extraer información de la persona
            datos_persona = self._extraer_datos_persona(driver, dni)
            
            driver.quit()
            
            if datos_persona.get('success'):
                self.logger.info(f"✅ DNI validado: {datos_persona.get('nombres', 'N/A')}")
            else:
                self.logger.warning(f"❌ DNI no encontrado: {dni}")
            
            return datos_persona
            
        except Exception as e:
            if driver:
                driver.quit()
            
            self.logger.error(f"❌ Error validando DNI: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'dni_buscado': dni
            }
    
    def _validar_formato_dni(self, dni: str) -> bool:
        """Validar que el DNI tenga el formato correcto"""
        if not dni:
            return False
        
        # Debe ser exactamente 8 dígitos
        if len(dni) != 8:
            return False
        
        # Debe contener solo números
        if not dni.isdigit():
            return False
        
        return True
    
    def _encontrar_campo_dni(self, driver) -> Optional[Any]:
        """Encontrar el campo de DNI"""
        selectores_dni = [
            "input[name*='dni']",
            "input[id*='dni']",
            "input[placeholder*='DNI']",
            "input[placeholder*='dni']",
            "input[type='text']",
            "input[name*='documento']",
            "input[id*='documento']"
        ]
        
        self.logger.info("🔍 Buscando campo de DNI...")
        for selector in selectores_dni:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                for elemento in elementos:
                    if elemento.is_displayed() and elemento.is_enabled():
                        self.logger.info(f"✅ Campo DNI encontrado con selector: {selector}")
                        return elemento
            except Exception as e:
                self.logger.debug(f"Selector {selector} falló: {e}")
                continue
        
        # Buscar todos los inputs de texto
        try:
            inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            if inputs:
                # Usar el primer input disponible
                first_input = inputs[0]
                if first_input.is_displayed() and first_input.is_enabled():
                    self.logger.info("✅ Usando primer input de texto para DNI")
                    return first_input
        except Exception as e:
            self.logger.error(f"Error buscando inputs: {e}")
        
        return None
    
    def _encontrar_boton_buscar(self, driver) -> Optional[Any]:
        """Encontrar el botón de búsqueda"""
        selectores_botones = [
            "button[type='submit']",
            "input[type='submit']",
            "button:contains('Buscar')",
            "button:contains('BUSCAR')",
            "input[value*='Buscar']",
            ".btn",
            "button"
        ]
        
        self.logger.info("🔍 Buscando botón de búsqueda...")
        for selector in selectores_botones:
            try:
                elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                for elemento in elementos:
                    if elemento.is_displayed() and elemento.is_enabled():
                        texto = elemento.text.lower() if elemento.text else ''
                        value = elemento.get_attribute('value') or ''
                        
                        if ('buscar' in texto or 'buscar' in value.lower() or 
                            elemento.get_attribute('type') == 'submit'):
                            self.logger.info(f"✅ Botón de búsqueda encontrado: {selector}")
                            return elemento
            except Exception as e:
                self.logger.debug(f"Selector {selector} falló: {e}")
                continue
        
        # Buscar todos los botones
        try:
            botones = driver.find_elements(By.TAG_NAME, "button")
            if botones:
                # Usar el primer botón disponible
                first_button = botones[0]
                if first_button.is_displayed() and first_button.is_enabled():
                    self.logger.info("✅ Usando primer botón disponible")
                    return first_button
        except Exception as e:
            self.logger.error(f"Error buscando botones: {e}")
        
        return None
    
    def _extraer_datos_persona(self, driver, dni: str) -> Dict[str, Any]:
        """Extraer datos de la persona desde la página de resultados"""
        try:
            # Obtener el texto completo de la página
            page_text = driver.find_element(By.TAG_NAME, "body").text
            
            # Buscar mensajes de error
            mensajes_error = [
                "no se encontraron datos",
                "dni no encontrado",
                "no existe",
                "error en la consulta",
                "datos no disponibles"
            ]
            
            page_text_lower = page_text.lower()
            for mensaje in mensajes_error:
                if mensaje in page_text_lower:
                    return {
                        'success': False,
                        'error': f'DNI no encontrado: {mensaje}',
                        'dni_buscado': dni
                    }
            
            # Buscar datos en diferentes formatos
            datos = self._parsear_datos_dni(page_text, dni)
            
            if not datos:
                # Buscar en tablas
                datos = self._buscar_en_tablas_dni(driver, dni)
            
            if not datos:
                # Buscar en divs específicos
                datos = self._buscar_en_divs_dni(driver, dni)
            
            if datos:
                return {
                    'success': True,
                    'dni': dni,
                    'nombres': datos.get('nombres', ''),
                    'apellido_paterno': datos.get('apellido_paterno', ''),
                    'apellido_materno': datos.get('apellido_materno', ''),
                    'nombre_completo': datos.get('nombre_completo', ''),
                    'fuente': 'eldni.com',
                    'validado': True
                }
            else:
                return {
                    'success': False,
                    'error': 'No se pudieron extraer datos del DNI',
                    'dni_buscado': dni
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error extrayendo datos: {str(e)}',
                'dni_buscado': dni
            }
    
    def _parsear_datos_dni(self, texto: str, dni: str) -> Optional[Dict[str, Any]]:
        """Parsear datos desde texto usando patrones"""
        datos = {}
        
        # Buscar patrones comunes
        lineas = texto.split('\n')
        
        for i, linea in enumerate(lineas):
            linea = linea.strip()
            
            # Buscar nombres y apellidos
            if any(keyword in linea.lower() for keyword in ['nombre', 'apellido']):
                # La siguiente línea podría contener el dato
                if i + 1 < len(lineas):
                    valor = lineas[i + 1].strip()
                    if len(valor) > 2 and not valor.isdigit():
                        if 'nombre' in linea.lower():
                            datos['nombres'] = valor
                        elif 'paterno' in linea.lower():
                            datos['apellido_paterno'] = valor
                        elif 'materno' in linea.lower():
                            datos['apellido_materno'] = valor
            
            # Buscar nombre completo en una sola línea
            if self._parece_nombre_completo(linea):
                datos['nombre_completo'] = linea
        
        # Construir nombre completo si no se encontró
        if not datos.get('nombre_completo') and datos.get('nombres'):
            nombre_completo = datos['nombres']
            if datos.get('apellido_paterno'):
                nombre_completo += ' ' + datos['apellido_paterno']
            if datos.get('apellido_materno'):
                nombre_completo += ' ' + datos['apellido_materno']
            datos['nombre_completo'] = nombre_completo
        
        return datos if datos else None
    
    def _buscar_en_tablas_dni(self, driver, dni: str) -> Optional[Dict[str, Any]]:
        """Buscar datos en tablas"""
        try:
            tablas = driver.find_elements(By.TAG_NAME, "table")
            
            for tabla in tablas:
                filas = tabla.find_elements(By.TAG_NAME, "tr")
                
                for fila in filas:
                    celdas = fila.find_elements(By.TAG_NAME, "td")
                    if len(celdas) >= 2:
                        textos = [celda.text.strip() for celda in celdas]
                        
                        # Buscar patrones de nombre
                        for texto in textos:
                            if self._parece_nombre_completo(texto):
                                return {'nombre_completo': texto}
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error buscando en tablas: {e}")
            return None
    
    def _buscar_en_divs_dni(self, driver, dni: str) -> Optional[Dict[str, Any]]:
        """Buscar datos en divs"""
        try:
            # Buscar divs que contengan texto relevante
            elementos = driver.find_elements(By.XPATH, "//*[text()]")
            
            for elemento in elementos:
                texto = elemento.text.strip()
                if self._parece_nombre_completo(texto):
                    return {'nombre_completo': texto}
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error buscando en divs: {e}")
            return None
    
    def _parece_nombre_completo(self, texto: str) -> bool:
        """Determinar si un texto parece ser un nombre completo"""
        if not texto or len(texto) < 5:
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
        
        # No debe ser muy largo (nombres reales)
        if len(texto) > 80:
            return False
        
        # No debe contener palabras comunes de páginas web
        palabras_excluir = ['buscar', 'consultar', 'datos', 'información', 'resultado']
        if any(palabra.lower() in palabras_excluir for palabra in palabras):
            return False
        
        return True


# Función de utilidad para integración fácil
def validar_dni(dni: str) -> Dict[str, Any]:
    """
    Función de utilidad para validar DNI
    
    Args:
        dni: Número de DNI (8 dígitos)
    
    Returns:
        Datos de la persona validada
    """
    validator = DNIValidationService()
    return validator.validar_dni(dni)


# Ejemplo de uso
if __name__ == "__main__":
    # Test de validación
    dni_test = input("Ingresa un DNI para validar (8 dígitos): ").strip()
    
    if dni_test:
        print(f"🔍 Validando DNI: {dni_test}")
        resultado = validar_dni(dni_test)
        
        print("\n📋 Resultado:")
        for key, value in resultado.items():
            print(f"  {key}: {value}")
    else:
        print("❌ DNI vacío")