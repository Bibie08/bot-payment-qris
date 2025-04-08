import asyncio
import requests
from aiogram import Bot, Dispatcher, types

# Token bot dari BotFather
TOKEN = "7906182534:AAEcmieckSza4Sf8yXa2gQMBVWjScSmZiws"
SAWERIA_USERNAME = "https://saweria.co/habibiezz"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Fungsi untuk membuat QRIS otomatis dari Saweria
async def generate_qris(nominal):
    url = "https://saweria.co/api/create_qris"  # Pastikan URL ini benar
    data = {
        "username": SAWERIA_USERNAME,
        "amount": nominal,
        "name": "User Bot",
        "email": "bot@saweria.co",
        "message": "Pembayaran otomatis",
        "agree_terms": True
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        qris_url = response.json().get("qris_url")
        return qris_url
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
        await message.answer(f"Silakan bayar dengan QRIS berikut:\n{qris_link}")
    else:
        await message.answer("Gagal membuat QRIS. Coba lagi.")

# Menjalankan bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
