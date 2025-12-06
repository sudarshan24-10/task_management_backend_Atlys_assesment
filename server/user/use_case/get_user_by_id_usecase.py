from user.abstract_repository.abstract_db_operations import AbstractUserRepository
from user.schema.user_schema import UserResponseSchema
from logger import Logger

logger = Logger().get_logger()

class GetUserByIdUseCase:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> UserResponseSchema:
        try:
            saved_user = await self.user_repository.read(user_id)
            
            return UserResponseSchema(
                id=str(saved_user.id),
                email=saved_user.email,
                full_name=saved_user.full_name,
                role=saved_user.role,
                created_at=saved_user.created_at,
                updated_at=saved_user.updated_at
            )
        except Exception as e:
            logger.error(f"Error retrieving user by ID at GetUserByIdUseCase: {e}")
            raise e
