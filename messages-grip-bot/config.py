# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Конфигурация Telegram API
API_ID = os.getenv('api_id')
API_HASH = os.getenv('api_hash')
BOT_TOKEN = os.getenv('bot_token')



if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("Пожалуйста, задайте API_ID, API_HASH и BOT_TOKEN в файле .env.")

# Ключ шифрования для паролей (должен быть длиной 16, 24 или 32 байта)
ENCRYPTION_KEY = os.getenv('key_bd_en')
if ENCRYPTION_KEY is None or len(ENCRYPTION_KEY.encode('utf-8')) not in (16, 24, 32):
    raise ValueError("Некорректный ENCRYPTION_KEY. Он должен быть длиной 16, 24 или 32 байта.")

# URL базы данных
DATABASE_URL = 'postgresql://admin:FASDWrergfrw#41@94.241.140.109:5432/aiteam?sslmode=disable'

