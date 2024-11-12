# handlers/__init__.py
from .message_handlers import register_handlers

def setup_handlers(app):
    register_handlers(app)
