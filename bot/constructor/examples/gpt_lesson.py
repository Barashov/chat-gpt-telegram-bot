from constructor.tools import ConversationHandlerConstructor, send_text, prompt
from telegram.ext import Application, CommandHandler, ConversationHandler
from telegram import Update


async def start_dialog(update: Update, context):
    text = """
    Приветствую! Я - учебный бот, созданный, чтобы помочь вам узнать больше о chat gpt.\
    Попробуйте написать "`Расскажи мне что-нибудь интересное о космосе`".
    
    """
    await send_text(update, text)
    return 0


# диалог начинается с какого то события, в данном случае он начинается, если пользователь введет "/start"
start_dialog_handler = CommandHandler('start', start_dialog)
# может быть несколько стартовых хендлеров, передаем список
conv = ConversationHandlerConstructor(start_handlers=[start_dialog_handler, ])


@conv.handle(0)
async def handle_first_message(update: Update, context):
    # в прошлом сообщении мы попросили отправить пользователя запрос к гпт
    # здесь мы обработаем его сообщение

    # берем сообщение пользователя
    text = update.message.text
    message = await send_text(update, 'Запрос к chat gpt отправлен')

    response_text = await prompt(text)
    await message.edit_text(response_text)
    await send_text(update, 'Напишите ваш email, чтобы мы могли отправить вам информацию')
    return 1


@conv.handle(1)
async def handle_email(update: Update, context):
    email = update.message.text
    print(email)
    await send_text(update, 'Спасибо! информация придет на указанный email')
    return ConversationHandler.END


def init_handlers(application: Application):
    application.add_handler(conv.build())
