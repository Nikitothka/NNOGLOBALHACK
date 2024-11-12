from pydantic import BaseModel

class BoardPayload(BaseModel):
    title: str
    project_id: str