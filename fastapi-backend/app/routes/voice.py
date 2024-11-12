from app.models.voice_payload import VoicePayload
from fastapi import APIRouter

voice_router = APIRouter()

@voice_router.post("/voice")
def send_voice(payload: VoicePayload):
    print(payload)
