from dotenv import load_dotenv
import os
from pyrogram import Client

load_dotenv()

main_url = 'https://ru.yougile.com/api-v2/'

headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('key')}"
}

api_id = '14776716'
api_hash = '69fc778931cdcfe5f40253c20a8767ac'
session_name = 'botApi_session'

# Определяем путь для сохранения сессии в текущей директории
session_path = os.path.join(os.getcwd(), f"{session_name}.session")


# Инициализация Pyrogram клиента с указанием пути к файлу сессии
userbot = Client(session_path, api_id=api_id, api_hash=api_hash)
