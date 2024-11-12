from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import os
from app.services.gigachat_service.system_prompts import SystemPrompts

class GigaChatService:
    def __init__(self):
        # Авторизация в сервисе GigaChat
        self.chat = GigaChat(credentials=os.getenv("GIGACHAT_API_KEY"), verify_ssl_certs=False,
                             scope="GIGACHAT_API_PERS", model="GigaChat", )

    def send_message(self, user_message):
        messages = [HumanMessage(content=user_message)]
        result = self.chat(messages)
        return result.content

    def send_message_for_summury(self, tg_messages):
        messages = [SystemMessage(content=SystemPrompts.summury_prompt),
                    HumanMessage(content=tg_messages)]
        result = self.chat(messages)
        return result.content


