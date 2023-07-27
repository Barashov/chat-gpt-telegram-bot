from telegram import Update
from prompt import get_rate_dialog_prompt
from telegram.ext import ConversationHandler, ContextTypes
from openai_helper import handle_message
import settings


async def asking_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    seller_name = update.message.text
    context.user_data['seller_name'] = seller_name
    await update.effective_message.reply_text('Как зовут клиента?')
    return settings.ASKING_CLIENT


async def asking_client(update: Update, context):
    client_name = update.message.text

    message = await update.effective_message.reply_text(f'запрос отправлен')
    prompt = get_rate_dialog_prompt(context.user_data['audio_text'],
                                    context.user_data['seller_name'],
                                    client_name)
    await handle_message(prompt, message)

    return ConversationHandler.END
