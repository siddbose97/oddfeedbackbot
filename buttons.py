from telegram import KeyboardButton

weapons = {
    "SAR21":KeyboardButton(text='SAR21'),
    "SAW MK2":KeyboardButton(text='SAW MK2'),
    "SAW MK3":KeyboardButton(text='SAW MK3'),
    "SAW MK3A":KeyboardButton(text='SAW MK3A'),
    "GPMG INF":KeyboardButton(text='GPMG INF'),
    "Other":KeyboardButton(text='Other')

}

unitbuttons = {
    'Armour':KeyboardButton(text='Armour'),
    'Artillery':KeyboardButton(text='Artillery'),
    'Engineers':KeyboardButton(text='Engineers'),
    'Commandos':KeyboardButton(text='Commandos'),
    'Guards':KeyboardButton(text='Guards'),
    'Infantry':KeyboardButton(text='Infantry'),
    'Signals':KeyboardButton(text='Signals')
}

battalionButtons = {
    'Armour': [[KeyboardButton(text='40SAR'),KeyboardButton(text='41SAR')],
                [KeyboardButton(text='42SAR'),KeyboardButton(text='48SAR')]]
}

companyButtons = {
    'Armour':{
        '40SAR':[[KeyboardButton(text='HQ'),KeyboardButton(text='Support')],
                [KeyboardButton(text='Alpha')],
                [KeyboardButton(text='Bravo'),KeyboardButton(text='Charlie')]],
        '41SAR':[[KeyboardButton(text='HQ'),KeyboardButton(text='Support')],
                [KeyboardButton(text='Alpha')],
                [KeyboardButton(text='Bravo'),KeyboardButton(text='Charlie')]],
        '42SAR':[[KeyboardButton(text='HQ'),KeyboardButton(text='Support')],
                [KeyboardButton(text='Alpha')],
                [KeyboardButton(text='Bravo'),KeyboardButton(text='Charlie')]],
        '48SAR':[[KeyboardButton(text='HQ'),KeyboardButton(text='Support')],
                [KeyboardButton(text='Alpha')],
                [KeyboardButton(text='Bravo'),KeyboardButton(text='Charlie')]]
    }
}
