from http import HTTPStatus
from fastapi import HTTPException
from user.abstract_repository.abstract_db_operations import AbstractUserRepository
from user.schema.user_schema import UserLoginSchema
from auth.usecase.verify_password_usecase import VerifyPasswordUseCase
from auth.usecase.generate_token_usecase import GenerateTokenUseCase
from logger import Logger

logger = Logger().get_logger()

class LoginUserUseCase:
    def __init__(
        self,
        user_repository: AbstractUserRepository,
        verify_password_usecase: VerifyPasswordUseCase,
        generate_token_usecase: GenerateTokenUseCase
    ):
        self.user_repository = user_repository
        self.verify_password_usecase = verify_password_usecase
        self.generate_token_usecase = generate_token_usecase

    async def execute(self, user_data: UserLoginSchema) -> dict:
        try:
            user = await self.user_repository.read(user_data.email)
            
            if not user:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail="User not found."
                )
            
            if not self.verify_password_usecase.execute(user_data.password, user.password):
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail="Invalid password."
                )
            
            user_id = str(user.id)
            user_role = user.role.value if hasattr(user.role, 'value') else str(user.role)
            access_token = self.generate_token_usecase.execute(user_id, user_role)
            
            return {"access_token": access_token}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error logging in user at LoginUserUseCase: {e}")
            raise e
