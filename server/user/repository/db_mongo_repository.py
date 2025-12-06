from bson import ObjectId
from typing import List
from user.abstract_repository.abstract_db_operations import AbstractUserRepository
from user.schema.user_schema import UserCreateSchema, UserResponseSchema
from user.models.user_model import User
from fastapi import HTTPException
from http import HTTPStatus
from pymongo import errors
from logger import Logger

logger = Logger().get_logger()

class DbUserRepository(AbstractUserRepository):
    def __init__(self, db_session):
        pass

    async def create(self, data: UserCreateSchema) -> UserResponseSchema:
        try:
            data_dict = data.model_dump()
            new_user = User(**data_dict)
            saved_user = await new_user.insert()
            logger.info(f"User created with ID: {saved_user.id}")
            return saved_user
        except errors.DuplicateKeyError as e:
            logger.error(f"Duplicate key error in DbUserRepository create method: {e}")
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="User with given email or username already exists."
            )
        except Exception as e:
            logger.error(f"Error in DbUserRepository create method: {e}")
            raise e

    async def read(self, user_id: str) -> UserResponseSchema:
        try:
            try:
                user = await User.find_one({"_id": ObjectId(user_id)})
            except Exception as e:
                user = await User.find_one({"email": user_id})
            
            if not user:
                logger.warning(f"User with ID/email {user_id} not found.")
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail="User not found."
                )
            
            logger.info(f"User with ID/email {user_id} retrieved successfully.")
            return user
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in DbUserRepository read method: {e}")
            raise e

    async def get_all_users(self) -> List[UserResponseSchema]:
        try:
            users = await User.find_all().to_list()
            logger.info(f"Retrieved {len(users)} users from the database.")
            return users
        except Exception as e:
            logger.error(f"Error in DbUserRepository get_all_users method: {e}")
            raise e

    async def update(self, query: dict, data: dict) -> dict:
        pass  # not necessary for now as per current requirements

    async def delete(self, query: dict) -> bool:
        pass  # not necessary for now as per current requirements
