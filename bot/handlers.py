import os
from telegram import Update
from telegram.ext import ContextTypes
from utils import transcribe, chop_audio, extract_audio_from_video, streaming_transcribe
from pydub import AudioSegment
from uuid import uuid4


async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text('запрос отправлен')
    audio = update.message.audio
    if audio:
        file_id = update.message.audio.file_id
        file_size = update.message.audio.file_size
    else:
        file_id = update.message.voice.file_id
        file_size = update.message.voice.file_size

    if file_size < 24 * 1024 * 1024:

        file = await context.bot.getFile(file_id)

        filename = f'./file/{uuid4()}.mp3'
        await file.download_to_drive(filename)

        audio = AudioSegment.from_file(filename)
        os.remove(filename)

        await streaming_transcribe(audio, update)

    else:
        await update.effective_message.reply_text('file is too big')


async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text('запрос отправлен')

    video_note = update.message.video_note
    if video_note:
        file_id = video_note.file_id
    else:
        file_id = update.message.video
    # получаем видео
    file = await context.bot.getFile(file_id, read_timeout=30)
    # сохраняем видео
    video_name = f'./file/{uuid4()}.mp4'
    await file.download_to_drive(video_name)
    # вытаскиваем аудио из видео
    audio = extract_audio_from_video(video_name)
    os.remove(video_name)

    audio_name = f'./file/{uuid4()}.mp3'
    audio.write_audiofile(audio_name)

    audio = AudioSegment.from_file(audio_name)
    os.remove(audio_name)

    await streaming_transcribe(audio, update)

