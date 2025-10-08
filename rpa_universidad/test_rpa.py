from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def test_google_search():
    # Usa webdriver-manager para instalar y gestionar el chromedriver correcto
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Universidad Nacional de Ingeniería Perú")
    search_box.send_keys(Keys.RETURN)

    assert "Universidad Nacional de Ingeniería" in driver.page_source

    driver.quit()
