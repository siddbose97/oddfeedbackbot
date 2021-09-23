import telegram
import telebot
import telegram.ext
import re
from random import randint
import os
from buttons import unitbuttons, battalionButtons,companyButtons
from datastruct import mainDB
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import gspread_dataframe
import pytz
import datetime as dt


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# The API Key we received for our bot
API_KEY = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', 8443))

# Create an updater object with our API Key
updater = telegram.ext.Updater(API_KEY)
# Retrieve the dispatcher, which will be used to add handlers
dispatcher = updater.dispatcher
# Our states, as integers

BATSTEP, COYSTEP, WPNSTEP,BUTTSTEP, DEFECTSTEP, DEFECTIDSTEP, RMKCHKSTEP, RMKSTEP, CANCEL = range(9)

#=================================================================================================================
#Google sheet API access set up
#=================================================================================================================
#set up google sheets API
# Set scope to use when authenticating:
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']

# Authenticate using your credentials, saved in JSON in Step 1:
jsonfile = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
creds = ServiceAccountCredentials.from_json_keyfile_name(jsonfile, scope)

# authorize the clientsheet 
client = gspread.authorize(creds)
sheet = client.open('ODD Feedback').sheet1
data = gspread_dataframe.get_as_dataframe(sheet)
#=================================================================================================================

oddDict = {}

class ODD:
    def __init__(self, chatID):
        self.chatID = chatID
        self.unit = ""
        self.battalion = ""        
        self.datetime = ""
        self.coy = ""
        self.wpn = ""
        self.butt = 0
        # self.defPart = ""
        # self.defect = ""
        # self.rmk = ""
        self.batstep = ""
        self.coystep = ""
        self.wpnstep = ""
        self.buttstep = ""
        self.defidstep = ""
        self.defstep = ""
        self.rmkchkstep = ""
        self.rmkstep = ""


# The entry function
def start(update_obj, context):
    # send the question, and show the keyboard markup (suggested answers)
    # list1 = [unitbuttons['Armour'], unitbuttons['Artillery']]
    # list2 = [unitbuttons['Engineers'], unitbuttons['Commandos'], unitbuttons['Guards']]
    # list3 = [unitbuttons['Infantry'], unitbuttons['Signals']]
    try:
        list1 = [[telegram.KeyboardButton(text=unit)] for unit in list(mainDB.keys())]
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)
        chat_id = update_obj.message.chat_id
        oddDict[chat_id] = ODD(chat_id)

        update_obj.message.reply_text("Hello there, which unit are you from?",reply_markup=kb)
    # go to the Batallion state
        return BATSTEP
    except Exception as e:
        cancel(e, context)


def batStep(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        odd = oddDict[chat_id]
        sg=pytz.timezone('Asia/Singapore')
        now = sg.localize(dt.datetime.now())
        
        odd.datetime = now
        odd.unit = msg

        if not msg in mainDB.keys():
            raise Exception
        list1 = [[telegram.KeyboardButton(text=battalion)] for battalion in list(mainDB[odd.unit].keys())]
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

        update_obj.message.reply_text(f"Which battalion in {msg} are you from?",reply_markup=kb)
        return COYSTEP
    except Exception as e:
        cancel(e, context)

    


def coyStep(update_obj, context):
    chat_id = update_obj.message.chat_id
    msg = update_obj.message.text
    odd = oddDict[chat_id]

    odd.battalion = msg
    
    list1 = [[telegram.KeyboardButton(text=battalion)] for battalion in list(mainDB[odd.unit][odd.battalion].keys())]
    kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

    update_obj.message.reply_text(f"Which Company in {msg} are you from?",reply_markup=kb)
    #return CANCEL
    return WPNSTEP

def wpnStep(update_obj, context):
    chat_id = update_obj.message.chat_id
    msg = update_obj.message.text
    odd = oddDict[chat_id]
    odd.coy = msg

    list1 = [[telegram.KeyboardButton(text=weapon)] for weapon in mainDB[odd.unit][odd.battalion][odd.coy]]
    kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

    
    update_obj.message.reply_text("Which Weapon has a defect?",reply_markup=kb)

    return BUTTSTEP

def buttStep(update_obj, context):
    chat_id = update_obj.message.chat_id
    msg = update_obj.message.text
    odd = oddDict[chat_id]
    odd.wpn = msg

    # list1 = [
    # ['7', '8', '9'],
    # ['4', '5', '6'],
    # ['1', '2', '3'],
    #      ['0']]
    # kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

    
    update_obj.message.reply_text("What is the weapon's butt number?")
    
    return CANCEL 

def defectStep(update_obj, context):
    chat_id = update_obj.message.chat_id
    oddDict[chat_id].defstep = update_obj.message.text
    update_obj.message.reply_text("defectStep") 

    return DEFECTIDSTEP

def defectIDStep(update_obj, context):
    chat_id = update_obj.message.chat_id
    oddDict[chat_id].defidstep = update_obj.message.text
    update_obj.message.reply_text("defectIDStep")

    return RMKCHKSTEP

def rmkchkStep(update_obj, context):
    chat_id = update_obj.message.chat_id
    oddDict[chat_id].rmkchkstep = update_obj.message.text
    update_obj.message.reply_text("rmkchkStep")

    return RMKSTEP

def rmkstep(update_obj, context):
    chat_id = update_obj.message.chat_id
    odd = oddDict[chat_id]
    odd.rmkstep = update_obj.message.text
    update_obj.message.reply_text("rmkstep")
    #sheet.append_row([odd.batstep, odd.coystep, odd.wpnstep, odd.buttstep, odd.defidstep, odd.defstep, odd.rmkchkstep, odd.rmkstep])
    return CANCEL 









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
                BATSTEP: [telegram.ext.MessageHandler(telegram.ext.Filters.text(), batStep)],
                COYSTEP: [telegram.ext.MessageHandler(telegram.ext.Filters.text, coyStep)],
                WPNSTEP: [telegram.ext.MessageHandler(telegram.ext.Filters.text, wpnStep)],
                BUTTSTEP: [telegram.ext.MessageHandler(telegram.ext.Filters.text, buttStep)],
                DEFECTSTEP: [telegram.ext.MessageHandler(telegram.ext.Filters.text, defectStep)],
                DEFECTIDSTEP: [telegram.ext.MessageHandler(telegram.ext.Filters.text, defectIDStep)],
                RMKCHKSTEP: [telegram.ext.MessageHandler(telegram.ext.Filters.text, rmkchkStep)],
                RMKSTEP: [telegram.ext.MessageHandler(telegram.ext.Filters.text, rmkstep)],
                CANCEL: [telegram.ext.MessageHandler(telegram.ext.Filters.text, cancel)]
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