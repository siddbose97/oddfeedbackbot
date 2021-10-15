import telegram
import telegram.ext
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
import os
from armskote import mainDB
from weapons import weaponDefects
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
updater = Updater(API_KEY)
# Retrieve the dispatcher, which will be used to add handlers
dispatcher = updater.dispatcher
# Our states, as integers

BATSTEP, COYSTEP, WPNSTEP,BUTTSTEP, DEFECTSTEP, DEFECTIDSTEP, RMKCHKSTEP, YESORNO, RMKSTEP, END, CANCEL = range(11)

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
    def __init__(self, chatID, first_name, last_name):
        self.chatID = chatID
        self.name = f'{first_name} {last_name}'
        self.unit = ""
        self.battalion = ""        
        self.datetime = ""
        self.coy = ""
        self.wpn = ""
        self.butt = 0
        self.defPart = ""
        self.defect = "Check Remark"
        self.rmk = "N/A"
#=================================================================================================================
       
def help(update_obj, context):
    try:
        help_string = """
Welcome to the ODD Feedback Bot! 
Here you can report your ODDs 
without spending time waiting 
for the notebook to be passed around!

/start will start the bot and will
lead you through a series of questions
to easily report the required information

If you are having any issues or
suggestions please contact 62FMD at 6AMB

        
        """

        update_obj.message.reply_text(help_string)
        return ConversationHandler.END

    except Exception as e:
        cancel(e, context)
        return ConversationHandler.END
#=================================================================================================================

# The entry function
def start(update_obj, context):
  
    try:
        list1 = [[telegram.KeyboardButton(text=unit)] for unit in list(mainDB.keys())]
        list1.append([telegram.KeyboardButton(text='QUIT')])
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)
        chat_id = update_obj.message.chat_id
        first_name = update_obj.message.from_user['first_name']
        last_name = update_obj.message.from_user['last_name']
        oddDict[chat_id] = ODD(chat_id, first_name,last_name )

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

        if msg == "QUIT":
            return cancel(update_obj, context)

        if not msg in mainDB.keys():
            raise Exception
        list1 = [[telegram.KeyboardButton(text=battalion)] for battalion in list(mainDB[odd.unit].keys())]
        list1.append([telegram.KeyboardButton(text='QUIT')])

        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

        update_obj.message.reply_text(f"Which battalion in {msg} are you from?",reply_markup=kb)
        return COYSTEP
    except Exception as e:
        cancel(update_obj, context)
        return ConversationHandler.END
    


def coyStep(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        odd = oddDict[chat_id]

        odd.battalion = msg
        if msg == "QUIT":
            return cancel(update_obj, context)
        list1 = [[telegram.KeyboardButton(text=battalion)] for battalion in list(mainDB[odd.unit][odd.battalion].keys())]
        list1.append([telegram.KeyboardButton(text='QUIT')])
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

        update_obj.message.reply_text(f"Which Company in {msg} are you from?",reply_markup=kb)
        #return CANCEL
        return WPNSTEP  
    except Exception as e:
        cancel(update_obj, context)
        return ConversationHandler.END

def wpnStep(update_obj, context):
    try: 
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        odd = oddDict[chat_id]
        odd.coy = msg
        if msg == "QUIT":
            return cancel(update_obj, context)

        list1 = [[telegram.KeyboardButton(text=weapon)] for weapon in mainDB[odd.unit][odd.battalion][odd.coy]]
        list1.append([telegram.KeyboardButton(text='QUIT')])
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

        
        update_obj.message.reply_text("Which Weapon has a defect?",reply_markup=kb)
        return BUTTSTEP

    except Exception as e:
        cancel(update_obj, context)
        return ConversationHandler.END


def buttStep(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        odd = oddDict[chat_id]
        odd.wpn = msg
        if msg == "QUIT":
            return cancel(update_obj, context)    
        list1 = [[telegram.KeyboardButton(text='QUIT')]]
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)
        update_obj.message.reply_text("Enter the Weapon's butt number or click QUIT to end" ,reply_markup=kb)
        
        return DEFECTSTEP 
    except Exception as e:        
        cancel(update_obj, context)
        return ConversationHandler.END

def defectStep(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        odd = oddDict[chat_id]
        odd.butt = msg
        if msg == "QUIT":
            return cancel(update_obj, context)  
        list1 = [[telegram.KeyboardButton(text=weapon_part)] for weapon_part in list(weaponDefects[odd.wpn].keys())]
        list1.append([telegram.KeyboardButton(text='QUIT')])
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

        
        update_obj.message.reply_text("What part has the defect?",reply_markup=kb)

        return DEFECTIDSTEP
    except Exception as e:        
        cancel(update_obj, context)
        return ConversationHandler.END

def defectIDStep(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        odd = oddDict[chat_id]
        odd.defPart = msg
        if msg == "QUIT":
            return cancel(update_obj, context)  
        if odd.defPart == 'OTHER':
            update_obj.message.reply_text("Please explain as best as possible what the issue is")
            return END
        else:
            list1 = [[telegram.KeyboardButton(text=defect)] for defect in list(weaponDefects[odd.wpn][odd.defPart].values())]
            list1.append([telegram.KeyboardButton(text='QUIT')])

            kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

            
            update_obj.message.reply_text("What is the actual defect?",reply_markup=kb)
            return RMKCHKSTEP
    except Exception as e:        
        cancel(update_obj, context)
        return ConversationHandler.END

def rmkchkStep(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        odd = oddDict[chat_id]
        odd.defect = msg
        if msg == "QUIT":
            return cancel(update_obj, context)  
        list1 = [[telegram.KeyboardButton(text='Yes'), telegram.KeyboardButton(text='No')],[telegram.KeyboardButton(text='QUIT')]]
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

        
        update_obj.message.reply_text("Do you have further remarks?",reply_markup=kb)
        return YESORNO

    except Exception as e:        
        cancel(update_obj, context)
        return ConversationHandler.END


def check_yes_or_no(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        odd = oddDict[chat_id]
        if msg == "QUIT":
            return cancel(update_obj, context)  
        if msg == 'Yes':
            list1 = [[telegram.KeyboardButton(text='QUIT')]]

            kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)
            update_obj.message.reply_text("Enter remarks below or click QUIT to end",  reply_markup=kb)
            return END
        elif msg == 'No':
            update_obj.message.reply_text(
            f"Thank you {odd.name.split()[0]} for your report! Please click /start to restart the bot", reply_markup=telegram.ReplyKeyboardRemove()
            )
            sheet.append_row([str(odd.datetime),odd.name, f"{odd.battalion} {odd.coy}", odd.wpn, odd.butt,odd.defPart, odd.defect, odd.rmk])
            return ConversationHandler.END
    except Exception as e:        
        cancel(update_obj, context)
        return ConversationHandler.END




def end(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        odd = oddDict[chat_id]
        odd.rmk = msg
        if msg == "QUIT":
            return cancel(update_obj, context)  
        sheet.append_row([str(odd.datetime),odd.name, f"{odd.battalion} {odd.coy}", odd.wpn, odd.butt,odd.defPart, odd.defect, odd.rmk])
        update_obj.message.reply_text(
            f"Thank you {odd.name.split()[0]} for your report! Click /start to start again", reply_markup=telegram.ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    except Exception as e:        
        cancel(update_obj, context)
        return ConversationHandler.END 
    




def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}! Please click /start to start again",\
             reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END

def outside_of_handler(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Hi {first_name}! Please click /start to start the bot or click /help to learn more",\
             reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END


def main():


    handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),CommandHandler('help', help)],
        states={
                BATSTEP: [MessageHandler(Filters.text, batStep)],
                COYSTEP: [MessageHandler(Filters.text, coyStep)],
                WPNSTEP: [MessageHandler(Filters.text, wpnStep)],
                BUTTSTEP: [MessageHandler(Filters.text, buttStep)],
                DEFECTSTEP: [MessageHandler(Filters.text, defectStep)],
                DEFECTIDSTEP: [MessageHandler(Filters.text, defectIDStep)],
                RMKCHKSTEP: [MessageHandler(Filters.text, rmkchkStep)],
                YESORNO: [MessageHandler(Filters.text, check_yes_or_no)],
                END: [MessageHandler(Filters.text, end)],
                CANCEL: [MessageHandler(Filters.text, cancel)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        )
    # add the handler to the dispatcher
    dispatcher.add_handler(handler)
    dispatcher.add_handler(MessageHandler(Filters.text | ~Filters.text, outside_of_handler))

    # start polling for updates from Telegram
    updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=API_KEY,
                            webhook_url="https://still-sierra-92948.herokuapp.com/" + API_KEY)
    updater.idle()


if __name__ == '__main__':
    main()