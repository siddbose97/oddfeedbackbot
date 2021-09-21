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
    'Armour': [[telegram.KeyboardButton(text='40SAR'),telegram.KeyboardButton(text='41SAR')]
                [telegram.KeyboardButton(text='42SAR'),telegram.KeyboardButton(text='48SAR')]]
}