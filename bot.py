from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from saweria_autofill import isi_form_saweria

TOKEN = "7906182534:AAEcmieckSza4Sf8yXa2gQMBVWjScSmZiws"

def handle_payment(update: Update, context: CallbackContext):
    try:
        nominal = int(update.message.text)  # Ambil nominal dari pesan user
        if nominal < 1000:
            update.message.reply_text("Minimal pembayaran adalah Rp 1.000")
            return
        
        update.message.reply_text(f"Memproses pembayaran Rp {nominal}...")
        
        # Panggil fungsi isi_form_saweria() untuk mendapatkan QRIS
        qris_image = isi_form_saweria(nominal)

        if qris_image:
            update.message.reply_photo(photo=qris_image, caption="Berikut adalah QRIS untuk pembayaran Anda.")
        else:
            update.message.reply_text("Gagal mendapatkan QRIS, coba lagi nanti.")
    
    except ValueError:
        update.message.reply_text("Mohon masukkan nominal yang valid.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_payment))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
