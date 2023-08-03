from telegram.ext import ConversationHandler, MessageHandler, filters


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
