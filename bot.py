import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask, request

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token (to be set as an environment variable)
TOKEN = os.environ.get('BOT_TOKEN')

# Welcome message for Social Casino
WELCOME_MESSAGE = """🎉 Welcome to Your Ultimate Social Games Guide! 🎉

🎁 Play for free
🏆 Top social games
🌍 VPN Friendly – Play from Anywhere
🔒 Safe and Secure

Start your adventure: https://miniclip.com/

Type /help to see all available commands!"""

# Help message
HELP_MESSAGE = """Available commands:

/start - Get the welcome message
/license - Information about online gambling licenses
/crypto - Learn about crypto casinos
/providers - List of popular slot providers
/bonuses - Types of casino bonuses
/paymentmethods - Payment options for online gambling
/responsiblegaming - Tips for responsible gambling
/games - Popular online gambling games
/rttpayouts - Explanation of RTP (Return to Player)
/casinoreviews - Reviews of trusted casinos
/trends - Latest trends in online gambling"""

# Command responses
RESPONSES = {
    'license': """🏛️ Online Gambling Licenses: Ensuring Fair Play and Safety 🛡️

Recognized Licenses:
🇲🇹 MGA (Malta Gaming Authority): Reputable with strict regulations
🇨🇼 Curacao: Common and easier to obtain, less stringent
🇪🇪 Estonia: High standards of compliance and security
🏝️ Isle of Man: Known for robust player protection laws
🇬🇧 UKGC (UK Gambling Commission): One of the most stringent globally

💡 Pro Tip: Always verify a casino's license before playing!""",

    'crypto': """🔐 Crypto Casinos: Revolutionizing Online Gambling 🚀

What is Crypto? 
💻 Digital currency offering privacy and faster transactions
🌐 Requires a crypto wallet and supported cryptocurrencies

Advantages of Crypto Casinos:
⚡ Faster deposits and withdrawals
🕵️‍♂️ Enhanced player anonymity
🌍 Access to casinos worldwide without traditional banking restrictions

🎰 Remember: Gamble responsibly, even with crypto!""",

    'providers': """🎰 Top Slot Providers in Online Casinos 🏆

Popular Developers:
✨ Play'n GO
🎲 Hacksaw Gaming
🌈 Evolution Gaming
🐯 Red Tiger
💥 Pragmatic Play
🃏 NetEnt
🚀 Microgaming
🔷 Blueprint Gaming
🌳 Yggdrasil
⚡ Quickspin
💎 Big Time Gaming

🔍 Want to know more about a specific provider? Just ask!""",

    'bonuses': """🎁 Online Casino Bonuses Explained 💰

Types of Bonuses:
🆕 Welcome Bonus: Extra funds or free spins on your first deposit
🆓 No-Deposit Bonus: Play without depositing; usually small but risk-free
🌀 Free Spins: Spin slots for free and keep winnings
💸 Cashback: Get a percentage of your losses back
🏅 Loyalty Rewards: Exclusive perks for regular players

⚠️ Important: Always read the terms and conditions of bonuses!""",

    'paymentmethods': """💳 Payment Methods for Online Gambling 🏧

Popular Options:
💻 E-Wallets: Skrill, Neteller, PayPal
₿ Cryptocurrency: Bitcoin, Ethereum, Litecoin
💵 Prepaid Cards: Paysafecard
🏦 Bank Transfers: Direct deposits and withdrawals
💳 Credit/Debit Cards: Visa, Mastercard, Maestro

🔒 Choose a method that ensures quick and secure transactions!""",

    'responsiblegaming': """🛑 Responsible Gambling: Protecting Your Well-being 🤲

Essential Tips:
💰 Set a budget and stick to it
⏰ Take regular breaks from gambling
🚫 Avoid chasing losses
🚩 Recognize signs of problem gambling: anxiety, financial strain, loss of control

Support Resources:
🆘 GamCare
🌈 Gambling Therapy
📞 Local support hotlines

Remember: Your well-being comes first! Stay safe and enjoy responsibly.""",

    'games': """🎮 Popular Online Gambling Games 🌟

Game Varieties:
🎰 Slots: Easy to play with various themes
♠️ Blackjack: Skill-based card game with low house edge
🎲 Roulette: Bet on numbers, colors, or sections of the wheel
🃏 Poker: Strategy-based card game with tournaments
👥 Live Dealer Games: Interact with real dealers in real-time

🏆 Tip: Learn the rules and strategies to improve your chances!""",

    'rttpayouts': """📊 Understanding RTP (Return to Player) 💡

What is RTP?
🔢 Percentage of total wagered money a game pays back over time
📈 Higher RTP means better long-term payouts

Key Points:
🎰 Slots typically have RTPs between 92%-98%
🏆 Aim for games with higher RTP percentages
⚖️ RTP is a long-term average, not a guarantee for every session

💡 Always check a game's RTP before playing!""",

    'casinoreviews': """🕵️‍♂️ Trusted Casino Reviews 🌟

Top Picks:
🥇 Casino A: High payout rates, fast withdrawals, excellent support
🏆 Casino B: Huge game selection and generous bonuses
💎 Casino C: Crypto-focused with lightning-fast transactions

🔍 Need a personalized recommendation? Let us know your preferences!""",

    'trends': """🚀 Latest Trends in Online Gambling 🔮

Exciting Innovations:
💥 Crash Games: Fast-paced with increasing multipliers
🔐 Provably Fair Games: Crypto-powered fairness verification
🕶️ VR Casinos: Immersive virtual reality experiences
🎰 New Slot Mechanics: Megaways, Cluster Pays, and more

Stay ahead of the curve and discover unique gambling experiences!"""
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Start command triggered")
    try:
        await update.message.reply_text(WELCOME_MESSAGE)
        logger.info("Welcome message sent successfully")
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Help command triggered")
    try:
        await update.message.reply_text(HELP_MESSAGE)
        logger.info("Help message sent successfully")
    except Exception as e:
        logger.error(f"Error in help command: {str(e)}")

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text[1:].lower()  # Remove the '/' and convert to lowercase
    logger.info(f"Command received: {command}")
    if command in RESPONSES:
        try:
            await update.message.reply_text(RESPONSES[command])
            logger.info(f"Response sent for command: {command}")
        except Exception as e:
            logger.error(f"Error sending response for command {command}: {str(e)}")
    else:
        await update.message.reply_text("Sorry, I don't recognize that command. Type /help to see available commands.")
        logger.warning(f"Unrecognized command received: {command}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Non-command message received")
    await update.message.reply_text("I'm designed to respond to specific commands. Type /help to see what I can do!")

# Set up the bot application
application = ApplicationBuilder().token(TOKEN).build()

# Add handlers for commands and messages
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Add handlers for all other commands
for command in RESPONSES.keys():
    application.add_handler(CommandHandler(command, handle_command))

# Add a general message handler
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Set up Flask app for webhook
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    try:
        logger.info("Webhook received")
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.process_update(update)
        return 'OK'
    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}")
        return 'Error', 500

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/test', methods=['GET'])
def test():
    return 'Bot is running!'

if __name__ == '__main__':
    # Initialize your bot application here
    application.initialize()
    # Start the Flask app
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
