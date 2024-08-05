from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Configurar el navegador para usar el perfil existente
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/home/javier/.config/google-chrome/Default")  # Ruta al perfil de Chrome

# Inicializar el navegador con el perfil existente
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Navegando a la URL de inicio de sesión...")
    driver.get('https://persona.patria.org.ve/login/clave/')

    print("Esperando a que el campo de cédula esté presente...")
    cedula_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    cedula_field.send_keys('tu_cedula')
    print("Cédula ingresada.")

    print("Esperando a que el campo de captcha esté presente y sea interactuable...")
    captcha_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'captchaCode'))
    )
    captcha_field.send_keys('tu_captcha')
    print("Captcha ingresado.")

    print("Esperando a que el botón de enviar esté presente y sea interactuable...")
    submit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'send_button'))
    )
    submit_button.click()
    print("Botón de enviar clicado.")

    print("Navegando a la URL de autenticación...")
    driver.get('https://persona.patria.org.ve/login/clave/autenticar')

    print("Esperando a que el campo de cédula esté presente...")
    cedula_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, '_username'))
    )
    cedula_field.send_keys('tu_cedula')
    print("Cédula ingresada nuevamente.")

    print("Esperando a que el campo de clave esté presente...")
    clave_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, '_password'))
    )
    clave_field.send_keys('tu_clave')
    print("Clave ingresada.")

    print("Esperando a que el botón de enviar esté presente y sea interactuable...")
    submit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'enviar'))
    )
    submit_button.click()
    print("Botón de enviar clicado.")

    print("Navegando a la URL de estadísticas...")
    driver.get('https://persona.patria.org.ve/monedero/estadisticas/')

    all_data = []

    while True:
        print("Esperando a que la tabla esté presente en el DOM...")
        table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'benefits_table'))
        )
        print("Tabla encontrada.")

        # Extraer datos de la tabla
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            all_data.append([col.text for col in cols])

        # Verificar si hay un botón de "Siguiente"
        try:
            next_button = driver.find_element(By.XPATH, '//li[@id="benefits_table_next" and not(contains(@class, "disabled"))]')
            next_button.click()
            print("Navegando a la siguiente página...")
            time.sleep(2)  # Esperar un poco para que la página cargue
        except:
            print("No hay más páginas.")
            break

    # Guardar los datos en un archivo CSV
    with open('benefits_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Fecha', 'Tipo', 'Cantidad', 'Monto'])
        writer.writerows(all_data)
    print("Datos guardados en benefits_data.csv.")

    # Pausar para evitar que el navegador se cierre inmediatamente
    time.sleep(10)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
    print("Navegador cerrado.")