import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask, request

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

async def setup_webhook(app, application):
    # Set the webhook
    webhook_url = f'https://{os.environ.get("RENDER_EXTERNAL_HOSTNAME")}/{TOKEN}'
    await application.bot.set_webhook(url=webhook_url)
    logger.info(f"Webhook set to {webhook_url}")

    @app.route('/' + TOKEN, methods=['POST'])
    def webhook():
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.process_update(update))
        return 'OK'

    @app.route('/')
    def index():
        return 'Hello, World!'

def main() -> None:
    # Set up the bot application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", welcome))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, welcome))

    # Create a Flask app
    app = Flask(__name__)

    # Set up the webhook
    asyncio.run(setup_webhook(app, application))

    # Run the Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8443)))

# Directly run the main function
if __name__ == '__main__':
    main()
