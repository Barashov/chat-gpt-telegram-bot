from telegram.ext import ConversationHandler, MessageHandler, filters
from telegram import Update, Message
import openai
import settings

openai.api_key = settings.OPENAI_API_KEY


class ConversationHandlerConstructor:
    def __init__(self, start_handlers: list, fallbacks: list = None):
        if fallbacks is None:
            self.fallbacks = []
        else:
            self.fallbacks = fallbacks
        self.start_handlers = start_handlers
        self.states = {}

    def build(self):
        return ConversationHandler(entry_points=self.start_handlers,
                                   fallbacks=self.fallbacks,
                                   states=self.states)

    def handle(self, number):
        """
        @param number: каким номером будет вызываться хендлер
        @return: None
        """

        def wrapper(func):
            self.states[number] = [MessageHandler(filters=filters.ALL, callback=func)]
        return wrapper


async def send_text(update: Update, text: str) -> Message:
    return await update.effective_message.reply_markdown(text=text)


async def prompt(text: str) -> str:
    messages = [{'role': 'user',
                 'content': text}]
    response = await openai.ChatCompletion.acreate(messages=messages, model='gpt-3.5-turbo')
    return response.choices[0]['message']['content']
