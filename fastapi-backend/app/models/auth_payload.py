from pydantic import BaseModel

class AuthPayload(BaseModel):
    login: str
    password: str