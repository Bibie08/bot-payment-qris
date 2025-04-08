import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types

# Token bot dari BotFather
TOKEN = "7906182534:AAEcmieckSza4Sf8yXa2gQMBVWjScSmZiws"
SAWERIA_URL = "https://saweria.co/habibiezz"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Fungsi untuk submit form dan mendapatkan QRIS
async def generate_qris(nominal):
    session = requests.Session()
    
    # Ambil halaman form Saweria
    response = session.get(SAWERIA_URL)
    if response.status_code != 200:
        return None

    # Ambil token CSRF dari form
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "_token"}).get("value")

    # Data untuk form
    form_data = {
        "_token": csrf_token,
        "amount": nominal,
        "name": "Pembayaran Bot",
        "email": "bot@saweria.co",
        "message": "Pembayaran otomatis",
        "agree_terms": "on",
    }

    # Kirim form
    submit_url = SAWERIA_URL + "/donate"
    submit_response = session.post(submit_url, data=form_data)

    # Cek apakah berhasil
    if submit_response.status_code == 200:
        # Coba cari QRIS di halaman hasil
        soup = BeautifulSoup(submit_response.text, "html.parser")
        qris_img = soup.find("img", {"alt": "QRIS"})
        if qris_img:
            return qris_img["src"]

    return None

# Command /start
@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    await message.answer("Halo! Silakan ketik nominal yang ingin kamu bayar.")

# Menangani input nominal
@dp.message(lambda message: message.text.isdigit())
async def handle_payment(message: types.Message):
    nominal = int(message.text)
    qris_link = await generate_qris(nominal)

    if qris_link:
        await message.answer_photo(qris_link, caption=f"Silakan bayar dengan QRIS berikut (Rp {nominal})")
    else:
        await message.answer("Gagal membuat QRIS. Coba lagi.")

# Menjalankan bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
