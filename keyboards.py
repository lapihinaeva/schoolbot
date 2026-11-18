from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup,InlineKeyboardButton)
menu_rell = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='на сегодня'),KeyboardButton(text='на завтра')],
        [KeyboardButton(text='на неделю')]
    ],
    resize_keyboard=True,
    input_field_placeholder= "выберите расписание"
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='5А'),
         KeyboardButton(text='5Б'),
         KeyboardButton(text='5В')],
        [KeyboardButton(text='6А'),
         KeyboardButton(text='6Б'),
         KeyboardButton(text='6В')],
        [KeyboardButton(text='7А'),
         KeyboardButton(text='7Б'),
         KeyboardButton(text='7В')],
        [KeyboardButton(text='8А'),
         KeyboardButton(text='8Б'),
         KeyboardButton(text='8В')],
        [KeyboardButton(text='9А'),
         KeyboardButton(text='9Б'),
         KeyboardButton(text='9В')],
        [KeyboardButton(text='10А'),
         KeyboardButton(text='10Б')],
        [KeyboardButton(text='11А'),
         KeyboardButton(text='11Б')]
    ],
    resize_keyboard=True,
    input_field_placeholder='выберите свой класс'
)

Cm1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='1 смена', callback_data='1_cm_back')],
        [InlineKeyboardButton(text='2 смена', callback_data='2_cm_back')]
    ]    
)



FiveA = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник5a')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник5a')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда5a')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг5a')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница5a')]
    ]    
)

FiveB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник5b')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник5b')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда5b')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг5b')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница5b')]
    ]    
)

FiveV = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник5v')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник5v')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда5v')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг5v')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница5v')]
    ]    
)



SixA = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник6a')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник6a')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда6a')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг6a')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница6a')]
    ]    
)

SixB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник6b')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник6b')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда6b')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг6b')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница6b')]
    ]    
)

SixV = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник6v')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник6v')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда6v')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг6v')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница6v')]
    ]    
)



SevenA = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник7a')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник7a')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда7a')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг7a')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница7a')]
    ]    
)

SevenB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник7b')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник7b')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда7b')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг7b')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница7b')]
    ]    
)

SevenV = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник7v')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник7v')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда7v')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг7v')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница7v')]
    ]    
)




EightA = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник8a')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник8a')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда8a')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг8a')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница8a')]
    ]    
)

EightB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник8b')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник8b')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда8b')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг8b')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница8b')]
    ]    
)

EightV = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник8v')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник8v')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда8v')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг8v')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница8v')]
    ]    
)



NineA = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник9a')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник9a')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда9a')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг9a')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница9a')]
    ]    
)

NineB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник9b')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник9b')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда9b')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг9b')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница9b')]
    ]    
)

NineV = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник9v')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник9v')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда9v')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг9v')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница9v')]
    ]    
)



TenA = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник10a')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник10a')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда10a')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг10a')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница10a')]
    ]    
)

TenB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник10b')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник10b')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда10b')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг10b')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница10b')]
    ]    
)


ElevenA = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник11a')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник11a')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда11a')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг11a')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница11a')]
    ]    
)

ElevenB = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='Понедельник11b')],
        [InlineKeyboardButton(text='Вторник', callback_data='Вторник11b')],
        [InlineKeyboardButton(text='Среда', callback_data='Среда11b')],
        [InlineKeyboardButton(text='Четверг', callback_data='Четверг11b')],
        [InlineKeyboardButton(text='Пятница', callback_data='Пятница11b')]
    ]    
)
