from task.abstract_repository.abstract_task_repository import AbstractTaskRepository
from task.schema.task_schema import TaskCreateSchema, TaskResponseSchema
from logger import Logger

logger = Logger().get_logger()

class CreateTaskUseCase:
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository

    async def execute(self, task_data: TaskCreateSchema, created_by: str) -> TaskResponseSchema:
        try:
            created_task = await self.task_repository.create(task_data, created_by)
            return created_task
        except Exception as e:
            logger.error(f"Error creating task at CreateTaskUseCase: {e}")
            raise e

