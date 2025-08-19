from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


# Кнопки для выбора профессии
def get_professions_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Courier', callback_data='prof1_start'),
            InlineKeyboardButton('Shipping', callback_data='prof2_start')
        ],
        [
            InlineKeyboardButton('supplier', callback_data='prof3_start'),
            InlineKeyboardButton('Farmer', callback_data='prof4_start')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)