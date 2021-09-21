import telegram 

unitbuttons = {
    'Armour':telegram.KeyboardButton(text='Armour'),
    'Artillery':telegram.KeyboardButton(text='Artillery'),
    'Engineers':telegram.KeyboardButton(text='Engineers'),
    'Commandos':telegram.KeyboardButton(text='Commandos'),
    'Guards':telegram.KeyboardButton(text='Guards'),
    'Infantry':telegram.KeyboardButton(text='Infantry'),
    'Signals':telegram.KeyboardButton(text='Signals')
}

battalionButtons = {
    'Armour': [[telegram.KeyboardButton(text='40SAR'),telegram.KeyboardButton(text='41SAR')],
                [telegram.KeyboardButton(text='42SAR'),telegram.KeyboardButton(text='48SAR')]]
}

companyButtons = {
    'Armour':{
        '40SAR':[[telegram.KeyboardButton(text='HQ'),telegram.KeyboardButton(text='Support')],
                [telegram.KeyboardButton(text='Alpha')],
                [telegram.KeyboardButton(text='Bravo'),telegram.KeyboardButton(text='Charlie')]],
        '41SAR':[[telegram.KeyboardButton(text='HQ'),telegram.KeyboardButton(text='Support')],
                [telegram.KeyboardButton(text='Alpha')],
                [telegram.KeyboardButton(text='Bravo'),telegram.KeyboardButton(text='Charlie')]],
        '42SAR':[[telegram.KeyboardButton(text='HQ'),telegram.KeyboardButton(text='Support')],
                [telegram.KeyboardButton(text='Alpha')],
                [telegram.KeyboardButton(text='Bravo'),telegram.KeyboardButton(text='Charlie')]],
        '48SAR':[[telegram.KeyboardButton(text='HQ'),telegram.KeyboardButton(text='Support')],
                [telegram.KeyboardButton(text='Alpha')],
                [telegram.KeyboardButton(text='Bravo'),telegram.KeyboardButton(text='Charlie')]]
    }
}