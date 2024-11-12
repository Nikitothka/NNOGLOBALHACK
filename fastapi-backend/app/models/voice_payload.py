from pydantic import BaseModel

class VoicePayload(BaseModel):
    text: str