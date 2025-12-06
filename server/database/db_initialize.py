# database/db_initialize.py

from database.db_factory import DBFactory

class DatabaseInitializer:
    async def db_init(self):
        mongo = await DBFactory.create("mongo")
        return { "mongo": mongo }
