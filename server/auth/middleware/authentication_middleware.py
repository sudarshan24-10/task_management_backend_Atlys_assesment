from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.usecase.verify_jwt_usecase import VerifyTokenUseCase
from user.schema.user_schema import UserResponseSchema
from user.models.user_model import User
from bson import ObjectId

class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthBearer, self).__init__(auto_error=auto_error)
        self.verify_token_usecase = VerifyTokenUseCase()

    async def __call__(self, request: Request):
        token = request.cookies.get("access_token")
        if not token:
            try:
                credentials: HTTPAuthorizationCredentials = await super().__call__(request)
                if credentials:
                    token = credentials.credentials
            except:
                pass
        
        if not token:
            raise HTTPException(status_code=403, detail="Authorization token missing")

        payload = self.verify_token_usecase.execute(token)

        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user_id = payload.get("id")
        user = await User.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponseSchema(
                id=str(user.id),
                email=user.email,
                full_name=user.full_name,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
