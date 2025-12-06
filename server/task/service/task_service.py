from typing import List, Optional
from task.abstract_repository.abstract_task_repository import AbstractTaskRepository
from task.use_case.create_task_usecase import CreateTaskUseCase
from task.use_case.get_task_by_id_usecase import GetTaskByIdUseCase
from task.use_case.get_all_tasks_usecase import GetAllTasksUseCase
from task.use_case.update_task_usecase import UpdateTaskUseCase
from task.use_case.delete_task_usecase import DeleteTaskUseCase
from task.use_case.bulk_update_tasks_usecase import BulkUpdateTasksUseCase
from task.use_case.get_task_analytics_usecase import GetTaskAnalyticsUseCase
from task.schema.task_schema import (
    TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema,
    TaskFilterSchema, BulkUpdateSchema, TaskAnalyticsResponse
)
from logger import Logger

logger = Logger().get_logger()

class TaskService:
    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository = task_repository

    async def create_task(self, task_data: TaskCreateSchema, created_by: str) -> TaskResponseSchema:
        try:
            create_task_usecase = CreateTaskUseCase(self.task_repository)
            created_task = await create_task_usecase.execute(task_data, created_by)
            return created_task
        except Exception as e:
            logger.error(f"Error creating task at TaskService: {e}")
            raise e

    async def get_task_by_id(self, task_id: str) -> TaskResponseSchema:
        try:
            get_task_usecase = GetTaskByIdUseCase(self.task_repository)
            task = await get_task_usecase.execute(task_id)
            return task
        except Exception as e:
            logger.error(f"Error retrieving task by ID at TaskService: {e}")
            raise e

    async def get_all_tasks(self, filters: Optional[TaskFilterSchema] = None) -> List[TaskResponseSchema]:
        try:
            get_all_tasks_usecase = GetAllTasksUseCase(self.task_repository)
            tasks = await get_all_tasks_usecase.execute(filters)
            return tasks
        except Exception as e:
            logger.error(f"Error retrieving all tasks at TaskService: {e}")
            raise e

    async def update_task(self, task_id: str, task_data: TaskUpdateSchema) -> TaskResponseSchema:
        try:
            update_task_usecase = UpdateTaskUseCase(self.task_repository)
            updated_task = await update_task_usecase.execute(task_id, task_data)
            return updated_task
        except Exception as e:
            logger.error(f"Error updating task at TaskService: {e}")
            raise e

    async def delete_task(self, task_id: str) -> bool:
        try:
            delete_task_usecase = DeleteTaskUseCase(self.task_repository)
            result = await delete_task_usecase.execute(task_id)
            return result
        except Exception as e:
            logger.error(f"Error deleting task at TaskService: {e}")
            raise e

    async def bulk_update_tasks(self, bulk_update_data: BulkUpdateSchema) -> List[TaskResponseSchema]:
        try:
            bulk_update_usecase = BulkUpdateTasksUseCase(self.task_repository)
            updated_tasks = await bulk_update_usecase.execute(bulk_update_data)
            return updated_tasks
        except Exception as e:
            logger.error(f"Error in bulk update at TaskService: {e}")
            raise e

    async def get_task_analytics(self, user_id: Optional[str] = None) -> TaskAnalyticsResponse:
        try:
            analytics_usecase = GetTaskAnalyticsUseCase(self.task_repository)
            analytics = await analytics_usecase.execute(user_id)
            return analytics
        except Exception as e:
            logger.error(f"Error getting task analytics at TaskService: {e}")
            raise e

