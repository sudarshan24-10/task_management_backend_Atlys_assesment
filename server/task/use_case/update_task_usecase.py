from task.abstract_repository.abstract_task_repository import AbstractTaskRepository
from task.schema.task_schema import TaskUpdateSchema, TaskResponseSchema
from logger import Logger

logger = Logger().get_logger()

class UpdateTaskUseCase:
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository

    async def execute(self, task_id: str, task_data: TaskUpdateSchema) -> TaskResponseSchema:
        try:
            updated_task = await self.task_repository.update(task_id, task_data)
            return updated_task
        except Exception as e:
            logger.error(f"Error updating task at UpdateTaskUseCase: {e}")
            raise e

