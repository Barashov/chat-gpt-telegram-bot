import os
from telegram import Update
from telegram.ext import ContextTypes
from utils import extract_audio_from_video, streaming_transcribe, num_tokens_from_messages
from utils import get_data, stream_response
from pydub import AudioSegment
from uuid import uuid4
from prompt import system_message


async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text('запрос отправлен')
    audio = update.message.audio
    if audio:
        file_id = update.message.audio.file_id
    else:
        file_id = update.message.voice.file_id

    file = await context.bot.getFile(file_id, read_timeout=None, write_timeout=None)

    audio = AudioSegment.from_file(file.file_path)

    await streaming_transcribe(audio, update)


async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text('запрос отправлен')

    video_note = update.message.video_note
    if video_note:
        file_id = video_note.file_id
    else:
        file_id = update.message.video.file_id

    file = await context.bot.getFile(file_id, read_timeout=None, write_timeout=None)

    audio = extract_audio_from_video(file.file_path)

    audio_name = f'/app/bot/file/{uuid4()}.mp3'
    audio.write_audiofile(audio_name)

    audio = AudioSegment.from_file(audio_name)
    os.remove(audio_name)

    await streaming_transcribe(audio, update)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.effective_message.reply_text('запрос отправлен')
    text = update.message.text
    messages = context.user_data.get('messages')
    if messages is None:
        messages = [{'role': 'system',
                     'content': system_message},
                    {'role': 'system',
                     'content': f'в магазине есть эти товары: {get_data()}'}]

    messages.append({'role': 'user',
                     'content': text})

    while True:
        if num_tokens_from_messages(messages) > 16000:
            messages.pop(2)
        else:
            break

    response_text = await stream_response(messages, update, message)

    messages.append({'role': 'assistant',
                     'content': response_text})

    context.user_data['messages'] = messages
