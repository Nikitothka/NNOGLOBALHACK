from fastapi import APIRouter
from fastapi.responses import JSONResponse

chat_router = APIRouter()

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True)
    text = Column(String)
    first_name = Column(String)

@chat_router.get("/get_chat/{task_id}")
def get_keys(task_id):
    # Устанавливаем соединение с PostgreSQL
    engine = create_engine("postgresql://admin:FASDWrergfrw#41@94.241.140.109/aiteam")

    # Создаем сессию
    with Session(engine) as session:
        # Пишем запрос для получения всех записей
        stmt = select(Message)

        # Выполняем запрос и получаем результаты
        results = session.execute(stmt).scalars().all()
        answer = [
            {"text": i.text, "sender": i.first_name} for i in results
        ]

        return JSONResponse(content=answer, status_code=200)
