from typing import List, Optional
from pydantic import BaseModel

class CTaskPayload(BaseModel):
    title: str
    task_id: str
    column_id: Optional[str] = None
    description: Optional[str] = None
    assigned: Optional[List[str]] = []
