from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request, Depends, Query
from logger import Logger
from task.repository.db_task_repository import DbTaskRepository
from task.service.task_service import TaskService
from task.schema.task_schema import (
    TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema,
    TaskFilterSchema, BulkUpdateSchema, TaskAnalyticsResponse
)
from task.enum.task_status_enum import TaskStatus
from task.enum.task_priority_enum import TaskPriority
from auth.middleware.authentication_middleware import AuthBearer
from datetime import datetime

logger = Logger().get_logger()

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_router.post("/create", response_model=TaskResponseSchema, status_code=201)
async def create_task(
    task_data: TaskCreateSchema,
    request: Request,
    authenticated_user = Depends(AuthBearer())
):
    try:
        logger.info("Create task API called")
        db_session = request.app.state.db
        task_repository = DbTaskRepository(db_session)
        task_service = TaskService(task_repository)
        
        created_task = await task_service.create_task(task_data, authenticated_user.id)
        return created_task
    except HTTPException as http_exc:
        logger.error(f"HTTPException in create_task route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in create_task route: {e}")
        raise HTTPException(status_code=500, detail="Task creation failed")

@task_router.get("/{task_id}", response_model=TaskResponseSchema)
async def get_task_by_id(
    task_id: str,
    request: Request,
    authenticated_user = Depends(AuthBearer())
):
    try:
        logger.info(f"Get task by ID API called for task_id: {task_id}")
        db_session = request.app.state.db
        task_repository = DbTaskRepository(db_session)
        task_service = TaskService(task_repository)
        
        task = await task_service.get_task_by_id(task_id)
        return task
    except HTTPException as http_exc:
        logger.error(f"HTTPException in get_task_by_id route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in get_task_by_id route: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve task")

@task_router.get("", response_model=List[TaskResponseSchema])
async def get_all_tasks(
    request: Request,
    authenticated_user = Depends(AuthBearer()),
    status: Optional[List[TaskStatus]] = Query(None, description="Filter by status"),
    priority: Optional[List[TaskPriority]] = Query(None, description="Filter by priority"),
    assignee_id: Optional[str] = Query(None, description="Filter by assignee ID"),
    created_by: Optional[str] = Query(None, description="Filter by creator ID"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    due_date_from: Optional[datetime] = Query(None, description="Filter tasks due from date"),
    due_date_to: Optional[datetime] = Query(None, description="Filter tasks due to date"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    filter_logic: str = Query("AND", description="AND or OR logic for multiple filters")
):
    try:
        logger.info("Get all tasks API called with filters")
        db_session = request.app.state.db
        task_repository = DbTaskRepository(db_session)
        task_service = TaskService(task_repository)
        
        filters = TaskFilterSchema(
            status=status,
            priority=priority,
            assignee_id=assignee_id,
            created_by=created_by,
            tags=tags,
            due_date_from=due_date_from,
            due_date_to=due_date_to,
            search=search,
            filter_logic=filter_logic
        )
        
        tasks = await task_service.get_all_tasks(filters)
        return tasks
    except HTTPException as http_exc:
        logger.error(f"HTTPException in get_all_tasks route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in get_all_tasks route: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tasks")

@task_router.put("/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: str,
    task_data: TaskUpdateSchema,
    request: Request,
    authenticated_user = Depends(AuthBearer())
):
    try:
        logger.info(f"Update task API called for task_id: {task_id}")
        db_session = request.app.state.db
        task_repository = DbTaskRepository(db_session)
        task_service = TaskService(task_repository)
        existing_task = await task_service.get_task_by_id(task_id)
        if existing_task.created_by != authenticated_user.id and existing_task.assignee_id != authenticated_user.id:
            raise HTTPException(status_code=403, detail="You don't have permission to update this task")
        
        updated_task = await task_service.update_task(task_id, task_data)
        return updated_task
    except HTTPException as http_exc:
        logger.error(f"HTTPException in update_task route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in update_task route: {e}")
        raise HTTPException(status_code=500, detail="Failed to update task")

@task_router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    request: Request,
    authenticated_user = Depends(AuthBearer())
):
    try:
        logger.info(f"Delete task API called for task_id: {task_id}")
        db_session = request.app.state.db
        task_repository = DbTaskRepository(db_session)
        task_service = TaskService(task_repository)
        existing_task = await task_service.get_task_by_id(task_id)
        if existing_task.created_by != authenticated_user.id:
            raise HTTPException(status_code=403, detail="Only the task creator can delete this task")
        
        await task_service.delete_task(task_id)
        return None
    except HTTPException as http_exc:
        logger.error(f"HTTPException in delete_task route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in delete_task route: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete task")

@task_router.patch("/bulk-update", response_model=List[TaskResponseSchema])
async def bulk_update_tasks(
    bulk_update_data: BulkUpdateSchema,
    request: Request,
    authenticated_user = Depends(AuthBearer())
):
    try:
        logger.info("Bulk update tasks API called")
        db_session = request.app.state.db
        task_repository = DbTaskRepository(db_session)
        task_service = TaskService(task_repository)
        
        updated_tasks = await task_service.bulk_update_tasks(bulk_update_data)
        return updated_tasks
    except HTTPException as http_exc:
        logger.error(f"HTTPException in bulk_update_tasks route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in bulk_update_tasks route: {e}")
        raise HTTPException(status_code=500, detail="Bulk update failed")

@task_router.get("/analytics/distribution", response_model=TaskAnalyticsResponse)
async def get_task_analytics(
    request: Request,
    user_id: Optional[str] = Query(None, description="Get analytics for specific user"),
    authenticated_user = Depends(AuthBearer())
):
    try:
        logger.info("Get task analytics API called")
        db_session = request.app.state.db
        task_repository = DbTaskRepository(db_session)
        task_service = TaskService(task_repository)
        target_user_id = user_id or authenticated_user.id
        
        analytics = await task_service.get_task_analytics(target_user_id)
        return analytics
    except HTTPException as http_exc:
        logger.error(f"HTTPException in get_task_analytics route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in get_task_analytics route: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve task analytics")

@task_router.get("/analytics/overdue", response_model=List[TaskResponseSchema])
async def get_overdue_tasks(
    request: Request,
    user_id: Optional[str] = Query(None, description="Get overdue tasks for specific user"),
    authenticated_user = Depends(AuthBearer())
):
    try:
        logger.info("Get overdue tasks API called")
        db_session = request.app.state.db
        task_repository = DbTaskRepository(db_session)
        target_user_id = user_id or authenticated_user.id
        
        overdue_tasks = await task_repository.get_overdue_tasks(target_user_id)
        return overdue_tasks
    except HTTPException as http_exc:
        logger.error(f"HTTPException in get_overdue_tasks route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in get_overdue_tasks route: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve overdue tasks")

