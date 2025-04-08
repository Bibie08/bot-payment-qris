from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

SAWERIA_URL = "https://saweria.co/habibiezz"

def generate_qris(amount):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Jalankan tanpa GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(SAWERIA_URL)
        time.sleep(3)  # Tunggu halaman load

        # Isi form
        driver.find_element(By.NAME, "amount").send_keys(str(amount))
        driver.find_element(By.NAME, "name").send_keys("User")
        driver.find_element(By.NAME, "email").send_keys("user@example.com")
        driver.find_element(By.NAME, "message").send_keys("Pembayaran via bot")

        # Klik tombol donasi
        driver.find_element(By.XPATH, "//button[contains(text(),'Donasi')]").click()
        time.sleep(5)  # Tunggu proses

        # Ambil QRIS URL
        qris_element = driver.find_element(By.TAG_NAME, "img")
        qris_url = qris_element.get_attribute("src")

        return qris_url

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        driver.quit()
