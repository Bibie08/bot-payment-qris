import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Ganti dengan token bot dari BotFather
TOKEN = "7906182534:AAEcmieckSza4Sf8yXa2gQMBVWjScSmZiws"
SAWERIA_URL = "https://saweria.co/habibiezz"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Respon ketika user mengirim /start
async def start(message: types.Message):
    await message.answer("Halo! Silakan ketik /bayar untuk melakukan pembayaran.")

# Respon untuk pembayaran
async def bayar(message: types.Message):
    jumlah = 10000  # Nominal default
    link_pembayaran = f"{SAWERIA_URL}?nominal={jumlah}"
    await message.answer(f"Silakan lakukan pembayaran dengan QRIS:\n{link_pembayaran}")

async def main():
    # Mendaftarkan handler
    dp.message.register(start, Command("start"))
    dp.message.register(bayar, Command("bayar"))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
