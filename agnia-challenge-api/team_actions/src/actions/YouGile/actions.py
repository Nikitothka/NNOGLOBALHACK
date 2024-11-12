# action.py
from typing import Annotated, List, Optional
from pydantic import BaseModel, Field

from team_actions.src.registration import register_action
from team_actions.src.settings import Settings
import requests

authorization_data = {}
# Это поле будет автоматически заполнено авторизационными данными после регистрации действий.

# Определение Type Hints
Id = Annotated[str, Field(description="Current state ID name")]
TaskTitle = Annotated[str, Field(description="Updated title of the task")]
Description = Annotated[str, Field(description="Updated description of the task")]
IsArchived = Annotated[bool, Field(description="Indicates if the task is archived")]
IsCompleted = Annotated[bool, Field(description="Indicates if the task is completed")]
AssignedUserIds = Annotated[List[str], Field(description="List of user IDs assigned to the task")]
DeadlineUnix = Annotated[int, Field(description="Updated deadline as a Unix timestamp")]
Column = Annotated[str, Field(description="Name of the column")]


# Data Models
class TaskUpdatePayload(BaseModel):
    new_title: Optional[TaskTitle]
    old_title: Optional[TaskTitle]
    new_column: Optional[Column]
    description: Optional[Description]
    archived: Optional[IsArchived]
    completed: Optional[IsCompleted]
    deadline: Optional[DeadlineUnix]


# Модели данных
class TaskPayload(BaseModel):
    title: TaskTitle
    description: Description
    archived: IsArchived
    completed: IsCompleted
    assigned: AssignedUserIds
    deadline: DeadlineUnix


class Task(BaseModel):
    id: Id
    title: TaskTitle
    column_id: Id
    description: Description
    archived: IsArchived
    completed: IsCompleted
    assigned: AssignedUserIds
    deadline: DeadlineUnix
    created_at: str  # ISO 8601 datetime string
    updated_at: str  # ISO 8601 datetime string


@register_action(
    system_type="task_tracker",
    include_in_plan=True,
    signature="(title: TaskTitle, description: Description, archived: Archived, completed: Completed, "
              "assigned: AssignedList, deadline: Deadline) -> Task",
    arguments=[
        "title",
        "description",
        "archived",
        "completed",
        "assigned",
        "deadline"
    ],
    description="Creates a new task",
)
def create_task(
        title: TaskTitle,
        description: Description,
        archived: IsArchived,
        completed: IsCompleted,
        assigned: AssignedUserIds,
        deadline: DeadlineUnix
) -> Task:
    payload = {k: v for k, v in {"title": "New Task",
                                 "description": "Description of the task",
                                 "archived": False,
                                 "completed": False,
                                 "assigned": ["user1", "user2"],
                                 "deadline": 1683302400
                                 }.items() if v is not None}
    response = requests.post(
        "https://aiteamtg.store/yougile/api/tasks",
        json={
            "title": title,
            "description": description,
            "archived": archived,
            "completed": completed,
            "assigned": assigned,
            "deadline": deadline
        },
    )

    response.raise_for_status()
    data = response.json()
    return data


@register_action(
    system_type="task_tracker",
    include_in_plan=True,
    signature="(new_title: Optional[TaskTitle] = None, old_title: Optional[TaskTitle] = None, new_column: Optional["
              "ColumnId] = None, description: Optional[Description] = None, archived: Optional[IsArchived] = None, "
              "completed: Optional[IsCompleted] = None, deadline: Optional[DeadlineUnix] = None) -> Task",
    arguments=[
        "new_title",
        "old_title",
        "new_column",
        "description",
        "archived",
        "completed",
        "deadline"
    ],
    description="Updates an existing task on the kanban board",
)
def change_task(
        new_title: Optional[TaskTitle] = None,
        old_title: Optional[TaskTitle] = None,
        new_column: Optional[Column] = None,
        description: Optional[Description] = None,
        archived: Optional[IsArchived] = None,
        completed: Optional[IsCompleted] = None,
        deadline: Optional[DeadlineUnix] = None
):
    json_data = {k: v for k, v in {
        "title": new_title,
        "task_id": old_title,
        "column_id": new_column,
        "description": description
    }.items() if v is not None}
    response = requests.put(
        "https://aiteamtg.store/yougile/api/change_task",
        json=json_data
    )
    # response.raise_for_status()
    data = response.json()
    return json_data
