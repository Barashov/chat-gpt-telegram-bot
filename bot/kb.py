from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def rate_dialog_kb():
    keyboard = [
        [InlineKeyboardButton(text='оценить', callback_data='rate_dialog')]
    ]
    return InlineKeyboardMarkup(keyboard)


def transcribe_dialog_kb():
    keyboard = [
        [InlineKeyboardButton(text='посмотреть транскрипт', callback_data='look_transcribe')]
    ]
    return InlineKeyboardMarkup(keyboard)
