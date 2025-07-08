import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
# Enable logging to see what's happening
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Replace with your actual bot token ---
TELEGRAM_BOT_TOKEN = os.getenv(BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! Send me any text message, and I'll echo it back to you.",
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echoes the user's text message back to them."""
    await update.message.reply_text(update.message.text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a help message when the /help command is issued."""
    await update.message.reply_text(
        "I'm a simple echo bot! Send me any text message, and I'll send it right back to you."
    )

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Register a message handler for all text messages that are not commands
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until you press Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
