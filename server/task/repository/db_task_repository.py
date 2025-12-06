from bson import ObjectId
from typing import List, Optional, Dict
from task.abstract_repository.abstract_task_repository import AbstractTaskRepository
from task.schema.task_schema import TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema, TaskFilterSchema
from task.models.task_model import Task
from task.enum.task_status_enum import TaskStatus
from fastapi import HTTPException
from http import HTTPStatus
from logger import Logger
from datetime import datetime

logger = Logger().get_logger()

class DbTaskRepository(AbstractTaskRepository):
    def __init__(self, db_session):
        pass

    async def create(self, data: TaskCreateSchema, created_by: str) -> TaskResponseSchema:
        try:
            data_dict = data.model_dump(exclude_none=True)
            data_dict["created_by"] = created_by
            new_task = Task(**data_dict)
            saved_task = await new_task.insert()
            if saved_task.dependencies:
                for dep_id in saved_task.dependencies:
                    dep_task = await Task.find_one({"_id": ObjectId(dep_id)})
                    if dep_task and str(saved_task.id) not in dep_task.blocked_by:
                        dep_task.blocked_by.append(str(saved_task.id))
                        await dep_task.save()
            
            logger.info(f"Task created with ID: {saved_task.id}")
            return self._to_response_schema(saved_task)
        except Exception as e:
            logger.error(f"Error creating task in DbTaskRepository: {e}")
            raise e

    async def read(self, task_id: str) -> TaskResponseSchema:
        try:
            task = await Task.find_one({"_id": ObjectId(task_id)})
            if not task:
                logger.warning(f"Task with ID {task_id} not found.")
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found.")
            logger.info(f"Task with ID {task_id} retrieved successfully.")
            return self._to_response_schema(task)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error reading task in DbTaskRepository: {e}")
            raise e

    async def get_all(self, filters: Optional[TaskFilterSchema] = None) -> List[TaskResponseSchema]:
        try:
            query = {}
            
            if filters:
                filter_conditions = []
                
                # Status filter
                if filters.status:
                    if filters.filter_logic == "OR":
                        filter_conditions.append({"status": {"$in": [s.value for s in filters.status]}})
                    else:
                        query["status"] = {"$in": [s.value for s in filters.status]}
                
                # Priority filter
                if filters.priority:
                    if filters.filter_logic == "OR":
                        filter_conditions.append({"priority": {"$in": [p.value for p in filters.priority]}})
                    else:
                        query["priority"] = {"$in": [p.value for p in filters.priority]}
                
                # Assignee filter
                if filters.assignee_id:
                    query["assignee_id"] = filters.assignee_id
                
                # Created by filter
                if filters.created_by:
                    query["created_by"] = filters.created_by
                
                # Tags filter
                if filters.tags:
                    query["tags"] = {"$in": filters.tags}
                
                # Due date range filter
                if filters.due_date_from or filters.due_date_to:
                    date_query = {}
                    if filters.due_date_from:
                        date_query["$gte"] = filters.due_date_from
                    if filters.due_date_to:
                        date_query["$lte"] = filters.due_date_to
                    query["due_date"] = date_query
                
                # Search in title and description
                if filters.search:
                    search_condition = {
                        "$or": [
                            {"title": {"$regex": filters.search, "$options": "i"}},
                            {"description": {"$regex": filters.search, "$options": "i"}}
                        ]
                    }
                    if filters.filter_logic == "OR":
                        filter_conditions.append(search_condition)
                    else:
                        query["$or"] = query.get("$or", [])
                        query["$or"].extend([
                            {"title": {"$regex": filters.search, "$options": "i"}},
                            {"description": {"$regex": filters.search, "$options": "i"}}
                        ])
                
                # Apply OR logic if needed
                if filters.filter_logic == "OR" and filter_conditions:
                    if len(filter_conditions) > 1:
                        query["$or"] = filter_conditions
                    elif len(filter_conditions) == 1:
                        query.update(filter_conditions[0])
            
            tasks = await Task.find(query).to_list()
            logger.info(f"Retrieved {len(tasks)} tasks from the database.")
            return [self._to_response_schema(task) for task in tasks]
        except Exception as e:
            logger.error(f"Error getting all tasks in DbTaskRepository: {e}")
            raise e

    async def update(self, task_id: str, data: TaskUpdateSchema) -> TaskResponseSchema:
        try:
            task = await Task.find_one({"_id": ObjectId(task_id)})
            if not task:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found.")
            
            update_dict = data.model_dump(exclude_none=True)
            update_dict["updated_at"] = datetime.utcnow()
            
            # Handle dependencies - update blocked_by in dependent tasks
            if "dependencies" in update_dict:
                # Remove old dependencies
                old_dependencies = task.dependencies
                for old_dep_id in old_dependencies:
                    if old_dep_id not in update_dict["dependencies"]:
                        # Remove this task from blocked_by of old dependency
                        dep_task = await Task.find_one({"_id": ObjectId(old_dep_id)})
                        if dep_task and str(task.id) in dep_task.blocked_by:
                            dep_task.blocked_by.remove(str(task.id))
                            await dep_task.save()
                
                # Add new dependencies
                for dep_id in update_dict["dependencies"]:
                    if dep_id not in old_dependencies:
                        # Add this task to blocked_by of new dependency
                        dep_task = await Task.find_one({"_id": ObjectId(dep_id)})
                        if dep_task and str(task.id) not in dep_task.blocked_by:
                            dep_task.blocked_by.append(str(task.id))
                            await dep_task.save()
            
            for key, value in update_dict.items():
                setattr(task, key, value)
            
            task.update_timestamp()
            await task.save()
            logger.info(f"Task with ID {task_id} updated successfully.")
            return self._to_response_schema(task)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating task in DbTaskRepository: {e}")
            raise e

    async def delete(self, task_id: str) -> bool:
        try:
            task = await Task.find_one({"_id": ObjectId(task_id)})
            if not task:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found.")
            
            # Remove from dependencies of other tasks
            for dep_id in task.dependencies:
                dep_task = await Task.find_one({"_id": ObjectId(dep_id)})
                if dep_task and str(task.id) in dep_task.blocked_by:
                    dep_task.blocked_by.remove(str(task.id))
                    await dep_task.save()
            
            await task.delete()
            logger.info(f"Task with ID {task_id} deleted successfully.")
            return True
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting task in DbTaskRepository: {e}")
            raise e

    async def bulk_update(self, task_ids: List[str], update_data: TaskUpdateSchema) -> List[TaskResponseSchema]:
        try:
            updated_tasks = []
            for task_id in task_ids:
                try:
                    updated_task = await self.update(task_id, update_data)
                    updated_tasks.append(updated_task)
                except HTTPException:
                    continue  # Skip tasks that don't exist
            logger.info(f"Bulk updated {len(updated_tasks)} tasks.")
            return updated_tasks
        except Exception as e:
            logger.error(f"Error in bulk update in DbTaskRepository: {e}")
            raise e

    async def get_user_task_distribution(self, user_id: str) -> Dict:
        try:
            # Get all tasks assigned to or created by user
            tasks = await Task.find({
                "$or": [
                    {"assignee_id": user_id},
                    {"created_by": user_id},
                    {"collaborators": user_id}
                ]
            }).to_list()
            
            distribution = {
                "user_id": user_id,
                "total_tasks": len(tasks),
                "tasks_by_status": {},
                "tasks_by_priority": {},
                "overdue_tasks": 0,
                "overdue_task_ids": []
            }
            
            now = datetime.utcnow()
            for task in tasks:
                # Count by status
                status = task.status.value
                distribution["tasks_by_status"][status] = distribution["tasks_by_status"].get(status, 0) + 1
                
                # Count by priority
                priority = task.priority.value
                distribution["tasks_by_priority"][priority] = distribution["tasks_by_priority"].get(priority, 0) + 1
                
                # Check overdue
                if task.due_date and task.due_date < now and task.status != TaskStatus.COMPLETED:
                    distribution["overdue_tasks"] += 1
                    distribution["overdue_task_ids"].append(str(task.id))
            
            return distribution
        except Exception as e:
            logger.error(f"Error getting user task distribution in DbTaskRepository: {e}")
            raise e

    async def get_overdue_tasks(self, user_id: Optional[str] = None) -> List[TaskResponseSchema]:
        try:
            query = {
                "due_date": {"$lt": datetime.utcnow()},
                "status": {"$ne": TaskStatus.COMPLETED.value}
            }
            
            if user_id:
                query["$or"] = [
                    {"assignee_id": user_id},
                    {"created_by": user_id},
                    {"collaborators": user_id}
                ]
            
            tasks = await Task.find(query).to_list()
            logger.info(f"Retrieved {len(tasks)} overdue tasks.")
            return [self._to_response_schema(task) for task in tasks]
        except Exception as e:
            logger.error(f"Error getting overdue tasks in DbTaskRepository: {e}")
            raise e

    def _to_response_schema(self, task: Task) -> TaskResponseSchema:
        return TaskResponseSchema(
            id=str(task.id),
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            assignee_id=task.assignee_id,
            created_by=task.created_by,
            tags=task.tags,
            subtasks=task.subtasks,
            dependencies=task.dependencies,
            blocked_by=task.blocked_by,
            collaborators=task.collaborators,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

