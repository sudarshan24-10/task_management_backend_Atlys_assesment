from typing import List
from task.abstract_repository.abstract_task_repository import AbstractTaskRepository
from task.schema.task_schema import TaskResponseSchema, BulkUpdateSchema
from logger import Logger

logger = Logger().get_logger()

class BulkUpdateTasksUseCase:
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository

    async def execute(self, bulk_update_data: BulkUpdateSchema) -> List[TaskResponseSchema]:
        try:
            updated_tasks = await self.task_repository.bulk_update(
                bulk_update_data.task_ids,
                bulk_update_data.update_data
            )
            return updated_tasks
        except Exception as e:
            logger.error(f"Error in bulk update at BulkUpdateTasksUseCase: {e}")
            raise e

