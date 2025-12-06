from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from task.schema.task_schema import TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema, TaskFilterSchema

class AbstractTaskRepository(ABC):
    @abstractmethod
    async def create(self, data: TaskCreateSchema, created_by: str) -> TaskResponseSchema:
        pass

    @abstractmethod
    async def read(self, task_id: str) -> TaskResponseSchema:
        pass

    @abstractmethod
    async def get_all(self, filters: Optional[TaskFilterSchema] = None) -> List[TaskResponseSchema]:
        pass

    @abstractmethod
    async def update(self, task_id: str, data: TaskUpdateSchema) -> TaskResponseSchema:
        pass

    @abstractmethod
    async def delete(self, task_id: str) -> bool:
        pass

    @abstractmethod
    async def bulk_update(self, task_ids: List[str], update_data: TaskUpdateSchema) -> List[TaskResponseSchema]:
        pass

    @abstractmethod
    async def get_user_task_distribution(self, user_id: str) -> Dict:
        pass

    @abstractmethod
    async def get_overdue_tasks(self, user_id: Optional[str] = None) -> List[TaskResponseSchema]:
        pass

