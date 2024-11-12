from fastapi import HTTPException, APIRouter
import logging
from settings import userbot

from app.models.voice_payload import VoicePayload

bot_router = APIRouter()


@bot_router.post("/voice")
async def send_text(payload: VoicePayload):
    target_user_id = 7232670177  # Укажите целевой Telegram ID пользователя

    try:
        # Отправка сообщения пользователю
        await userbot.send_message(chat_id=target_user_id, text=payload.text)
        logging.info(f"Sent message to user {target_user_id}: {payload.text}")
        return {"status": "success", "message": f"Message sent to {target_user_id}"}
    except Exception as e:
        logging.error(f"Failed to send message: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")
