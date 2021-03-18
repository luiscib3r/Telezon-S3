import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import DEVELOPMENT_DATABASE, DATABASE_URL, ENVIRONMENT

MONGODB_URL = ''

if ENVIRONMENT == 'production':
    MONGODB_URL = DATABASE_URL
else:
    MONGODB_URL = DEVELOPMENT_DATABASE


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongodb():
    db.client = AsyncIOMotorClient(MONGODB_URL)


async def close_mongodb_connection():
    await db.client.close()
