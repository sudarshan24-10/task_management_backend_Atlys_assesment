from motor import motor_asyncio
from settings import config
from beanie import init_beanie
from user.models.user_model import User

class MongoConfig:
    def __init__(self):
        self.MONGO_URI = config.MONGO_URI
        
    async def init_db(self):
        try:
            client = motor_asyncio.AsyncIOMotorClient(self.MONGO_URI)
            await client.admin.command('ping')
            print("Connected to MongoDB successfully!")
            database = client[config.DB_NAME]
            await init_beanie(database=database, document_models=[User])
            return database
        except Exception as e:
            print(f"Error initializing MongoDB: {e}")
            raise e
    async def get_database(self):
        return await self.init_db()
        