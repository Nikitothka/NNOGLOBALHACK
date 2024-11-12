from typing import Annotated, Optional
from datetime import date as DateType
import requests
from pydantic import BaseModel, Field
from team_actions.src.registration import register_action

authorization_data = {}

# Type Hint Definition
UserMessage = Annotated[str, Field(description="Message from user requesting generation")]
DateParam = Annotated[Optional[DateType], Field(description="Date for the summary (optional)")]
GroupName = Annotated[Optional[str], Field(description="Name of the group (optional)")]
TopicName = Annotated[Optional[str], Field(description="Name of the subgroup or topic (optional)")]


# Data Models
class LLMResponse(BaseModel):
    message: str  # Ответ от LLM


@register_action(
    system_type="llm_interaction",
    include_in_plan=True,
    signature="(user_message: UserMessage) -> LLMResponse",
    arguments=["user_message"],
    description="Sends user's generation request to the LLM and returns the response",
)
def request_llm_generation(user_message: UserMessage):
    # Отправляем запрос в LLM с помощью функции из llm_service.py
    response = requests.post(
        "https://aiteamtg.store/llm/api/generate",
        json={"content": user_message}
    )
    response.raise_for_status()
    return response.json()


@register_action(
    system_type="llm_interaction",
    include_in_plan=True,
    signature="(date: DateParam = None, group_name: GroupName = None, topic: TopicName = None) -> LLMResponse",
    arguments=["date", "group_name", "topic"],
    description="Generates a summary of messages from a conversation for the specified day, group, and topic.",
)
def request_daily_summary(
    date: DateParam = None,
    group_name: GroupName = None,
    topic: TopicName = None
) -> LLMResponse:
    """
    Sends a request to generate a daily summary based on optional parameters such as date, group name, and topic.
    """
    # Формируем payload для отправки запроса на LLM
    payload = {
        "date": date.isoformat() if date else None,
        "group_name": group_name,
        "topic": topic
    }
    # Отправляем запрос на LLM
    response = requests.post(
        "https://aiteamtg.store/llm/api/summarize_messages",
        json=payload
    )
    response.raise_for_status()
    data = response.json()
    return LLMResponse(message=data.get("summary", "No summary available."))