from abc import ABC, abstractmethod
from typing import List
from user.schema.user_schema import UserCreateSchema, UserResponseSchema

class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, data: UserCreateSchema) -> UserResponseSchema:
        pass

    @abstractmethod
    async def read(self, user_id: str) -> UserResponseSchema:
        pass

    @abstractmethod
    async def get_all_users(self) -> List[UserResponseSchema]:
        pass

    @abstractmethod
    async def update(self, query: dict, data: dict) -> dict:
        pass

    @abstractmethod
    async def delete(self, query: dict) -> bool:
        pass