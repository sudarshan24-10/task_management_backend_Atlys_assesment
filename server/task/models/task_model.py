from beanie import Document, Indexed
from typing import Annotated, List, Optional
from datetime import datetime
from pydantic import Field
from task.enum.task_status_enum import TaskStatus
from task.enum.task_priority_enum import TaskPriority

class Task(Document):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = None
    assignee_id: Optional[str] = None  # User ID
    created_by: str = Field(...)  # User ID who created the task
    tags: List[str] = Field(default_factory=list)
    subtasks: List[str] = Field(default_factory=list)  # List of subtask IDs
    dependencies: List[str] = Field(default_factory=list)  # List of task IDs this task depends on
    blocked_by: List[str] = Field(default_factory=list)  # List of task IDs that block this task
    collaborators: List[str] = Field(default_factory=list)  # List of user IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tasks"
        indexes = [
            "assignee_id",
            "status",
            "priority",
            "created_by",
            "due_date",
        ]

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()

