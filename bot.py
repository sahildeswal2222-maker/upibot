import logging
import os
from io import BytesIO
import qrcode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# ✅ Load BOT TOKEN directly from Render Environment Variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not found! Add it in Render → Environment Variables.")

# ✅ Telegram logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ /start command
def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Pay Now 💰", callback_data="pay")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! Click below to pay.", reply_markup=reply_markup)

# ✅ Handle Pay button click
def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "pay":
        # ✅ FIX: Correct UPI URL
        upi_url = "upi://pay?pa=8287366219@pthdfc&pn=PaidService&am=10&cu=INR"

        qr_img = qrcode.make(upi_url)
        bio = BytesIO()
        bio.name = "payment_qr.png"
        qr_img.save(bio, "PNG")
        bio.seek(0)

        query.message.reply_photo(photo=bio, caption="✅ Scan to pay via UPI.")

# ✅ Telegram Bot Runner
def run_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))

    logger.info("🤖 Bot running...")
    updater.start_polling()
    updater.idle()

##############################
# ✅ Flask server (for Render FREE plan)
##############################

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram bot is running on Render free plan!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

##############################
# ✅ Start BOTH bot + Flask
##############################

if __name__ == "__main__":
    # Start Flask server in background
    threading.Thread(target=run_flask).start()

    # Start Telegram bot
    run_bot()






