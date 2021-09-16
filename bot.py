from dotenv import load_dotenv
load_dotenv()

from time import sleep
import os
import telebot
from telegram import KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
PORT = int(os.environ.get('PORT', 8443))

oddDict = {}

class ODD:
    def __init__(self, coy):
        self.coy = coy
        self.wpnType = "SAR21" #use button options
        self.date = ""
        self.buttNum = ""
        self.oddCode = ""
        self.rmk = ""
        self.summary = ""

DIVSTEP, COYSTEP, WPNSTEP, DEFECTSTEP, DEFECTIDSTEP, RMKCHKSTEP, RMKSTEP = range(7)

#=============================================================
def start(update, context:CallbackContext):
    msg = bot.reply_to(update.effective_message, """\
Hi there, I am the ODD Feedback Bot. What unit are you from?
""")

    return DIVSTEP
    
def divStep(update, context:CallbackContext):
    bot.send_message(update.effective_message.chat.id,"Divstep")

    return COYSTEP

def coyStep(update, context:CallbackContext):
    bot.send_message(update.effective_message.chat.id,"Coystep")

    return WPNSTEP

def wpnStep(update, context:CallbackContext):
    bot.send_message(update.effective_message.chat.id,"WpnStep")

    return DEFECTSTEP

def defectStep(update, context:CallbackContext):
    bot.send_message(update.effective_message.chat.id,"DefectStep")

    return DEFECTIDSTEP

def defectIDStep(update, context:CallbackContext):
    bot.send_message(update.effective_message.chat.id,"DefectIDStep")

    return RMKCHKSTEP

def rmkchkStep(update, context:CallbackContext):
    bot.send_message(update.effective_message.chat.id,"RmkCheckStep")

    return RMKSTEP

def rmkStep(update, context:CallbackContext):
    bot.send_message(update.effective_message.chat.id,"RMKStep")

    return ConversationHandler.END

def qFunc(update, context:CallbackContext):
    try:
        bot.send_message(update.effective_message.chat.id,"Unrecognized Input! Please press /start to try again!")
    except Exception:
        errorString = "Sorry something went wrong! Please press /start to try again!"
        bot.send_message(update.effective_message.chat.id,errorString)
#=============================================================

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))    

    start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states = {
            DIVSTEP:  [MessageHandler(Filters.text, divStep)],
            COYSTEP: [MessageHandler(Filters.text, coyStep)],
            WPNSTEP: [MessageHandler(Filters.text, wpnStep)],
            DEFECTSTEP: [MessageHandler(Filters.text, defectStep)],
            DEFECTIDSTEP: [MessageHandler(Filters.text, defectIDStep)],
            RMKCHKSTEP: [MessageHandler(Filters.text, rmkchkStep)],
            RMKSTEP: [MessageHandler(Filters.text, rmkStep)],
                },
        fallbacks=[CommandHandler('quit', qFunc), MessageHandler(Filters.text, qFunc)]
        )


    dp.add_handler(start_conv_handler)
    dp.add_handler(CommandHandler('quit', qFunc))

    # add handlers
    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN,
                        webhook_url="https://still-sierra-92948.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()