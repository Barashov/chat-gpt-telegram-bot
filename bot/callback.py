from telegram import Update, Message
from telegram.constants import ChatAction
from prompt import get_rate_dialog_prompt, transcribe
import openai
from kb import transcribe_dialog_kb
import settings


async def callback_rate_dialog(update: Update, context):
    await update.effective_user.send_action(action=ChatAction.TYPING)
    message: Message = await update.effective_message.reply_text(text='запрос к gpt-4 отправлен')
    content = get_rate_dialog_prompt(update.callback_query.message.text)

    openai.api_key = settings.OPENAI_API_KEY
    messages = [{"role": "user", "content": content}]
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=messages,
        temperature=1,
        stream=True)

    text = ''
    for chunk in response:
        chunk_text = chunk["choices"][0].get("delta").get("content")
        if chunk_text is not None:
            if '\n' in chunk_text:
                text += chunk_text
                await message.edit_text(text)
                continue
            text += chunk_text
    else:
        await message.edit_reply_markup(transcribe_dialog_kb())


async def look_transcribe_callback(update: Update, context):
    await update.effective_user.send_action(action=ChatAction.TYPING,
                                            read_timeout=4.0)
    await update.effective_message.reply_text(text=transcribe)
