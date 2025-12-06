from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from user.enum.user_role_enum import UserRole

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email", unique=True)
    full_name: str = Field(..., min_length=3, max_length=50)
    role : UserRole = Field(default=UserRole.USER, description="Role of the user")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    class Config:
        orm_mode = True

class UserCreateSchema(UserBase):
    password: str = Field(..., min_length=6, max_length=20)

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, max_length=20)
class UserResponseSchema(UserBase):
    id: str
    class Config:
        orm_mode = True
