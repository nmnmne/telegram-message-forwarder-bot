from telegram.ext import Application, MessageHandler, filters
import logging
import re
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

# Фильтр по содержанию
TARGET_NUMBERS = {"500", "600"}

async def forward_message(update, context):
    # Игнорируем сообщения из целевого чата
    if update.message.chat_id == TARGET_CHAT_ID:
        return

    if update.message.text:
        text = update.message.text
        found_numbers = re.findall(r'\d+', text)

        if any(num in TARGET_NUMBERS for num in found_numbers):
            await update.message.forward(chat_id=TARGET_CHAT_ID)
            print(f"✅ Сообщение было перенаправлено: {text}")
        else:
            print(f"❌ Сообщение не было перенаправлено: {text}")

def main():
    application = Application.builder() \
        .token(TOKEN) \
        .arbitrary_callback_data(True) \
        .build()

    application.add_handler(MessageHandler(filters.ALL, forward_message))

    print("Бот включён и отслеживает числа:", TARGET_NUMBERS)
    application.run_polling()

if __name__ == "__main__":
    main()
