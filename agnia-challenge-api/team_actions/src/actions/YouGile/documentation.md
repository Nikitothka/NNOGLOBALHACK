# TypeHints Definition
Id = Annotated[str, Field(description="Unique identifier")]
TaskTitle: Annotated[str, Field(description="A well-crafted task name.")]
Column: Annotated[str, Field(description="Name of the column")]
Description: Annotated[str, Field(description="Task description")]
IsArchived: Annotated[bool, Field(description="Whether the task is archived")]
IsCompleted: Annotated[bool, Field(description="Whether the task is completed")]
AssignedUserIds: Annotated[List[str], Field(description="List of user IDs assigned to the task")]
DeadlineUnix: Annotated[int, Field(description="Deadline as Unix timestamp")]

# Models Definition
class TaskUpdatePayload(BaseModel):
    new_title: Optional[TaskTitle]
    old_title: Optional[TaskTitle]
    new_column: Optional[Column]
    description: Optional[Description]
    archived: Optional[IsArchived]
    completed: Optional[IsCompleted]
    deadline: Optional[DeadlineUnix]

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
    description: Description
    archived: IsArchived
    completed: IsCompleted
    assigned: AssignedUserIds
    deadline: DeadlineUnix
    created_at: str  # ISO 8601 datetime string
    updated_at: str  # ISO 8601 datetime string


# API Calls Documentation
## `create_task`

**Description**:
Creates a new task on the kanban board with optional parameters, like descriptions, column id and deadline.

**Parameters**:
- title (TaskTitle): The title of the task to be created, based on the main action or objective inferred from the user's message.
- description (Optional[Description]): A brief description of the task, incorporating any additional context or specifics mentioned by the user.
- archived (Optional[IsArchived]): Indicates if the task should be archived immediately upon creation. Defaults to False.
- completed (Optional[IsCompleted]): Indicates if the task is already completed upon creation. Defaults to False.
- assigned (Optional[List[AssignedUserIds]]): A list of user IDs for assigning the task to specific users, derived from names or references in the user's message.
- deadline (Optional[DeadlineUnix]): The task's deadline, expressed as a Unix timestamp. Extract any date references from the user's message and convert them accordingly.


**Returns**:
created_task (Task)


## `change_task`

**Description**:

Updates an existing task on the kanban board. Use this function to change properties such as the title, column, description, or status of a task.

**Parameters**:

- **new_title** (`Optional[TaskTitle]`):  
  The new title for the task if it is being changed. Leave `None` if the title is unchanged.

- **old_title** (`TaskTitle`):  
  The current title of the task, used to identify it for the update. It must be or nothing will work

- **new_column** (`Optional[ColumnId]`):  
  The ID of the new column for the task. Leave `None` if the column is unchanged.

- **description** (`Optional[Description]`):  
  An updated description for the task. Leave `None` if the description is unchanged.

- **archived** (`Optional[IsArchived]`):  
  A boolean indicating if the task should be archived or not. Leave `None` if this status is unchanged.

- **completed** (`Optional[IsCompleted]`):  
  A boolean indicating if the task should be marked as completed. Leave `None` if this status is unchanged.

- **deadline** (`Optional[DeadlineUnix]`):  
  The updated deadline for the task, represented as a Unix timestamp. Leave `None` if the deadline is unchanged.

**Returns**:

- **updated_task** (`Task`):  
  The task object that was updated, including all the current values.

**Usage Example**

When a user provides a message like:

- "Change the title of the 'Design Homepage' task to 'Revise Homepage Design' and move it to the 'In Progress' column."

The model should parse this to:

- **new_title**: "Revise Homepage Design"
- **old_title**: "Design Homepage"
- **new_column**: ID of the "In Progress" column
- **description**: `None` (unchanged)
- **archived**: `None` (unchanged)
- **completed**: `None` (unchanged)
- **deadline**: `None` (unchanged)

