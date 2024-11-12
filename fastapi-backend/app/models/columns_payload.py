from pydantic import BaseModel

class ColumnPayload(BaseModel):
    title: str
    board_id: str
