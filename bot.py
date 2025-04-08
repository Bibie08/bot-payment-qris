import asyncio
import qrcode
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

# Load token dari file .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
SAWERIA_URL = "https://saweria.co/habibiezz"
ADMIN_ID = os.getenv("ADMIN_ID")  # Ganti dengan ID admin

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Daftar produk
PRODUCTS = {
    "1": {"name": "Produk A", "price": 10000},
    "2": {"name": "Produk B", "price": 20000},
    "3": {"name": "Produk C", "price": 30000},
}

# Fungsi buat QR Code
def generate_qr(data, filename="qris.png"):
    qr = qrcode.make(data)
    qr.save(filename)

# Menu utama
@dp.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{product['name']} - Rp{product['price']}", callback_data=f"order_{key}")]
        for key, product in PRODUCTS.items()
    ])
    await message.answer("Silakan pilih produk:", reply_markup=keyboard)


# Menangani order
@dp.callback_query()
async def handle_order(callback: types.CallbackQuery):
    data = callback.data.split("_")
    if data[0] == "order":
        product_id = data[1]
        product = PRODUCTS.get(product_id)
        if product:
            jumlah = product["price"]
            link_pembayaran = f"{SAWERIA_URL}?nominal={jumlah}"
            generate_qr(link_pembayaran)
            
            with open("qris.png", "rb") as photo:
                await callback.message.answer_photo(photo, caption=f"Scan QR ini untuk membayar {product['name']} - Rp{jumlah:,}!")
                
            # Kirim notifikasi ke admin
            if ADMIN_ID:
                await bot.send_message(ADMIN_ID, f"Pesanan Baru! \n{callback.from_user.full_name} membeli {product['name']} seharga Rp{jumlah:,}")
    await callback.answer()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
