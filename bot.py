from dotenv import load_dotenv
load_dotenv()

from time import sleep
import os
import telebot
import geopy.distance
from telegram import Location, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime


TOKEN = "1835053064:AAF4txvpIA4em49xZwBYQACArT4OmQC7ZhQ"
bot = telebot.TeleBot(TOKEN)
PORT = int(os.environ.get('PORT', 8443))

oddDict = {}


class Odd:
    def __init__(self, unitNum):
        self.unit = unitNum
        self.wpnType = "SAR21" #use button options
        self.date = ""
        self.buttNum = ""
        self.oddCode = ""
        self.rmk = ""
        self.summary = ""


#turn this dictionary into numbers or make a secondary dictionary to transform into numbers (SAR21:1, SAW:2, etc)
oddTypes = {
    "SAR21": {
        "BARREL":{
            1:"1. Bent or curved",
            2:"2. Handguard Loose, Cracked or Deficient",
            3:"3. Others"
        },
        "SCOPE":
        {
            1:"1. Lens Cracked or Scratched",
            2:"2. Condensation in Lens",
            3:"3. Scope Loose",
            4:"4. Reticle/Crosshairs tilted",
            5:"5. Cannot aim target at 300m",
            6:"6. Others"
        },
        "CHARGING HANDLE":
        {
            1:"1. Rubber handle tear > 30mm",
            2:"2. Step Pin/Circlip deficient",
            3:"3. Front sight post broken/deficient",
            4:"4. Charging handle broken or deficient",
            5:"5. Charging handle over rotated",
            6:"6. Charging handle fail to function",
            7:"7. Others"
        },
        "LAD":
        {
            1:"1. Baffle worn out or cracked",
            2:"2. Selector switch worn out",
            3:"3. Lanyard broken",
            4:"4. Battery cap assembly deficient",
            5:"5. Momentary switch torn or faulty",
            6:"6. LAD loose",
            7:"7. LAD (4 modes) fail function check",
            8:"8. LAD does not work with AA Battery",
            9:"9. Others"
        },
        "MUZZLE AND WASHER":{
            1:"1. Muzzle cracked or worn out",
            2:"2. Washer deficient",
            3:"3. Others"
        },
        "BOLT CARRIER ASSEMBLY":{
            1:"1. Bolt cam pin deficient",
            2:"2. Extractor spring broken or deficient",
            3:"3. Extractor pin broken or deficient",
            4:"4. Others"
        },
        "RECEIVERS":
        {
            1:"1. Trigger bar assembly fail to function",
            2:"2. Safety button fail to function",
            3:"3. Safety button too tight/loose",
            4:"4. Deflector loose/deficient",
            5:"5. Front takedown pin too tight/deficient",
            6:"6. Back takedown pin too tight/deficient",
            7:"7. Hammer Spring Broken/deficient",
            8:"8. Hammer Plunger broken/deficient",
            9:"9. Auto-selector too tight or fail to function",
            10:"10. Others"
        },
        "FC":
        {
            1:"1. Gas regulator fail to function",
            2:"2. Can fire when set to safe",
            3:"3. Last round catch fail to trap bolt carrier assembly",
            4:"4. Magazine catch fail to hold magazine",
            5:"5. Bolt carrier cannot slide freely in Charging Tube Assembly",
            6:"6. Others"
        },
        "OTHER": {
            1:"Input ODD Location"
        }

    }
}

SAR21Map = {1: "BARREL", 2: "SCOPE", 3: "CHARGING HANDLE", 4:"LAD", 5:"MUZZLE AND WASHER", \
    6:"BOLT CARRIER ASSEMBLY", 7:"RECEIVERS", 8:"FC",9:"OTHER"}

#=============================================================
# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.reply_to(message, """\
Hi there, I am the ODD Feedback Bot. What unit are you from?
""")
    bot.register_next_step_handler(msg, unitStep)

def unitStep(message):
    try:
        chat_id = message.chat.id
        unit = message.text
        odd = Odd(unit)
        oddDict[chat_id] = odd


        #getting date
        now = datetime.now()

        # dd/mm/YY H:M:S
        odd.date = now.strftime("%d/%m/%Y %H:%M:%S")

        msg = bot.reply_to(message, 'What is the butt number?')
        bot.register_next_step_handler(msg, buttStep)
    except Exception as e:
        bot.reply_to(message, 'oooops')

#enter weapon type here
#add condition where if the input is "quit" then quit


def buttStep(message):
    try:
        chat_id = message.chat.id
        buttNum = message.text
        odd = oddDict[chat_id]
        odd.buttNum = buttNum
        url = "https://lh3.googleusercontent.com/V0ItwRUHvmcQ22XlCzeIeviA6kuMfUspJHgHbwkA8nD09SjesgQYt3RdFB1nvM63kYSs8TgTwk-1KTiJBt8gbRJZlZQVWzKEWDh3a1w51A2m2j-Qt31PrJbR3viWlMFMyar4TOTZS8eXGiX0itB4B-dTDCoJZnZONHwzhHGo_YetJlSpfE1ohVWpeQrj34TmOSGJSz48O-tkzMLKbuYsXIjKuolALQsM961r2N08HcBz0GQ03gxJkrV5Q5IOOwhvoAeK_z-lwf1gQb1GBpQ9gf0vQqG9KPYBuzljdBVlwqYzytihp-1gK7nlEYmeERYYK6ubpFX3NA4jkRujjaqY0df9AC7xsx5q0sbp-hboAlA1jM3bQLxvRicU5usSimVY6RCBFgrJ3LbLKNLNlxgYoLIe88eDpLVRVemMGqNURQBSzi-uKi8pe_BZuxOw3pMSQoOR0JELkjbIBRS9e3mP53Sb4eCflk1hQrwroiEBJDdN5tmfctqbY3ha9N0sJ9ng3wXSgBIWZl_tzYGVJlB4fng-vfyZhSxdsVWd1Z6Yc3pgZZJF8mz_6YG5z4jQ5SumFUEVtLeTPFXqNsR3-BhdQJK4QiZcnd8qWrIG8WoZBRIM_vp_NNvv7kInjb_SYZCz_7zvwjBYAZe_61K7XamQxrxWxIa_hOvzLmZGJk7eOPOIFT7yWJTtpvCudcGGQq8aqNW_WXluoVR6UhywwVu7N45COg=w763-h304-no?authuser=1"
        
        bot.send_photo(chat_id=chat_id, photo=url)
        msg = bot.reply_to(message, """\
Where is the ODD (input only the number)? \n
1. Barrel and Handguard
2. Scope
3. Charging Handle
4. LAD
5. Muzzle and Washer
6. Bolt Carrier Assembly
7. Upper/Lower Receiver
8. Functioning Check
9. Other
""")
        bot.register_next_step_handler(msg, locationStep)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def locationStep(message):
    try:
        chat_id = message.chat.id
        rmk = message.text
        odd = oddDict[chat_id]
        # odd.rmk = rmk
        info = oddTypes["SAR21"][SAR21Map[int(rmk)]]
        
        #if "other" then next step is inputting the correct location (idk is an option)
        #if not other, then say what the issue is, or choose other and type it in

        if int(rmk) != 9:
            sendString = "Select ODD from List (Number only)" + "\n\n"
            sendString += SAR21Map[int(rmk)] + ":\n"
            for elements in info.values():
                sendString += elements + "\n" 
            #bot.send_message(chat_id, )

            odd.oddCode = "1." + str(rmk)
            msg = bot.reply_to(message, sendString)
            bot.register_next_step_handler(msg, oddTypeStep)
        else:
            odd.oddCode = "OTHER"
            msg = bot.reply_to(message, 'What is the ODD?')
            bot.register_next_step_handler(msg, otherRMKStep)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def oddTypeStep(message):
    try:
        chat_id = message.chat.id
        oddType = message.text
        odd = oddDict[chat_id]
        odd.oddCode = odd.oddCode + "." + oddType        

        msg = bot.reply_to(message, 'Any further remarks?(if none, type n/a)')
        bot.register_next_step_handler(msg, extraRMKStep)
        
    except Exception as e:
        bot.reply_to(message, 'oooops')




def extraRMKStep(message):
    try:
        chat_id = message.chat.id
        rmk = message.text
        odd = oddDict[chat_id]
        odd.rmk = rmk
        

        unit = "Unit: " + odd.unit.upper() + "\n"
        date = "Date: " + odd.date + "\n"
        wpnType = "Weapon Type: " + odd.wpnType + "\n"
        buttNum = "Butt Number: " + odd.buttNum + "\n"
        oddCode = "ODD Code (if applicable): " + odd.oddCode + "\n"
        rmks = "Remarks: " + odd.rmk + "\n"

        splitting = odd.oddCode.split(".")
        print(splitting)
        #odd.summary = splitting
        #odd.summary = oddTypes[int(splitting[0])-1] + ", " + oddTypes[int(splitting[1])-1] + ", " + oddTypes[int(splitting[2])-1]
        keys = list(oddTypes.keys())
        wpn = keys[int(splitting[0])-1]
        subKeys = list(oddTypes[wpn].keys())
        location = subKeys[int(splitting[1])-1]

        subSubKeys = list(oddTypes[wpn][location].values())
        issue = subSubKeys[int(splitting[2])-1]
        issue = issue[3:]

        odd.summary = wpn + ", " + location.upper().capitalize() + ", " + issue + "\n"
        summary = "Summary: " + str(odd.summary)


        returnStatement = unit + date + wpnType + buttNum + oddCode + rmks + summary
        bot.send_message(chat_id, returnStatement)
        bot.send_message(chat_id, "Please send the above template to your armskote IC")


    except Exception as e:
        bot.reply_to(message, 'oooops')

def otherRMKStep(message):
    try:
        chat_id = message.chat.id
        rmk = message.text
        odd = oddDict[chat_id]
        odd.rmk = rmk

        unit = "Unit: " + odd.unit.upper() + "\n"
        date = "Date: " + odd.date + "\n"
        wpnType = "Weapon Type: " + odd.wpnType + "\n"
        buttNum = "Butt Number: " + odd.buttNum + "\n"
        oddCode = "ODD Code (if applicable): " + "OTHER" + "\n"
        rmks = "Remarks: " + odd.rmk

        returnStatement = unit + date + wpnType + buttNum + oddCode + rmks
        bot.send_message(chat_id, returnStatement)
        bot.send_message(chat_id, "Please send the above template to your armskote IC")

        
    except Exception as e:
        bot.reply_to(message, 'oooops')


def qFunc(update, context):
    try:
        bot.send_message(update.effective_message.chat.id,"Unrecognized Input! Please press /start to try again!")
    except Exception:
        errorString = "Sorry something went wrong! Please press /start to try again!"
        bot.send_message(update.effective_message.chat.id,errorString)
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
    dp.add_handler(CommandHandler("help", help))
    
    startList = ["/start", "RESTART"]
    #message handling
    dp.add_handler(MessageHandler(Filters.text(startList), start)) 
    dp.add_handler(MessageHandler(Filters.text, qFunc)) 

    # add handlers
    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN,
                        webhook_url="https://polar-chamber-36116.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()