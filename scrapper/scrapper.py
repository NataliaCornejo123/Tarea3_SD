from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Configuración de Selenium
from selenium.webdriver.chrome.options import Options

options = Options()
driver = webdriver.Chrome(options=options)

# URL de Waze
url = 'https://www.waze.com/es/live-map/directions?from=ll.-33.43672386%2C-70.63599586'
driver.get(url)

# Esperar a que la página cargue completamente
time.sleep(10)

# Lista para guardar incidentes
incidentes = []

def extraer_detalles(element):
    """Intenta extraer detalles de un incidente después de hacer clic."""
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2)  # Espera para que cargue el popup

        # Extrae detalles del popup
        title_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.wm-alert-details__title'))
        )
        address_element = driver.find_element(By.CSS_SELECTOR, '.wm-alert-details__address')
        time_element = driver.find_element(By.CSS_SELECTOR, '.wm-alert-details__time')

        return {
            "tipo": title_element.text.strip(),
            "ubicacion": address_element.text.strip(),
            "hora": time_element.text.strip(),
        }
    except Exception as e:
        print(f"Error al extraer detalles del incidente: {e}")
        return None

# Encuentra todos los iconos de incidentes, filtrando los "autos felices"
try:
    incident_elements = driver.find_elements(By.CSS_SELECTOR, '.leaflet-marker-icon.wm-alert-icon')
    print(f"Se encontraron {len(incident_elements)} incidentes en el mapa.")

    for index in range(len(incident_elements)):
        # Refrescar la lista de incidentes en cada iteración
        incident_elements = driver.find_elements(By.CSS_SELECTOR, '.leaflet-marker-icon.wm-alert-icon')
        if index >= len(incident_elements):
            print("Número de incidentes cambió dinámicamente, finalizando.")
            break

        element = incident_elements[index]
        print(f"Procesando incidente {index + 1} de {len(incident_elements)}")

        incidente = extraer_detalles(element)
        if incidente:
            incidentes.append(incidente)
            print(f"Incidente extraído: {incidente}")

except Exception as e:
    print(f"Error durante la extracción de incidentes: {e}")

driver.quit()

# Guardar en JSON
with open("incidentes.json", "w", encoding="utf-8") as file:
    json.dump(incidentes, file, indent=4, ensure_ascii=False)

print("Incidentes extraídos y guardados en 'incidentes.json'.")
