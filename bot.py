import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandObject

# Ganti dengan token bot dari BotFather
TOKEN = "7906182534:AAEcmieckSza4Sf8yXa2gQMBVWjScSmZiws"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Respon ketika user mengirim /start
async def start(message: types.Message):
    await message.answer("Halo! Silakan ketik /bayar <jumlah> untuk membayar.\n\nContoh: `/bayar 15000`")

# Respon untuk pembayaran
async def bayar(message: types.Message, command: CommandObject):
    if not command.args or not command.args.isdigit():
        await message.answer("Gunakan format: `/bayar 15000` (nominal angka)")
        return

    jumlah = int(command.args)
    if jumlah < 1000:  # Minimal 1000 biar masuk akal
        await message.answer("Minimal pembayaran adalah Rp1.000.")
        return

    # Cek apakah ada QRIS dengan nominal yang diminta
    qr_filename = f"qris_{jumlah}.png"  # Misal: qris_10000.png
    if not os.path.exists(qr_filename):
        await message.answer("QRIS untuk nominal ini belum tersedia. Coba nominal lain.")
        return

    # Kirim gambar QRIS
    with open(qr_filename, "rb") as photo:
        await message.answer_photo(photo, caption=f"Scan QR ini untuk membayar Rp{jumlah:,}!")

async def main():
    dp.message.register(start, CommandObject("start"))
    dp.message.register(bayar, CommandObject("bayar"))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
