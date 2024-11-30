from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Configuración de Selenium
driver = webdriver.Chrome()  # Asegúrate de tener el controlador de Chrome instalado y actualizado

# URL de Waze o la página de tráfico en tiempo real
url = 'https://ul.waze.com/ul?ll=-33.43271275%2C-70.64983606&navigate=yes&zoom=16&utm_campaign=default&utm_source=waze_website&utm_medium=lm_share_location'
driver.get(url)

# Esperar a que la página cargue completamente
time.sleep(10)

# Función para intentar cerrar el popup utilizando JavaScript
def cerrar_popup_con_js():
    try:
        # Ejecutar código JavaScript para ocultar el popup
        driver.execute_script("""
            var popup = document.querySelector('.waze-tour-step__overlay');
            if (popup) {
                popup.style.display = 'none';  # Ocultar el popup
            }
        """)
        print("Popup cerrado usando JavaScript.")
        time.sleep(1)  # Espera para asegurarse de que el popup se cierre
    except Exception as e:
        print(f"No se pudo cerrar el popup con JavaScript: {e}")

# Intentar cerrar el popup de "Edit your arrival time" con JavaScript
cerrar_popup_con_js()

# Extraer información de tráfico
incidentes = []
try:
    # Encuentra todos los iconos de incidentes (usa las clases específicas)
    incident_elements = driver.find_elements(By.CSS_SELECTOR, '.wm-alert-icon')  # Todos los iconos de alerta
    print(f"Se encontraron {len(incident_elements)} incidentes en el mapa.")

    for _ in range(len(incident_elements)):
        # Refrescar la lista de elementos en cada iteración
        incident_elements = driver.find_elements(By.CSS_SELECTOR, '.wm-alert-icon')
        elem = incident_elements[_]  # Seleccionar el elemento actual
        
        # Intentar hacer clic en el marcador
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.wm-alert-icon')))
            driver.execute_script("arguments[0].click();", elem)
            time.sleep(2)  # Espera para que el popup se cargue

            # Extraer detalles del popup
            try:
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.wm-alert-details__title'))
                )
                address_element = driver.find_element(By.CSS_SELECTOR, '.wm-alert-details__address')
                time_element = driver.find_element(By.CSS_SELECTOR, '.wm-alert-details__time')

                incident = {
                    "tipo": title_element.text,  # Tipo del incidente (ej. "Problema de Semáforo")
                    "ubicacion": address_element.text,  # Ubicación (ej. "Av. Cardenal José María Caro")
                    "hora": time_element.text,  # Hora del incidente (ej. "hace 26 min")
                }

                incidentes.append(incident)
                print(f"Incidente extraído: {incident}")  # Para verificar cada incidente extraído
            except Exception as e:
                print(f"Error al extraer detalles del popup: {e}")
            
            # Cerrar el popup para continuar
            try:
                close_button = driver.find_element(By.CSS_SELECTOR, '.leaflet-popup-close-button')
                close_button.click()
                time.sleep(1)  # Espera a que se cierre el popup
            except Exception as e:
                print(f"Error al cerrar el popup: {e}")
        except Exception as e:
            print(f"Error al hacer clic en el marcador: {e}")

except Exception as e:
    print(f"Error al obtener incidentes: {e}")

driver.quit()

# Guardar los incidentes en un archivo JSON
with open("incidentes.json", "w") as file:
    json.dump(incidentes, file, indent=4)

print("Incidentes extraídos y guardados en 'incidentes.json'.")
