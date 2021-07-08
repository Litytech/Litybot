import logging
from telegram.ext import Updater, CommandHandler
from litybot import Litybot
from dotenv import dotenv_values

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    litybot = Litybot()
    token = dotenv_values(".env").get("TOKEN")
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", litybot.start))
    dispatcher.add_handler(CommandHandler("help", litybot.help_command))
    dispatcher.add_handler(CommandHandler("inspirame", litybot.inspireme))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()