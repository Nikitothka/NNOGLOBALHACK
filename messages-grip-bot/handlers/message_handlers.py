# handlers/message_handlers.py
import logging
from pyrogram import Client, filters, types
from database.crud import add_message, add_business_message
from models import MessageModel, BusinessMessageModel
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_handlers(app: Client):

    @app.on_message(filters.group & ~filters.command('sum'))
    async def handle_group_message(client, message: types.Message):
        logger.info('Group message received')

        # Извлечение темы форума, если она есть
        if hasattr(message, 'forum_topic') and message.forum_topic:
            topic = message.forum_topic.title
        else:
            topic = "None"

        message_data = MessageModel(
            message_id=message.id,
            user_id=message.from_user.id if message.from_user else 0,
            username=message.from_user.username if message.from_user else "",
            text=message.text or message.caption or "",
            topic=topic,
            date=message.date or datetime.utcnow(),
            title=message.chat.title if message.chat else "None",
            chat_id=message.chat.id if message.chat else 0,
            first_name=message.from_user.first_name if message.from_user else ""
        )

        try:
            add_message(message_data)
            logger.info(f"Message {message.id} added to the database.")
        except Exception as e:
            logger.error(f"Error adding message {message.id}: {e}")

    @app.on_message(filters.business & ~filters.command('sum'))
    async def handle_private_message(client, message: types.Message):
        logger.info('business message received')
        business_message_data = BusinessMessageModel(
            message_id=message.id,
            user_id=message.from_user.id if message.from_user else 0,
            username=message.from_user.username if message.from_user else "",
            text=message.text or message.caption or "",
            date=message.date or datetime.utcnow(),
            first_name=message.from_user.first_name if message.from_user else ""
        )

        try:
            add_business_message(business_message_data)
            logger.info(f"Business message {message.id} added to the database.")
        except Exception as e:
            logger.error(f"Error adding business message {message.id}: {e}")
