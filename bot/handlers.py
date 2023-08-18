import os
from telegram import Update
from telegram.ext import ContextTypes
from utils import transcribe, chop_audio, extract_audio_from_video, streaming_transcribe, is_subscribed_decorator
from pydub import AudioSegment
from uuid import uuid4


@is_subscribed_decorator
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


@is_subscribed_decorator
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

