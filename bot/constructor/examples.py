from .tools import ConversationHandlerConstructor
from telegram.ext import CommandHandler, ConversationHandler
from telegram import Update


async def start(update, context):

    await update.effective_message.reply_text('привет это chatgpt как тебя зовут')
    # возращает id хендлера, который будет следующим
    # в данный момент я спросил имя и обработаю его в handle_name
    return 0

# объявляю что при /start будет начинаться диалог, начинается с запуска функции start
conv = ConversationHandlerConstructor(start_handlers=[CommandHandler('start', start)])


@conv.handle(0)
async def handle_name(update, context):
    name = update.message.text
    print(name)
    await update.effective_message.reply_text(f'спасибо, {name} сколько тебе лет')
    return 1
# возращает следующий id


@conv.handle(1)
async def handle_age(update: Update, context):
    age = update.message.text
    print(age, 'age')
    if int(age) < 18:
        await update.effective_message.reply_text('спасибо, но вы еще маленький')
        return ConversationHandler.END
    else:
        # возращаем id другого нужного нам хендлера
        await update.effective_message.reply_text('хорошо, введите номер банковской карты для оплаты')
        return 44
# при последнем вопросе возращает это.
# но можно диалог запустить заново коммандой \start так как указали сверху
