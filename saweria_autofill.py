from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fill_saweria_form(url, amount, name, email, message):
    # Setup WebDriver (gunakan Chrome atau Firefox sesuai kebutuhan)
    driver = webdriver.Chrome()
    driver.get(url)
    
    try:
        # Tunggu hingga input nominal tersedia
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "amount"))
        )
        
        # Isi nominal
        amount_input = driver.find_element(By.NAME, "amount")
        amount_input.clear()
        amount_input.send_keys(str(amount))
        
        # Isi nama
        name_input = driver.find_element(By.NAME, "name")
        name_input.clear()
        name_input.send_keys(name)
        
        # Isi email
        email_input = driver.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(email)
        
        # Isi pesan
        message_input = driver.find_element(By.NAME, "message")
        message_input.clear()
        message_input.send_keys(message)
        
        # Centang checkbox (jika ada)
        try:
            checkbox = driver.find_element(By.NAME, "terms")
            if not checkbox.is_selected():
                checkbox.click()
        except:
            print("Checkbox tidak ditemukan atau tidak diperlukan.")
        
        # Pilih metode pembayaran QRIS (jika ada opsi)
        try:
            qris_button = driver.find_element(By.XPATH, "//button[contains(text(), 'QRIS')]")
            qris_button.click()
        except:
            print("Tombol QRIS tidak ditemukan.")
        
        # Tunggu beberapa detik sebelum menutup browser
        time.sleep(5)
        
    finally:
        driver.quit()

# Contoh penggunaan
fill_saweria_form(
    url="https://saweria.co/habibiezz",
    amount=10000,  # Minimal Rp10.000 untuk QRIS
    name="User Test",
    email="user@example.com",
    message="Test donasi otomatis"
)
