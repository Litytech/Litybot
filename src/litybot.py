from telegram import Update, ForceReply
from telegram.ext import CallbackContext
from Json import Json

class Litybot:

    def __init__(self):
        pass        

    def start(self, update: Update, context: CallbackContext):
        """Send a message when the command /start is issued."""
        user = update.effective_user
        message = fr'Hola {user.mention_markdown_v2()}\!\
Estoy para ayudarte\.'
        update.message.reply_markdown_v2(
            message,
            reply_markup=ForceReply(selective=True),
        )

    def help_command(self, update: Update, context: CallbackContext):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def inspireme(self, update: Update, context: CallbackContext):
        "Send an insirational message to the user"
        json = Json()
        update.message.reply_text(json.randomInspire())

    def echo(self, update: Update, context: CallbackContext):
        """Echo the user message."""
        update.message.reply_text(update.message.text)