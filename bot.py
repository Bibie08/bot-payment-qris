import asyncio
import qrcode
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
import os

# Ganti dengan token bot dari BotFather
TOKEN = "7906182534:AAEcmieckSza4Sf8yXa2gQMBVWjScSmZiws"
SAWERIA_URL = "https://saweria.co/habibiezz"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Fungsi buat QR Code
def generate_qr(data, filename="qris.png"):
    qr = qrcode.make(data)
    qr.save(filename)

# Respon ketika user mengirim /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Halo! Silakan ketik /bayar <jumlah> untuk membayar.\n\nContoh: `/bayar 15000`")

# Respon untuk pembayaran
@dp.message(Command("bayar"))
async def bayar(message: Message):
    args = message.text.split()
    
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Gunakan format: `/bayar 15000` (nominal angka)")
        return

    jumlah = int(args[1])
    if jumlah < 1000:  # Minimal 1000 biar masuk akal
        await message.answer("Minimal pembayaran adalah Rp1.000.")
        return

    # Buat link pembayaran Saweria dengan nominal yang dipilih
    link_pembayaran = f"{SAWERIA_URL}?nominal={jumlah}"

    # Generate QR dari link pembayaran
    generate_qr(link_pembayaran)

    # Kirim gambar QR ke user
    with open("qris.png", "rb") as photo:
        await message.answer_photo(photo, caption=f"Scan QR ini untuk membayar Rp{jumlah:,}!\n\nAtau klik link: {link_pembayaran}")

async def main():
    # Mulai polling bot
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
