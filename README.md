# Telegram Message Forwarder Bot

Бот для автоматической пересылки сообщений между чатами Telegram.

## 📋 Описание
Бот пересылает все сообщения (текст, медиа, документы) из одного чата в другой, исключая циклические пересылки.

## 🛠 Технологии
- Python 3.11
- python-telegram-bot 20.0
- python-dotenv

## ⚙️ Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your_username/message_forwarder_bot.git
cd message_forwarder_bot
```
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
# Linux/Mac:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env:
```bash
# Токен вашего Telegram бота (получаем у @BotFather)
TELEGRAM_BOT_TOKEN=ваш_токен_бота_здесь

# ID чата, куда будут пересылаться сообщения (получаем c помощью @getidsbot)
TARGET_CHAT_ID=сюда_вставить_id_целевого_чата
```

## 🚀 Запуск
```bash
python message_forwarder_bot.py
```
