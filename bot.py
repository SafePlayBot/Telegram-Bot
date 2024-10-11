import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Bot token (to be set as an environment variable)
TOKEN = os.environ.get('BOT_TOKEN')

# Messages and offers
WELCOME_MESSAGE = "🎰Welcome to SafePlay, your guide to the world of safe Crypto Casinos"
BIG_OFFER = """Win Big at Kripty today!

⚡ Get a 100% Bonus on Your First Deposit!
💰 Enjoy Ultra-Fast Withdrawals
🪙 Benefit from Weekly Cashback and Perks
🌍 VPN Friendly – Play from Anywhere

Play now ➡️ http://bit.ly/kripty-casino"""

PREFERENCES = {
    'VPN': "The best VPN Casino\n\n💰 Enjoy Ultra-Fast Withdrawals 🪙 Benefit from Weekly Cashback and Perks 🌍\nPlay now ➡️ http://bit.ly/kripty-casino",
    'INSTANT_CASHOUT': "Instant Cashout Casino\n\n💰 Get your winnings instantly!\nPlay now ➡️ http://bit.ly/kripty-casino",
    'FREESPINS': "Free Spins Casino\n\n🎡 Enjoy tons of free spins!\nPlay now ➡️ http://bit.ly/kripty-casino",
    'DEPOSIT_BONUS': "Deposit Bonus Casino\n\n💼 Get the best deposit bonuses!\nPlay now ➡️ http://bit.ly/kripty-casino"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Activate Bot", callback_data='activate'),
         InlineKeyboardButton("Deactivate Bot", callback_data='deactivate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'activate':
        await query.edit_message_text(text=f"{WELCOME_MESSAGE}\n\n{BIG_OFFER}")
        await show_preferences(update, context)
    elif query.data == 'deactivate':
        await query.edit_message_text(text="Bot deactivated. Send /start to activate again.")
    elif query.data in PREFERENCES:
        await query.message.reply_text(PREFERENCES[query.data])

async def show_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("VPN", callback_data='VPN'),
         InlineKeyboardButton("INSTANT CASHOUT", callback_data='INSTANT_CASHOUT')],
        [InlineKeyboardButton("FREESPINS", callback_data='FREESPINS'),
         InlineKeyboardButton("DEPOSIT BONUS", callback_data='DEPOSIT_BONUS')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Choose your preferences:", reply_markup=reply_markup)

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Flask web server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = Thread(target=run_bot)
    bot_thread.start()

    # Run the Flask web server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
