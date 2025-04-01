from telegram.ext import Application, MessageHandler, filters
import logging
from pytz import utc
from dotenv import load_dotenv
import os


load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") # Бот, админ в группе источника и получателя
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID")) # Чат куда пересылаем сообщения

async def forward_message(update, context):
    # Не копируем сообщения из целевого чата
    if update.message.chat_id != TARGET_CHAT_ID:
        await update.message.forward(chat_id=TARGET_CHAT_ID)

def main():
    application = Application.builder() \
        .token(TOKEN) \
        .arbitrary_callback_data(True) \
        .build()
    
    application.add_handler(MessageHandler(filters.ALL, forward_message))
    
    print("Бот включён...")
    application.run_polling()

if __name__ == "__main__":
    main()
