from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from task.enum.task_status_enum import TaskStatus
from task.enum.task_priority_enum import TaskPriority

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Task status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    assignee_id: Optional[str] = Field(None, description="User ID assigned to this task")
    tags: List[str] = Field(default_factory=list, description="Task tags")
    subtasks: List[str] = Field(default_factory=list, description="List of subtask IDs")
    dependencies: List[str] = Field(default_factory=list, description="List of task IDs this task depends on")
    collaborators: List[str] = Field(default_factory=list, description="List of user IDs collaborating on this task")

    class Config:
        from_attributes = True
        use_enum_values = True

class TaskCreateSchema(TaskBase):
    pass

class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[str] = None
    tags: Optional[List[str]] = None
    subtasks: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None
    collaborators: Optional[List[str]] = None

    class Config:
        use_enum_values = True

class TaskResponseSchema(TaskBase):
    id: str
    created_by: str
    blocked_by: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

class BulkUpdateSchema(BaseModel):
    task_ids: List[str] = Field(..., description="List of task IDs to update")
    update_data: TaskUpdateSchema = Field(..., description="Data to update for all tasks")

class TaskFilterSchema(BaseModel):
    status: Optional[List[TaskStatus]] = None
    priority: Optional[List[TaskPriority]] = None
    assignee_id: Optional[str] = None
    created_by: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    search: Optional[str] = None  
    filter_logic: str = Field(default="AND", description="AND or OR logic for multiple filters")

    class Config:
        use_enum_values = True

class TaskDistributionResponse(BaseModel):
    user_id: str
    total_tasks: int
    tasks_by_status: dict
    tasks_by_priority: dict
    overdue_tasks: int
    overdue_task_ids: List[str]

class TaskAnalyticsResponse(BaseModel):
    total_tasks: int
    tasks_by_status: dict
    tasks_by_priority: dict
    user_distributions: List[TaskDistributionResponse]

