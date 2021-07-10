from dotenv import dotenv_values
from telegram import Update, ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext.conversationhandler import ConversationHandler
from Json import Json
from calendarEvent import Event
from datetime import datetime, timedelta

SUMMARY, DATE, TIMES, GUESTS = range(4)

class Litybot:
    """
        Class with the logic for make the responses for the bot to the users
        Author: José Cruz
        Version: 1.0.1
    """

    def __init__(self):
        self.event = Event()
        pass 

    def start(self, update: Update, context: CallbackContext):
        """
            Send a message when the command /start is issued.

            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """

        user = update.effective_user
        message = fr'Hola {user.mention_markdown_v2()}\!\
Estoy para ayudarte\.'
        update.message.reply_markdown_v2(
            message,
            reply_markup=ForceReply(selective=True),
        )

    def help_command(self, update: Update, context: CallbackContext):
        """
            Send a message when the command /help is issued.
            
            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """

        update.message.reply_text('Help!')

    def inspireme(self, update: Update, context: CallbackContext):
        """
            Send an insirational message to the user

            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """
        json = Json()
        update.message.reply_text(json.randomInspire())

    def echo(self, update: Update, context: CallbackContext):
        """
            Echo the user message.
            
            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """

        update.message.reply_text(update.message.text)
    
    def createMeet(self, update: Update, context: CallbackContext):
        """
            Method that init the meet creation

            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """

        update.message.reply_text(
            "Para programar tu reunión necesitamos algunos datos básicos\n"
            "*Puedes cancelar esta acción en cualquier momento con el comando /cancelar*\n\n"
            "Indicame como se llamará el evento:",
            parse_mode='MarkdownV2'
        )

        return SUMMARY
    
    def setEventName(self, update: Update, context: CallbackContext):
        """
            Method that add the name to the meet event

            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """

        self.event.summary = update.message.text

        update.message.reply_text(
            "Ahora indicame la fecha del evento:\n"
            "*Ej: 2021\\-07\\-10*",
            parse_mode='MarkdownV2'
        )

        return DATE
    
    def setEventDate(self, update: Update, context: CallbackContext):
        """
            Method that stablish the date for the event

            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """

        self.event.date = update.message.text

        update.message.reply_text(
            "Indicame la hora de inicio y de fin del evento:\n"
            "*Ej: 12:00 pm \\- 2:00 pm*",
            parse_mode='MarkdownV2'
        )

        return TIMES
    
    def setEventTimes(self, update: Update, context: CallbackContext):
        """
            Method that stablish the datetimes for the init and end infor for the event

            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """

        times = self.extractTime(update.message.text)

        self.event.schedule["start"] = times[0]
        self.event.schedule["end"] = times[1]

        update.message.reply_text(
            "Para finalizar, indicame los correos de los usuarios que participaran del evento separados por comas y sin espacios:\n"
            "*Puedes escribir /default para añadir los integrantes por defecto*",
            parse_mode='MarkdownV2'
        )

        return GUESTS

    def extractTime(self, message):
        """
            Method that get the datetime string for end and init from a message

            Parameters
            -----------
            message: str
                the text message with the times
            
            Returns
            --------
            result: List
                The list with the start and end datetimes
        """

        times = message.split("-")
        timeInit = times[0].split(" ")
        timeEnd = times[1].split(" ")
        dateEnd = self.event.date

        if timeInit[1].lower() == 'am':
            timeInit = timeInit[0].split(":")
            timeInit[0] = timeInit[0] if len(timeInit[0]) > 1 else f"0{timeInit[0]}"
            timeInit = f"00:{timeInit[1]}:00" if timeInit[0] == '12' else f"{timeInit[0]}:{timeInit[1]}:00"
        else:
            timeInit = timeInit[0].split(":")
            timeInit = f"{timeInit[0]}:{timeInit[1]}:00" if timeInit[0] == '12' else f"{int(timeInit[0]) + 12}:{timeInit[1]}:00"

        if (timeEnd[1].lower() if timeEnd[0] != "" else timeEnd[2].lower()) == 'am':
            timeEnd = timeEnd[0].split(":") if timeEnd[0] != "" else timeEnd[1].split(":")
            tempTime = timeEnd[0]
            timeEnd[0] = timeEnd[0] if len(timeEnd[0]) > 1 else f"0{timeEnd[0]}"
            timeEnd = f"00:{timeEnd[1]}:00" if timeEnd[0] == '12' else f"{timeEnd[0]}:{timeEnd[1]}:00"

            if tempTime == '12':
                dateEnd = str(datetime.strptime(dateEnd, "%Y-%m-%d") + timedelta(days=1)).split(" ")
                dateEnd = dateEnd[0]
        else:
            timeEnd = timeEnd[0].split(":") if timeEnd[0] != "" else timeEnd[1].split(":")
            timeEnd = f"{timeEnd[0]}:{timeEnd[1]}:00" if timeEnd[0] == '12' else f"{int(timeEnd[0]) + 12}:{timeEnd[1]}:00"

        dateInit = f"{self.event.date}T{timeInit}"
        dateEnd = f"{dateEnd}T{timeEnd}"

        return [dateInit, dateEnd]

    def setGuests(self, update: Update, context: CallbackContext):
        """
            Function that get the emails of the guests for the message

            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """

        guests = update.message.text.split(",")

        for i in range(1, len(guests)):
            self.event.guests.append({"email": guests[i]})
        
        self.programMeet(update, context)

        return  ConversationHandler.END
        
    def defaultGuests(self, update: Update, context: CallbackContext):
        """
            Function that set the guests with the default guests emails saved

            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """

        guests = str(dotenv_values(".env").get("DEFAULT_EMAILS")).split(",")

        for i in range(1, len(guests)):
            self.event.guests.append({"email": guests[i]})
        
        self.programMeet(update, context)
        self.event = Event()

        return  ConversationHandler.END

    def programMeet(self, update: Update, context: CallbackContext):
        """
            Method that create a new meet in the google calendar

            Parameters
            -----------
            update : Update
                Information from the user and chat
            context: CallbackContext
        """      

        event = self.event.createEvent()

        update.message.reply_text(f"Se ha programado tu reunión, podrás acceder a través del siguiente enlace:\n{event.get('hangoutLink')}")

        return
    
    def cancel(self, update: Update, context: CallbackContext):
        update.message.reply_text("Está bien, estoy aquí por si me necesitas nuevamente.")
        self.event = Event()

        return ConversationHandler.END
