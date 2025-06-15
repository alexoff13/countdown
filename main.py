import logging
from datetime import datetime, timedelta
import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
import dotenv

# Задаём дату и время защиты во Владивостоке
VLADIVOSTOK_TZ = pytz.timezone('Asia/Vladivostok')
TARGET_DATETIME = VLADIVOSTOK_TZ.localize(datetime(2025, 7, 7, 10, 0, 0))

async def countdown_message():
    now = datetime.now(VLADIVOSTOK_TZ)
    delta = TARGET_DATETIME - now
    if delta.total_seconds() <= 0:
        return "До защиты осталось 0 дней 0 часов 0 минут"
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"До защиты осталось {days} дней {hours} часа {minutes} минуты"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await countdown_message()
    sent = await update.message.reply_text(msg)
    # Сохраняем id сообщения для обновления
    context.chat_data['countdown_msg_id'] = sent.message_id
    context.chat_data['chat_id'] = sent.chat_id
    # Запускаем задачу обновления каждую минуту
    context.job_queue.run_repeating(update_countdown, interval=30, first=30, chat_id=sent.chat_id)

async def update_countdown(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    app = context.application
    msg_id = context.chat_data.get('countdown_msg_id')
    if not msg_id:
        return
    msg = await countdown_message()
    try:
        await app.bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=msg)
    except Exception as e:
        logging.error(f"Ошибка при обновлении сообщения: {e}")

def main():
    import os
    dotenv.load_dotenv("env")
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        print('Установите переменную окружения TELEGRAM_BOT_TOKEN с токеном бота!')
        return
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.run_polling()

if __name__ == '__main__':
    main()