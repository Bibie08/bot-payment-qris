import qrcode
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
SAWERIA_USERNAME = "habibiezz"  # Ganti dengan username Saweria kamu
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Halo! Masukkan nominal pembayaran yang ingin kamu buat QRIS-nya.")

@dp.message()
async def generate_qris(message: types.Message):
    try:
        jumlah = int(message.text)
        saweria_link = f"https://saweria.co/{SAWERIA_USERNAME}?nominal={jumlah}"
        
        # Generate QR Code
        qr = qrcode.make(saweria_link)
        qr_path = f"qris_{message.from_user.id}.png"
        qr.save(qr_path)
        
        # Kirim QR Code ke user
        qr_file = FSInputFile(qr_path)
        await message.answer_photo(photo=qr_file, caption=f"Scan QRIS untuk membayar Rp{jumlah}")
        
        # Hapus file setelah dikirim
        os.remove(qr_path)
    except ValueError:
        await message.answer("Silakan masukkan angka yang valid.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
