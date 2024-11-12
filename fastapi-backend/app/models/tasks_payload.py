from typing import List, Optional

from pydantic import BaseModel

class TaskPayload(BaseModel):
    title: str
    description: Optional[str] = None
    archived: Optional[bool] = False
    completed: Optional[bool] = False
    assigned: Optional[List[str]] = []
    deadline: Optional[int] = None
