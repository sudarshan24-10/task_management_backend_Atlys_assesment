from task.abstract_repository.abstract_task_repository import AbstractTaskRepository
from task.schema.task_schema import TaskResponseSchema
from logger import Logger

logger = Logger().get_logger()

class GetTaskByIdUseCase:
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository

    async def execute(self, task_id: str) -> TaskResponseSchema:
        try:
            task = await self.task_repository.read(task_id)
            return task
        except Exception as e:
            logger.error(f"Error retrieving task by ID at GetTaskByIdUseCase: {e}")
            raise e

