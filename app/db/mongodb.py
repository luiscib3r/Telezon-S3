from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import DATABASE_URL, logger


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongodb():
    db.client = AsyncIOMotorClient(DATABASE_URL)
    logger.info("Connected to MongoDB")


async def close_mongodb_connection():
    db.client.close()
    logger.info("Disconnected from MongoDB")
