import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Ganti dengan token bot Telegram kamu
TOKEN = "7906182534:AAEcmieckSza4Sf8yXa2gQMBVWjScSmZiws"
SAWERIA_URL = "https://saweria.co/habibiezz"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def generate_qris(nominal):
    """
    Fungsi untuk mengisi form Saweria secara otomatis dan mendapatkan QRIS.
    """
    form_data = {
        "nominal": nominal,
        "name": "Bot User",
        "email": "bot@saweria.co",
        "message": "Pembayaran otomatis via bot",
        "terms": "on",  # Menyetujui checkbox
    }
    
    response = requests.post(SAWERIA_URL, data=form_data)
    
    if response.status_code == 200:
        # Coba ekstrak URL QRIS dari respons
        qris_url = "https://saweria.co/qris_generated_example.png"  # Gantilah dengan cara parsing HTML jika diperlukan
        return qris_url
    else:
        return None

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Halo! Ketik /bayar untuk melakukan pembayaran.")

@dp.message_handler(commands=["bayar"])
async def bayar(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Rp 10.000", callback_data="pay_10000"))
    keyboard.add(InlineKeyboardButton(text="Rp 25.000", callback_data="pay_25000"))
    keyboard.add(InlineKeyboardButton(text="Rp 50.000", callback_data="pay_50000"))
    await message.reply("Pilih nominal pembayaran:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("pay_"))
async def process_payment(callback_query: types.CallbackQuery):
    nominal = int(callback_query.data.split("_")[1])
    await bot.answer_callback_query(callback_query.id)
    
    await bot.send_message(callback_query.from_user.id, "Sedang memproses pembayaran...")
    qris_url = await generate_qris(nominal)
    
    if qris_url:
        await bot.send_photo(callback_query.from_user.id, qris_url, caption=f"Silakan scan QRIS untuk membayar Rp {nominal}")
    else:
        await bot.send_message(callback_query.from_user.id, "Gagal mendapatkan QRIS. Coba lagi nanti.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
