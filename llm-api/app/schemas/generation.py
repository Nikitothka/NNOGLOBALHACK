from pydantic import BaseModel


class GigaChatRequest(BaseModel):
    content: str


class GigaChatResponse(BaseModel):
    response_text: str
