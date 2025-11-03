import os
import qrcode
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
UPI_ID = os.getenv("UPI_ID")
PRODUCT_NAME = os.getenv("PRODUCT_NAME")
AMOUNT = os.getenv("AMOUNT")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # your chat ID

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Pay Now 💰", callback_data="pay_now")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Welcome! You can pay ₹{AMOUNT} for {PRODUCT_NAME}.",
        reply_markup=reply_markup
    )

# Handle button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "pay_now":
        upi_url = f"upi://pay?pa={UPI_ID}&pn={PRODUCT_NAME}&am={AMOUNT}&cu=INR"
        qr_img = qrcode.make(upi_url)
        qr_img.save("payment.png")

        keyboard = [[InlineKeyboardButton("✅ Payment Done", callback_data="payment_done")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_photo(
            photo=open("payment.png", "rb"),
            caption=f"📲 Scan this QR to pay ₹{AMOUNT}\n\nOr tap below:\n{upi_url}",
            reply_markup=reply_markup
        )

    elif query.data == "payment_done":
        user = query.from_user
        await query.message.reply_text("✅ Thank you! Your payment confirmation has been sent to admin.")
        # Send notification to admin
        if ADMIN_CHAT_ID:
            msg = f"💸 Payment confirmation received!\n👤 From: {user.full_name} (@{user.username})\n🪙 Amount: ₹{AMOUNT}"
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)

# Run bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))

    print("✅ Bot started. Waiting for messages...")
    app.run_polling()

if __name__ == "__main__":
    main()



