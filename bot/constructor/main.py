"""
файл, в котором будет содаваться основная логика бота,
"""
from telegram.ext import Application, MessageHandler, filters
from .examples import conv


def add_handlers(application: Application):
    """
    добавляет новые хендлеры или заменяет старые. пример: в боте есть хендлер
    для текста, но захотелось сделать свой
    """
    # application.add_handler(MessageHandler(filters=filters.TEXT, callback=handler))
    application.add_handler(conv.build())
    print(conv.states)
