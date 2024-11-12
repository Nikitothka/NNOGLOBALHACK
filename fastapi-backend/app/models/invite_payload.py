from pydantic import BaseModel

class InvitePayload(BaseModel):
    email: str
    