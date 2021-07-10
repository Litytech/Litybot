import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from litybot import Litybot
from dotenv import dotenv_values

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

SUMMARY, DATE, TIMES, GUESTS = range(4)

def main() -> None:
    """
        Start the bot.
        Author: José Cruz
        Version 1.1.0
    """
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
    
    # Commands group for generate an event - multiple answer in telegram
    meet_handler = ConversationHandler(
        entry_points = [CommandHandler("reunion", litybot.createMeet)],
        states = {
            SUMMARY: [MessageHandler(Filters.text & ~Filters.command, litybot.setEventName)],
            DATE: [MessageHandler(Filters.regex('^([2][0][2-9][0-9][-][0-1][1-9][-][0-3][0-9])$'), litybot.setEventDate)],
            TIMES: [MessageHandler(Filters.regex('^(([0]?[1-9]|[1][0-2])[:][0-9]{2}[ ]((am|pm)|(AM|PM))[ ][-][ ]([0]?[1-9]|[1][0-2])[:][0-9]{2}[ ]((am|pm)|(AM|PM)))$'), litybot.setEventTimes)],
            GUESTS: [MessageHandler(Filters.regex("^([a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?[,]?)+$"), litybot.setGuests), CommandHandler('default', litybot.defaultGuests)]
        },
        fallbacks = [CommandHandler("cancelar", litybot.cancel)]
    )

    dispatcher.add_handler(meet_handler)

    # dispatcher.add_handler(CommandHandler("reunion", litybot.programMeet))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, litybot.echo))



    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()