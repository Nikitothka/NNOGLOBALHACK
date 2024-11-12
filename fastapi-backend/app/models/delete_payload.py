from pydantic import BaseModel

class DeletePayload(BaseModel):
    title: str