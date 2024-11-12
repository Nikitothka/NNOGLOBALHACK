# database/models.py
from sqlalchemy import (
    Column, BigInteger, Text, ForeignKey, DateTime, Integer, LargeBinary, Table
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from config import ENCRYPTION_KEY
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

Base = declarative_base()

# Функции для шифрования и дешифрования паролей
def encrypt_password(plain_password):
    password_bytes = plain_password.encode('utf-8')
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY.encode('utf-8')), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(password_bytes) + padder.finalize()
    encrypted_password = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_password  # Конкатенируем IV и зашифрованный пароль

def decrypt_password(encrypted_data):
    iv = encrypted_data[:16]
    encrypted_password = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY.encode('utf-8')), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_password) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data.decode('utf-8')

# Ассоциативная таблица для связи многие-ко-многим между пользователями и группами
user_groups = Table(
    'user_groups',
    Base.metadata,
    Column('user_id', BigInteger, ForeignKey('users.user_id'), primary_key=True),
    Column('group_id', BigInteger, ForeignKey('groups.group_id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    username = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    _password_encrypted = Column(LargeBinary, nullable=False)
    api_key = Column(Text)
    chat_id = Column(BigInteger)

    messages = relationship('Message', back_populates='user')
    business_messages = relationship('BusinessMessage', back_populates='user')
    tasks = relationship('Task', back_populates='assigned_user')
    interactions_from = relationship('Interaction', back_populates='from_user', foreign_keys='Interaction.from_user_id')
    interactions_to = relationship('Interaction', back_populates='to_user', foreign_keys='Interaction.to_user_id')
    groups = relationship('Group', secondary=user_groups, back_populates='users')

    @property
    def password(self):
        return decrypt_password(self._password_encrypted)

    @password.setter
    def password(self, plain_password):
        self._password_encrypted = encrypt_password(plain_password)

class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(BigInteger, primary_key=True)
    title = Column(Text)
    topic = Column(Text)

    messages = relationship('Message', back_populates='group')
    users = relationship('User', secondary=user_groups, back_populates='groups')
    projects = relationship('Project', back_populates='group')

class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    group_id = Column(BigInteger, ForeignKey('groups.group_id'), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    topic = Column(Text)
    title = Column(Text)
    chat_id = Column(BigInteger, nullable=False)
    first_name = Column(Text)

    user = relationship('User', back_populates='messages')
    group = relationship('Group', back_populates='messages')
    interactions = relationship('Interaction', back_populates='message')

class BusinessMessage(Base):
    __tablename__ = 'business_messages'

    message_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    first_name = Column(Text)
    username = Column(Text)

    user = relationship('User', back_populates='business_messages')

class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    group_id = Column(BigInteger, ForeignKey('groups.group_id'), nullable=False)

    group = relationship('Group', back_populates='projects')
    tasks = relationship('Task', back_populates='project')
    interactions = relationship('Interaction', back_populates='project')

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(BigInteger, ForeignKey('projects.project_id'), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Text, default='New')
    priority = Column(Integer)
    assigned_user_id = Column(BigInteger, ForeignKey('users.user_id'))

    project = relationship('Project', back_populates='tasks')
    assigned_user = relationship('User', back_populates='tasks')

class Interaction(Base):
    __tablename__ = 'interactions'

    interaction_id = Column(BigInteger, primary_key=True, autoincrement=True)
    from_user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    to_user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    project_id = Column(BigInteger, ForeignKey('projects.project_id'), nullable=False)
    message_id = Column(BigInteger, ForeignKey('messages.message_id'))
    date = Column(DateTime, default=datetime.utcnow)
    interaction_type = Column(Text)

    from_user = relationship('User', foreign_keys=[from_user_id], back_populates='interactions_from')
    to_user = relationship('User', foreign_keys=[to_user_id], back_populates='interactions_to')
    project = relationship('Project', back_populates='interactions')
    message = relationship('Message', back_populates='interactions')
