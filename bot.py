import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaAnimation
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import asyncio
from aiohttp import web

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token (to be set as an environment variable)
TOKEN = os.environ.get('BOT_TOKEN')

# Port (to be set as an environment variable or use default)
PORT = int(os.environ.get('PORT', 4323))

# GIF URL
GIF_URL = "https://media1.tenor.com/m/Y5vmrdIrr4wAAAAC/mehdi-casino.gif"

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
        # Send the GIF
        await update.message.reply_animation(GIF_URL)
        
        # Send the welcome message with buttons
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

async def web_app():
    # Set up a simple web app
    app = web.Application()
    app.router.add_get("/", lambda request: web.Response(text="Telegram Bot is running!"))
    return app

async def main() -> None:
    # Set up the bot application
    application = Application.builder().token(TOKEN).build()

    # Handler for /start command
    application.add_handler(CommandHandler("start", welcome))
    
    # Handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, welcome))
    
    # Handler for button callbacks
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot
    await application.initialize()
    await application.start()
    
    # Set up and start the web app
    app = await web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

    logger.info(f"Server started on port {PORT}")

    # Run the bot until the user presses Ctrl-C
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main())
