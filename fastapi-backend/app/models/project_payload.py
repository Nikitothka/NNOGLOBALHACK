from pydantic import BaseModel

class ProjectsPayload(BaseModel):
    title: str
