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

# New command responses
RESPONSES = {
    'license': """Online gambling licenses ensure fair play and safety for players. Here are some of the most recognized licenses:

MGA (Malta Gaming Authority): A reputable license known for strict regulations.
Curacao: Common among online casinos; easier to obtain but less stringent.
Estonia: Offers high standards of compliance and security.
Isle of Man: Known for robust player protection laws.
UKGC (UK Gambling Commission): One of the most stringent licenses globally.
Always check if a casino holds a valid license before playing!""",

    'crypto': """Crypto casinos let you gamble using cryptocurrencies like Bitcoin, Ethereum, and Litecoin.
What is crypto? Digital currency that offers privacy and faster transactions.
What do you need? A crypto wallet and funds in Bitcoin or other supported cryptocurrencies.
Why choose crypto casinos?

Faster deposits and withdrawals.
Anonymity for players.
Access to casinos worldwide without traditional banking restrictions.
Make sure to gamble responsibly!""",

    'providers': """Here's a list of popular slot providers you'll find in online casinos:
Play'n GO, Hacksaw Gaming, Evolution Gaming, Red Tiger, Pragmatic Play, NetEnt, Microgaming, Blueprint Gaming, Yggdrasil, Quickspin, Big Time Gaming, and many more!
Want details on specific providers? Ask me!""",

    'bonuses': """Online casinos offer these bonuses:

Welcome Bonus: Extra money or free spins on your first deposit.
No-Deposit Bonus: Play without depositing; usually small but risk-free.
Free Spins: Spin slots for free and keep the winnings.
Cashback: Get a percentage of your losses back.
Loyalty Rewards: Exclusive perks for regular players.
Always read the terms and conditions of bonuses!""",

    'paymentmethods': """Common payment methods for online gambling include:

E-Wallets: Skrill, Neteller, PayPal.
Cryptocurrency: Bitcoin, Ethereum, Litecoin.
Prepaid Cards: Paysafecard.
Bank Transfers: Direct deposits and withdrawals.
Credit/Debit Cards: Visa, Mastercard, Maestro.
Choose a payment method that ensures quick and secure transactions.""",

    'responsiblegaming': """Responsible gambling is important for your well-being. Here are some tips:

Set a budget and stick to it.
Take breaks and avoid chasing losses.
Use self-exclusion tools if needed.
Know the signs of problem gambling: anxiety, financial strain, or losing control.
Seek help: Organizations like GamCare and Gambling Therapy are here to support you.
Stay safe and gamble responsibly!""",

    'games': """Popular online gambling games:

Slots: Easy to play with various themes.
Blackjack: Skill-based card game with low house edge.
Roulette: Bet on numbers, colors, or sections of the wheel.
Poker: Strategy-based card game with tournaments.
Live Dealer Games: Interact with real dealers in real-time.
Each game has its rules and strategies. Learn them to improve your chances of winning!""",

    'rttpayouts': """RTP (Return to Player) is the percentage of total money wagered that a game pays back to players over time.
For example:

Slots often have RTPs between 92%-98%.
Higher RTP means better long-term payouts.
Always check the RTP of a game before playing and aim for games with higher percentages.""",

    'casinoreviews': """Looking for a reliable casino? Here are some trusted ones:

Casino A: High payout rates, fast withdrawals, and excellent customer support.
Casino B: Huge game selection and generous bonuses.
Casino C: Focused on crypto players with lightning-fast transactions.
Want personalized recommendations? Let me know what you're looking for!""",

    'trends': """Stay ahead in the gambling world! Latest trends include:

Crash Games: A fast-growing casino game type where players cash out before a multiplier crashes.
Provably Fair Games: Crypto-powered fairness verification.
VR Casinos: Virtual reality for immersive gambling.
New Slot Mechanics: Such as Megaways and Cluster Pays.
Follow the trends to find unique and exciting gambling experiences!"""
}

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Welcome message triggered")
    try:
        await update.message.reply_text(WELCOME_MESSAGE)
        logger.info("Welcome message sent successfully")
    except Exception as e:
        logger.error(f"Error in welcome message: {str(e)}")

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text[1:].lower()  # Remove the '/' and convert to lowercase
    if command in RESPONSES:
        await update.message.reply_text(RESPONSES[command])
    else:
        await update.message.reply_text("Sorry, I don't recognize that command.")

def main() -> None:
    # Set up the bot application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", welcome))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, welcome))

    # Add handlers for new commands
    for command in RESPONSES.keys():
        application.add_handler(CommandHandler(command, handle_command))

    # Start the application with polling
    application.run_polling()

# Directly run the main function
if __name__ == '__main__':
    main()
