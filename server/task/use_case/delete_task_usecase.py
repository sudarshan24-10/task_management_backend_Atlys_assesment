from task.abstract_repository.abstract_task_repository import AbstractTaskRepository
from logger import Logger

logger = Logger().get_logger()

class DeleteTaskUseCase:
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository

    async def execute(self, task_id: str) -> bool:
        try:
            result = await self.task_repository.delete(task_id)
            return result
        except Exception as e:
            logger.error(f"Error deleting task at DeleteTaskUseCase: {e}")
            raise e

