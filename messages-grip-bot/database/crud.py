# database/crud.py
from .models import User, Message, Group, BusinessMessage, user_groups
from . import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import MessageModel, BusinessMessageModel

def add_user(session: Session, user_data):
    try:
        user = User(
            user_id=user_data['user_id'],
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            api_key=user_data.get('api_key'),
            chat_id=user_data.get('chat_id')
        )
        user.password = user_data['password']
        session.add(user)
        session.commit()
        print(f"User {user.user_id} added successfully.")
    except IntegrityError:
        session.rollback()
        print(f"User {user_data['user_id']} already exists.")

def get_user(session: Session, user_id: int):
    return session.query(User).filter_by(user_id=user_id).first()

def add_message(message_data: MessageModel):
    db = SessionLocal()
    try:
        # Проверяем и добавляем пользователя, если его нет
        user = get_user(db, message_data.user_id)
        if not user:
            user_data = {
                'user_id': message_data.user_id,
                'username': message_data.username,
                'first_name': message_data.first_name,
                'password': 'default_password',
                'api_key': '',
                'chat_id': message_data.chat_id
            }
            add_user(db, user_data)
            user = get_user(db, message_data.user_id)

        # Проверяем и добавляем группу, если её нет
        group = db.query(Group).filter_by(group_id=message_data.chat_id).first()
        if not group:
            group = Group(
                group_id=message_data.chat_id,
                title=message_data.title,
                topic=message_data.topic
            )
            db.add(group)
            db.commit()
            print(f"Group {group.group_id} added successfully.")

        # Связываем пользователя и группу
        if not db.query(user_groups).filter_by(user_id=user.user_id, group_id=group.group_id).first():
            db.execute(user_groups.insert().values(user_id=user.user_id, group_id=group.group_id))
            db.commit()
            print(f"User {user.user_id} linked to group {group.group_id}.")

        # Добавляем сообщение
        message = Message(
            message_id=message_data.message_id,
            user_id=message_data.user_id,
            group_id=message_data.chat_id,
            text=message_data.text,
            date=message_data.date,
            topic=message_data.topic,
            title=message_data.title,
            chat_id=message_data.chat_id,
            first_name=message_data.first_name
        )
        db.add(message)
        db.commit()
        print(f"Message {message.message_id} added to the database.")
    except Exception as e:
        db.rollback()
        print(f"Error adding message: {e}")
    finally:
        db.close()

def add_business_message(business_message_data: BusinessMessageModel):
    db = SessionLocal()
    try:
        # Проверяем и добавляем пользователя, если его нет
        user = get_user(db, business_message_data.user_id)
        if not user:
            user_data = {
                'user_id': business_message_data.user_id,
                'username': business_message_data.username,
                'first_name': business_message_data.first_name,
                'password': 'default_password',
                'api_key': '',
                'chat_id': 0
            }
            add_user(db, user_data)
            user = get_user(db, business_message_data.user_id)

        # Добавляем бизнес-сообщение
        business_message = BusinessMessage(
            message_id=business_message_data.message_id,
            user_id=business_message_data.user_id,
            text=business_message_data.text,
            date=business_message_data.date,
            first_name=business_message_data.first_name,
            username=business_message_data.username
        )
        db.add(business_message)
        db.commit()
        print(f"Business message {business_message.message_id} added to the database.")
    except Exception as e:
        db.rollback()
        print(f"Error adding business message: {e}")
    finally:
        db.close()
