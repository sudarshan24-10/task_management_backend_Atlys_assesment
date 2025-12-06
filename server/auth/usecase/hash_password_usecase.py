from passlib.context import CryptContext

class HashPasswordUseCase:
    def __init__(self):
        self.bcrypt_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def execute(self, password: str) -> str:
        return self.bcrypt_hash.hash(password)
