from typing import List
from task.abstract_repository.abstract_task_repository import AbstractTaskRepository
from task.schema.task_schema import TaskResponseSchema, TaskFilterSchema
from logger import Logger

logger = Logger().get_logger()

class GetAllTasksUseCase:
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository

    async def execute(self, filters: TaskFilterSchema = None) -> List[TaskResponseSchema]:
        try:
            tasks = await self.task_repository.get_all(filters)
            return tasks
        except Exception as e:
            logger.error(f"Error retrieving all tasks at GetAllTasksUseCase: {e}")
            raise e

