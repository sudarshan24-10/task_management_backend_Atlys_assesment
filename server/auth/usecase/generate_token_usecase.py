from datetime import datetime, timedelta
from jose import jwt
from settings import config

class GenerateTokenUseCase:
    def execute(self, user_id: str, role: str) -> str:
        expire = datetime.now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "id": user_id,
            "role": role,
            "exp": expire
        }

        token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGO)
        return token
