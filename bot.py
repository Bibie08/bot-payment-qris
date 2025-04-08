import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from saweria_scraper import generate_qris  # Menggunakan scraper Saweria

# Load .env file
load_dotenv()

# Konfigurasi logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ambil token bot dari environment variable
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("TOKEN tidak ditemukan! Pastikan sudah diset di Railway.")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Halo! Kirim nominal untuk membuat QRIS pembayaran.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text.isdigit():
        nominal = int(text)
        qris_url = generate_qris(nominal)
        if qris_url:
            await update.message.reply_text(f"🔗 QRIS untuk pembayaran Rp {nominal}:\n{qris_url}")
        else:
            await update.message.reply_text("⚠️ Gagal membuat QRIS. Coba lagi nanti.")
    else:
        await update.message.reply_text("❌ Masukkan angka yang valid untuk nominal pembayaran.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🚀 Bot telah berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
