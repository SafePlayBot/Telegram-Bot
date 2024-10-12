import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token (to be set as an environment variable)
TOKEN = os.environ.get('BOT_TOKEN')

# Welcome message for Social Casino
WELCOME_MESSAGE = """Your ultimate social games guide

🎁 Play for free 🏆 Top social games 🌍 VPN Friendly – Play from Anywhere 🔒 Safe and Secure

Link: https://miniclip.com/"""

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Welcome message triggered")
    try:
        await update.message.reply_text(WELCOME_MESSAGE)
        logger.info("Welcome message sent successfully")
    except Exception as e:
        logger.error(f"Error in welcome message: {str(e)}")

async def main() -> None:
    # Set up the bot application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", welcome))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, welcome))

    # Start the application with polling
    await application.run_polling()

# Run the bot using the appropriate method for the environment
if __name__ == '__main__':
    import asyncio
    # Use run_async if there is already a running event loop
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError as e:
        if str(e) == "no running event loop":
            asyncio.run(main())  # Use run only if there is no running event loop
        else:
            logger.error(f"Unexpected RuntimeError: {str(e)}")
