import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests

# Konfigurasi logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token bot Telegram dari environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SAWERIA_URL = "https://saweria.co/habibiezz"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Halo! Kirim nominal untuk membuat QRIS pembayaran.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text.isdigit():
        nominal = int(text)
        qris_url = generate_qris(nominal)
        await update.message.reply_text(f"Berikut QRIS untuk pembayaran Rp {nominal}\n{qris_url}")
    else:
        await update.message.reply_text("Silakan kirim angka saja untuk nominal pembayaran.")


def generate_qris(amount):
    payload = {
        "amount": amount,
        "name": "User",
        "email": "user@example.com",
        "message": "Pembayaran via bot",
    }
    response = requests.post(SAWERIA_URL, data=payload)
    if response.status_code == 200:
        return response.url  # Sesuaikan dengan format URL QRIS yang dihasilkan
    return "Gagal membuat QRIS. Coba lagi."


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot telah berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
