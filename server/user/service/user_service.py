from typing import List
from user.abstract_repository.abstract_db_operations import AbstractUserRepository
from user.use_case.create_user_usecase import CreateUserUseCase
from user.use_case.get_user_by_id_usecase import GetUserByIdUseCase
from user.use_case.get_all_users_usecase import GetAllUsersUseCase
from user.use_case.login_usecase import LoginUserUseCase
from user.schema.user_schema import (
    UserCreateSchema, UserLoginSchema, UserResponseSchema
)
from auth.usecase.verify_password_usecase import VerifyPasswordUseCase
from auth.usecase.generate_token_usecase import GenerateTokenUseCase
from auth.usecase.hash_password_usecase import HashPasswordUseCase
from logger import Logger

logger = Logger().get_logger()

class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreateSchema) -> UserResponseSchema:
        try:
            hash_password_usecase = HashPasswordUseCase()
            create_user_usecase = CreateUserUseCase(self.user_repository, hash_password_usecase)
            created_user = await create_user_usecase.execute(user_data)
            return created_user
        except Exception as e:
            logger.error(f"Error creating user at UserService: {e}")
            raise e

    async def get_user_by_id(self, user_id: str) -> UserResponseSchema:
        try:
            get_user_usecase = GetUserByIdUseCase(self.user_repository)
            user = await get_user_usecase.execute(user_id)
            return user
        except Exception as e:
            logger.error(f"Error retrieving user by ID at UserService: {e}")
            raise e

    async def login_user(self, user_data: UserLoginSchema) -> dict:
        try:
            verify_password_usecase = VerifyPasswordUseCase()
            generate_token_usecase = GenerateTokenUseCase()
            login_user_usecase = LoginUserUseCase(
                self.user_repository,
                verify_password_usecase,
                generate_token_usecase
            )
            response = await login_user_usecase.execute(user_data)
            return response
        except Exception as e:
            logger.error(f"Error logging in user at UserService: {e}")
            raise e

    async def get_all_users(self) -> List[UserResponseSchema]:
        try:
            get_all_users_usecase = GetAllUsersUseCase(self.user_repository)
            users = await get_all_users_usecase.execute()
            return users
        except Exception as e:
            logger.error(f"Error retrieving all users at UserService: {e}")
            raise e
