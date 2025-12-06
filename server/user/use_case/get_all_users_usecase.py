from typing import List
from user.abstract_repository.abstract_db_operations import AbstractUserRepository
from user.schema.user_schema import UserResponseSchema
from logger import Logger

logger = Logger().get_logger()

class GetAllUsersUseCase:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def execute(self) -> List[UserResponseSchema]:
        try:
            users = await self.user_repository.get_all_users()
            
            # Convert each user to UserResponseSchema
            return [
                UserResponseSchema(
                    id=str(user.id),
                    email=user.email,
                    full_name=user.full_name,
                    role=user.role,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
                for user in users
            ]
        except Exception as e:
            logger.error(f"Error retrieving all users at GetAllUsersUseCase: {e}")
            raise e


