# database/db_factory.py

from database.mongo_config import MongoConfig

class DBFactory:
    @staticmethod
    async def create(db_type: str):
        if db_type == "mongo":
            mongo_config = MongoConfig()
            return await mongo_config.get_database()
        else:
            raise ValueError("Unsupported DB type")
