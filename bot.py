import telegram
import telegram.ext
import re
from random import randint
import os

# The API Key we received for our bot
API_KEY = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', 8443))

# Create an updater object with our API Key
updater = telegram.ext.Updater(API_KEY)
# Retrieve the dispatcher, which will be used to add handlers
dispatcher = updater.dispatcher
# Our states, as integers

DIVSTEP, COYSTEP, WPNSTEP, DEFECTSTEP, DEFECTIDSTEP, RMKCHKSTEP, RMKSTEP, CANCEL = range(8)

buttons = {
    "units":['Armour', 'Artillery','Combat Engineers', "Commandos", "Guards","Infantry","Signals"]
}

# The entry function
def start(update_obj, context):
    # send the question, and show the keyboard markup (suggested answers)
    update_obj.message.reply_text("Hello there, which unit are you from?",
        reply_markup=telegram.ReplyKeyboardMarkup([buttons['units']], one_time_keyboard=True)
    )
    # go to the Division state
    return DIVSTEP
def divstep(update_obj, context):
    update_obj.message.reply_text("divstep")

    return COYSTEP


def coyStep(update_obj, context):
    update_obj.message.reply_text("coystep")

    return CANCEL









# in the CORRECT state
def correct(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        update_obj.message.reply_text("Glad it was useful! ^^")
    else:
        update_obj.message.reply_text("You must be a programming wizard already!")
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(f"See you {first_name}!, bye")
    return telegram.ext.ConversationHandler.END

def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}!", reply_markup=telegram.ReplyKeyboardRemove()
    )
    return telegram.ext.ConversationHandler.END



def main():
    # a regular expression that matches yes or no
    yes_no_regex = re.compile(r'^(yes|no|y|n)$', re.IGNORECASE)
    # Create our ConversationHandler, with only one state
    handler = telegram.ext.ConversationHandler(
        entry_points=[telegram.ext.CommandHandler('start', start)],
        states={
                DIVSTEP: [telegram.ext.MessageHandler(telegram.ext.Filters.text, divstep)],
                CANCEL: [telegram.ext.MessageHandler(telegram.ext.Filters.text, cancel)],
                COYSTEP: [telegram.ext.MessageHandler(telegram.ext.Filters.text, coyStep)],
        },
        fallbacks=[telegram.ext.CommandHandler('cancel', cancel)],
        )
    # add the handler to the dispatcher
    dispatcher.add_handler(handler)
    # start polling for updates from Telegram
    updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=API_KEY,
                            webhook_url="https://still-sierra-92948.herokuapp.com/" + API_KEY)
    updater.idle()


if __name__ == '__main__':
    main()