from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date

# Подключение к базе данных
DATABASE_URL = "postgresql+psycopg2://admin:FASDWrergfrw#41@94.241.140.109:5432/aiteam"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определение модели таблицы
Base = declarative_base()


class BMessages(Base):
    __tablename__ = "business_messages"

    message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    text = Column(String)
    date = Column(TIMESTAMP)
    first_name = Column(String)
    username = Column(String)

class Messages(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    group_id = Column(Integer)
    text = Column(String)
    date = Column(TIMESTAMP)
    topic = Column(String)
    title = Column(String)
    chat_id = Column(Integer)
    first_name = Column(String)


# Создание сессии и выполнение запроса SELECT
def get_bmessages(date=date.today(), first_name=None):
    session = SessionLocal()
    messages_s = []
    try:
        query = session.query(BMessages)

        if date:
            query = query.filter(func.date(BMessages.date) == date)
        if first_name:
            query = query.filter(BMessages.first_name == first_name)

        messages = query.all()

        for i in messages:
            messages_s.append(i.text)
    finally:
        session.close()

    print(messages_s)

# Создание сессии и выполнение запроса SELECT
def get_messages(date=date.today(), title=None, topic=None):
    session = SessionLocal()
    messages_s = []
    try:
        query = session.query(Messages)

        if date:
            query = query.filter(func.date(Messages.date) == date)
        if title:
            query = query.filter(Messages.title == title)
        if topic:
            query = query.filter(Messages.topic == topic)

        messages = query.all()

        for i in messages:
            messages_s.append(i.text)
    finally:
        session.close()

    print(messages_s)

