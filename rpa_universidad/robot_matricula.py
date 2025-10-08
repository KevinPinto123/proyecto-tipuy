from RPA.Browser.Selenium import Selenium
from RPA.PDF import PDF
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Inicializar navegador con webdriver manager
browser = Selenium()
browser.set_driver(webdriver.Chrome(ChromeDriverManager().install()))

# 1. Abrir formulario de ejemplo
browser.open_available_browser("https://www.w3schools.com/html/html_forms.asp")

# 2. Llenar campos (simulando matrícula)
browser.input_text("xpath://input[@name='firstname']", "Kevin")
browser.input_text("xpath://input[@name='lastname']", "Pinto")

# 3. Click en botón
browser.click_button("xpath://button[@type='submit']")

# 4. Generar PDF de constancia
pdf = PDF()
pdf.html_to_pdf(
    "<h1>Constancia de Matrícula</h1><p>Alumno: Kevin Pinto</p>",
    "constancia.pdf"
)

print("✅ Flujo completado. Se generó constancia.pdf")
browser.close_browser()


