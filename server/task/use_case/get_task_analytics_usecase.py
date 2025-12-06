from typing import List, Optional
from task.abstract_repository.abstract_task_repository import AbstractTaskRepository
from task.schema.task_schema import TaskAnalyticsResponse, TaskDistributionResponse
from logger import Logger

logger = Logger().get_logger()

class GetTaskAnalyticsUseCase:
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository

    async def execute(self, user_id: Optional[str] = None) -> TaskAnalyticsResponse:
        try:
            if user_id:
                distribution = await self.task_repository.get_user_task_distribution(user_id)
                overdue_tasks = await self.task_repository.get_overdue_tasks(user_id)
                
                return TaskAnalyticsResponse(
                    total_tasks=distribution["total_tasks"],
                    tasks_by_status=distribution["tasks_by_status"],
                    tasks_by_priority=distribution["tasks_by_priority"],
                    user_distributions=[TaskDistributionResponse(
                        user_id=distribution["user_id"],
                        total_tasks=distribution["total_tasks"],
                        tasks_by_status=distribution["tasks_by_status"],
                        tasks_by_priority=distribution["tasks_by_priority"],
                        overdue_tasks=distribution["overdue_tasks"],
                        overdue_task_ids=distribution["overdue_task_ids"]
                    )]
                )
            else:
                return TaskAnalyticsResponse(
                    total_tasks=0,
                    tasks_by_status={},
                    tasks_by_priority={},
                    user_distributions=[]
                )
        except Exception as e:
            logger.error(f"Error getting task analytics at GetTaskAnalyticsUseCase: {e}")
            raise e

