from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

SAWERIA_URL = "https://saweria.co/habibiezz"

def generate_qris(amount):
    try:
        # Setup WebDriver dengan path chromedriver di Railway
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Jalankan tanpa tampilan GUI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service("/usr/bin/chromedriver")  # Path ChromeDriver di Railway
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(SAWERIA_URL)
        time.sleep(3)  # Tunggu halaman termuat

        # Isi form Saweria
        driver.find_element(By.NAME, "amount").send_keys(str(amount))
        driver.find_element(By.NAME, "name").send_keys("User Bot")
        driver.find_element(By.NAME, "email").send_keys("user@example.com")
        driver.find_element(By.NAME, "message").send_keys("Pembayaran via bot")

        # Submit form
        driver.find_element(By.NAME, "submit").click()
        time.sleep(5)  # Tunggu QRIS muncul

        # Ambil URL QRIS yang dihasilkan
        qris_url = driver.current_url
        driver.quit()  # Tutup browser
        return qris_url

    except Exception as e:
        print(f"❌ Error: {e}")
        return None
