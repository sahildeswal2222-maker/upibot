import logging
import os
from io import BytesIO
import qrcode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = "923903808"  # Your Telegram ID

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing in environment variables!")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ /start command
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Pay via QR 💳", callback_data="pay_qr")],
        [InlineKeyboardButton("Pay via UPI ID 📲", callback_data="pay_upi")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "👋 Welcome!\nChoose how you want to pay:",
        reply_markup=reply_markup
    )

    # ✅ notify admin that a user started bot
    user = update.effective_user
    context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"✅ User started bot: @{user.username} (ID: {user.id})"
    )

# ✅ Button handler
def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user = update.effective_user

    if query.data == "pay_qr":
        upi_url = "upi://pay?pa=8287366219@pthdfc&pn=PaidService&am=10&cu=INR"
        qr_img = qrcode.make(upi_url)

        bio = BytesIO()
        bio.name = "payment_qr.png"
        qr_img.save(bio, "PNG")
        bio.seek(0)

        query.message.reply_photo(photo=bio, caption="✅ Scan this QR to pay.")

        # ✅ notify admin
        context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"💰 User @{user.username} clicked Pay via QR"
        )

    if query.data == "pay_upi":
        query.message.reply_text("📲 UPI ID: **8287366219@pthdfc**\nSend payment and reply with screenshot ✅",
                                 parse_mode="Markdown")

        context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"💰 User @{user.username} clicked Pay via UPI ID"
        )

# ✅ Forward user messages to admin
def forward_to_admin(update: Update, context: CallbackContext):
    user = update.effective_user
    text = update.message.text

    context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📩 Message from @{user.username}: {text}"
    )

# ✅ Run bot
def run_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_to_admin))

    updater.start_polling()
    updater.idle()

# ✅ Flask (Render free requirement)
from flask import Flask
import threading
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
