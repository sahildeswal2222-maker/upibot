import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import qrcode
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # Add this in Render Variables
UPI_ID = "8287366219@pthdfc"
PRODUCT_NAME = "Call Service"
AMOUNT = "300"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ✅ Start button
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💳 Pay by QR", callback_data="pay_qr")],
        [InlineKeyboardButton("📲 Pay by UPI ID", callback_data="pay_upi")],
        [InlineKeyboardButton("✅ Send Payment Screenshot", callback_data="send_ss")],
        [InlineKeyboardButton("🎧 Contact Support", url="https://t.me/Lakshikaa07")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "👋 Welcome!\nChoose an option below:",
        reply_markup=reply_markup
    )


# ✅ Handle button clicks
def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # ✅ Send QR
    if query.data == "pay_qr":
        upi_url = f"upi://pay?pa={UPI_ID}&pn={PRODUCT_NAME}&am={AMOUNT}&cu=INR"
        qr_img = qrcode.make(upi_url)

        bio = BytesIO()
        bio.name = "payment_qr.png"
        qr_img.save(bio, "PNG")
        bio.seek(0)

        query.message.reply_photo(photo=bio, caption=f"Scan & Pay ₹{AMOUNT}")

    # ✅ Show UPI ID
    elif query.data == "pay_upi":
        query.message.reply_text(
            f"📲 Pay using UPI ID:\n\n`{UPI_ID}`\n\nAmount: ₹{AMOUNT}",
            parse_mode="Markdown"
        )

    # ✅ Ask for screenshot
    elif query.data == "send_ss":
        query.message.reply_text("📤 Send payment screenshot here.")
        

# ✅ When user sends screenshot
def handle_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    file_id = update.message.photo[-1].file_id

    # ✅ Forward screenshot to admin
    context.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=file_id,
        caption=f"🔥 Payment screenshot from @{user.username} (User ID: {user.id})"
    )

    # ✅ Give service button
    keyboard = [
        [InlineKeyboardButton("📦 Get Service Now", url="https://t.me/Lakshikaa07")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "✅ Screenshot received!\nWe will verify shortly.\nClick below to get service:",
        reply_markup=reply_markup
    )


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    logger.info("✅ Bot started & running")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
