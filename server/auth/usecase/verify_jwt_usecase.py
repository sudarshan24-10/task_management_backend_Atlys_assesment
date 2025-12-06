from jose import jwt, JWTError
from settings import config

class VerifyTokenUseCase:
    def execute(self, token: str):
        try:
            payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGO])
            return payload
        except JWTError:
            return None
