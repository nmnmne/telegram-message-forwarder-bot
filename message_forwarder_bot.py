import logging
import os
import asyncio
from collections import defaultdict
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters

load_dotenv()

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ],
    force=True
)

logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))
TARGET_NUMBERS = {"827", "818", "828", "854", "3632", "2191", "3139", "3355", "2274"}

# Временное хранилище для альбомов
media_groups = defaultdict(list)
media_timers = {}

async def forward_album(media_group_id, context):
    messages = media_groups.pop(media_group_id, [])
    for msg in messages:
        try:
            await msg.forward(chat_id=TARGET_CHAT_ID)
            logging.info(f"✅ Переслано сообщение из альбома")
        except Exception as e:
            logging.error(f"❗ Ошибка при пересылке сообщения из альбома: {e}")

    media_timers.pop(media_group_id, None)

async def schedule_forward_album(media_group_id, context, delay=3):
    await asyncio.sleep(delay)
    if media_group_id in media_groups:
        await forward_album(media_group_id, context)

async def forward_message(update, context):
    message = update.message
    if not message or message.chat_id == TARGET_CHAT_ID:
        return

    text = (message.text or message.caption or "").lower()
    if not text:
        logging.info("Пропущено сообщение без текста или подписи.")
        return

    matched = [num for num in TARGET_NUMBERS if num in text]
    logging.info(f"🔍 Найдены совпадения: {matched}")

    if matched:
        mgid = message.media_group_id
        if mgid:
            media_groups[mgid].append(message)
            logging.info(f"📸 Добавлено сообщение в альбом {mgid} (всего: {len(media_groups[mgid])})")

            if mgid not in media_timers:
                media_timers[mgid] = asyncio.create_task(schedule_forward_album(mgid, context))
        else:
            try:
                await message.forward(chat_id=TARGET_CHAT_ID)
                logging.info(f"✅ Сообщение было перенаправлено: {text}")
            except Exception as e:
                logging.error(f"❗ Ошибка при пересылке: {e}")
    else:
        logging.info(f"❌ Сообщение не было перенаправлено: {text}")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, forward_message))

    logging.info(f"🚀 Бот запущен и отслеживает числа: {', '.join(TARGET_NUMBERS)}")
    application.run_polling()

if __name__ == "__main__":
    main()
