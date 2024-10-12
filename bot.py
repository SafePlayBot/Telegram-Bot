import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token (to be set as an environment variable)
TOKEN = os.environ.get('BOT_TOKEN')

# GIF URL
GIF_URL = "https://media1.tenor.com/m/rDy3M2M3oroAAAAC/casino-casino-withdraw.gif"

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

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Welcome message triggered")
    try:
        await update.message.reply_animation(GIF_URL)
        keyboard = [
            [InlineKeyboardButton("Activate Bot", callback_data='activate'),
             InlineKeyboardButton("Deactivate Bot", callback_data='deactivate')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)
        logger.info("Welcome message and GIF sent successfully")
    except Exception as e:
        logger.error(f"Error in welcome message: {str(e)}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'activate':
            await query.edit_message_text(text=f"{WELCOME_MESSAGE}\n\n{BIG_OFFER}")
            await show_preferences(update, context)
        elif query.data == 'deactivate':
            await query.edit_message_text(text="Bot deactivated. Send any message to activate again.")
        elif query.data in PREFERENCES:
            await query.message.reply_text(PREFERENCES[query.data])
        logger.info(f"Button callback processed: {query.data}")
    except Exception as e:
        logger.error(f"Error in button callback: {str(e)}")

async def show_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        keyboard = [
            [InlineKeyboardButton("VPN", callback_data='VPN'),
             InlineKeyboardButton("INSTANT CASHOUT", callback_data='INSTANT_CASHOUT')],
            [InlineKeyboardButton("FREESPINS", callback_data='FREESPINS'),
             InlineKeyboardButton("DEPOSIT BONUS", callback_data='DEPOSIT_BONUS')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text("Choose your preferences:", reply_markup=reply_markup)
        logger.info("Preferences shown successfully")
    except Exception as e:
        logger.error(f"Error in show_preferences: {str(e)}")

def main() -> None:
    # Set up the bot application
    application = ApplicationBuilder().token(TOKEN).build()

    # Handler for /start command
    application.add_handler(CommandHandler("start", welcome))
    
    # Handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, welcome))
    
    # Handler for button callbacks
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot with polling
    application.run_polling()

if __name__ == '__main__':
    import asyncio

    # Get the current event loop and run the main function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
