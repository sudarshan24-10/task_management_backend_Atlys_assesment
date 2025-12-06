from user.abstract_repository.abstract_db_operations import AbstractUserRepository
from user.schema.user_schema import UserCreateSchema, UserResponseSchema
from auth.usecase.hash_password_usecase import HashPasswordUseCase
from logger import Logger

logger = Logger().get_logger()

class CreateUserUseCase:
    def __init__(
        self,
        user_repository: AbstractUserRepository,
        hash_password_usecase: HashPasswordUseCase
    ):
        self.user_repository = user_repository
        self.hash_password_usecase = hash_password_usecase

    async def execute(self, user_data: UserCreateSchema) -> UserResponseSchema:
        try:
            # Hash the password
            user_data.password = self.hash_password_usecase.execute(user_data.password)

            # Save user in DB
            saved_user = await self.user_repository.create(user_data)
            
            # Convert to response schema
            return UserResponseSchema(
                id=str(saved_user.id),
                email=saved_user.email,
                full_name=saved_user.full_name,
                role=saved_user.role,
                created_at=saved_user.created_at,
                updated_at=saved_user.updated_at
            )
        except Exception as e:
            logger.error(f"Error creating user at CreateUserUseCase: {e}")
            raise e

