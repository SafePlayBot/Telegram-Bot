import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ChatMemberHandler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Welcome message triggered")
    try:
        keyboard = [
            [InlineKeyboardButton("Activate Bot", callback_data='activate'),
             InlineKeyboardButton("Deactivate Bot", callback_data='deactivate')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.effective_chat.send_message(WELCOME_MESSAGE, reply_markup=reply_markup)
        logger.info("Welcome message sent successfully")
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
            await query.edit_message_text(text="Bot deactivated. Restart the bot to activate again.")
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

async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    # If the bot was added to a group or a user started a conversation with it
    if not was_member and is_member:
        await send_welcome(update, context)

def extract_status_change(chat_member_update):
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        "member",
        "creator",
        "administrator",
    ] or (old_status == "restricted" and old_is_member is True)
    is_member = new_status in [
        "member",
        "creator",
        "administrator",
    ] or (new_status == "restricted" and new_is_member is True)

    return was_member, is_member

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Handler for /start command (as a fallback)
    application.add_handler(CommandHandler("start", send_welcome))
    
    # Handler for button callbacks
    application.add_handler(CallbackQueryHandler(button_callback))

    # Handler to track when the bot is added to a chat or when a user starts a conversation
    application.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
