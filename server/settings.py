import os
from dotenv import load_dotenv

load_dotenv() 

class Settings:
    def __init__(self):
        self.MONGO_URI: str = os.getenv("MONGO_URI", "mongodb+srv://sudarshan2:0250@cluster0.zvvo4kp.mongodb.net/?retryWrites=true&w=majority")
        self.DB_NAME: str = os.getenv("DB_NAME", "core_db")
        self.CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
        self.JWT_SECRET: str = os.getenv("JWT_SECRET", "defaultsecret")
        self.JWT_ALGO: str = os.getenv("JWT_ALGO", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


config = Settings()
