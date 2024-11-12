# app.py
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import setup_handlers
from database.models import Base
from database import engine

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = Client("321123aerogram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Регистрация обработчиков
setup_handlers(app)

# Запуск бота
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
