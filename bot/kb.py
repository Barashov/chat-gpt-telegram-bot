from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def rate_dialog_kb(message_id):
    keyboard = [
        [InlineKeyboardButton(text='оценить', callback_data='rate_dialog_')]
    ]
    return InlineKeyboardMarkup(keyboard)


def transcribe_dialog_kb():
    keyboard = [
        [InlineKeyboardButton(text='посмотреть транскрипт', callback_data='look_transcribe')]
    ]
    return InlineKeyboardMarkup(keyboard)
