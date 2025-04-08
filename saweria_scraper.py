from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def generate_qris(nominal):
    # Setup Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run tanpa membuka browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Buka halaman Saweria
        driver.get("https://saweria.co/habibiezz")
        time.sleep(3)  # Tunggu loading

        # Isi nominal
        nominal_input = driver.find_element(By.NAME, "amount")
        nominal_input.clear()
        nominal_input.send_keys(str(nominal))

        # Isi nama
        name_input = driver.find_element(By.NAME, "name")
        name_input.clear()
        name_input.send_keys("User")

        # Isi email
        email_input = driver.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys("user@example.com")

        # Isi pesan
        message_input = driver.find_element(By.NAME, "message")
        message_input.clear()
        message_input.send_keys("Pembayaran via bot")

        # Klik checkbox (jika ada)
        try:
            checkbox = driver.find_element(By.NAME, "agree")
            checkbox.click()
        except:
            pass  # Jika tidak ada checkbox, lanjut saja

        # Klik tombol "Lanjutkan"
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Lanjutkan')]")
        submit_button.click()

        # Tunggu QRIS muncul
        time.sleep(5)

        # Ambil URL QRIS
        qris_img = driver.find_element(By.TAG_NAME, "img")
        qris_url = qris_img.get_attribute("src")

        return qris_url

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        driver.quit()  # Tutup browser

# Contoh penggunaan
if __name__ == "__main__":
    nominal = 5000  # Contoh nominal
    qris_url = generate_qris(nominal)
    if qris_url:
        print(f"QRIS URL: {qris_url}")
    else:
        print("Gagal membuat QRIS.")
