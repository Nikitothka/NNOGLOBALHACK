# models.py
from pydantic import BaseModel
from datetime import datetime

class MessageModel(BaseModel):
    message_id: int
    user_id: int
    username: str
    text: str
    topic: str
    date: datetime
    title: str
    chat_id: int
    first_name: str

class BusinessMessageModel(BaseModel):
    message_id: int
    user_id: int
    username: str
    text: str
    date: datetime
    first_name: str
