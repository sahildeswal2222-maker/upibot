import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import qrcode
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Pay Now 💰", callback_data="pay")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! Click below to pay.", reply_markup=reply_markup)

def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "pay":
        upi_url = "upi://pay?pa=8287366219@pthdc@upi&pn=PaidService&am=10&cu=INR"
        qr_img = qrcode.make(upi_url)

        bio = BytesIO()
        bio.name = "payment_qr.png"
        qr_img.save(bio, "PNG")
        bio.seek(0)

        query.message.reply_photo(photo=bio, caption="Scan to pay via UPI")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))

    logger.info("✅ Bot started. Waiting for messages...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()


