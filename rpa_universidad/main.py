from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files

def prueba_basica():
    # Probar navegador
    browser = Selenium()
    browser.open_available_browser("https://www.google.com")
    print("✅ Navegador abierto correctamente")

    # Probar Excel
    excel = Files()
    excel.create_workbook("prueba.xlsx")
    excel.append_rows_to_worksheet([["Nombre", "Edad"], ["Kevin", 21], ["Andrea", 22]])
    excel.save_workbook()
    excel.close_workbook()
    print("✅ Archivo Excel creado y guardado")

if __name__ == "__main__":
    prueba_basica()

