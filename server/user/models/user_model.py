# user/models/user_model.py
from beanie import Document, Indexed
from typing import Annotated
from datetime import datetime
from pydantic import EmailStr, Field
from user.enum.user_role_enum import UserRole

class User(Document):
    email: Annotated[EmailStr, Indexed(unique=True)]
    full_name: str = Field(..., min_length=3, max_length=50)
    password: str
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()
