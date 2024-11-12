from pydantic import BaseModel


class RecognitionResponse(BaseModel):
    text: str


class RecognitionMessage(BaseModel):
    audio: bytes
