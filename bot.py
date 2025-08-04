import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Папка для загрузки
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Скачивание mp3
def download_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = ydl.prepare_filename(info).rsplit('.', 1)[0]
        return title + ".mp3"

# /music команда
async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Пришли ссылку: /music https://www.youtube.com/watch?v=...")
        return

    url = context.args[0]
    await update.message.reply_text("⏬ Скачиваю...")

    try:
        path = download_mp3(url)
        with open(path, 'rb') as audio:
            await update.message.reply_audio(audio)
        os.remove(path)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Отправь команду /music <ссылка на YouTube>, и я пришлю mp3!")

# Запуск
app = ApplicationBuilder().token("Token").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("music", music))

app.run_polling()
