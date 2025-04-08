import os
from dotenv import load_dotenv
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load .env file
load_dotenv()

# Konfigurasi logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ambil Token dari environment variable
TOKEN = os.getenv("BOT_TOKEN")
SAWERIA_URL = "https://saweria.co/habibiezz"

if not TOKEN:
    raise ValueError("TOKEN tidak ditemukan! Pastikan sudah diset di Railway.")

# Fungsi Start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Halo! Kirim nominal untuk membuat QRIS pembayaran.")

# Fungsi menangani pesan dari user
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text.isdigit():
        nominal = int(text)
        qris_url = generate_qris(nominal)
        if qris_url:
            await update.message.reply_text(f"Berikut QRIS untuk pembayaran Rp {nominal}\n{qris_url}")
        else:
            await update.message.reply_text("Gagal membuat QRIS. Silakan coba lagi.")
    else:
        await update.message.reply_text("Silakan kirim angka saja untuk nominal pembayaran.")

# Fungsi membuat QRIS (Menggunakan Requests)
def generate_qris(amount):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "amount": amount,
        "name": "User",
        "email": "user@example.com",
        "message": "Pembayaran via bot",
    }
    
    try:
        response = requests.post(SAWERIA_URL, data=payload, headers=headers)
        if response.status_code == 200:
            return response.url  # Sesuaikan dengan format URL QRIS yang dihasilkan
        else:
            logger.error(f"Error Saweria: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exception saat request ke Saweria: {e}")
        return None

# Fungsi utama menjalankan bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot telah berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
