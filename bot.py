from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Ganti dengan token bot dari BotFather
TOKEN = "7906182534:AAEcmieckSza4Sf8yXa2gQMBVWjScSmZiws"

# Ganti dengan link Saweria kamu
SAWERIA_URL = "https://saweria.co/habibiezz"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Respon ketika user mengirim /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Halo! Silakan ketik /bayar untuk melakukan pembayaran.")

# Respon untuk pembayaran
@dp.message_handler(commands=["bayar"])
async def bayar(message: types.Message):
    jumlah = 10000  # Nominal default, bisa diubah
    link_pembayaran = f"{SAWERIA_URL}?nominal={jumlah}"
    await message.reply(f"Silakan lakukan pembayaran dengan QRIS:\n{link_pembayaran}")

if __name__ == "__main__":
    executor.start_polling(dp)
