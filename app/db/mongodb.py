from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

from app.core.config import (
    DATABASE_NAME,
    DATABASE_URL,
    INITIAL_ADMIN_PASSWORD,
    INITIAL_ADMIN_USER,
    logger,
)
from app.crud.bucket import crud_create_bucket
from app.crud.user import crud_create_user
from app.models.bucket import BucketInCreate
from app.models.user import User, UserInCreate


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def init_db():
    logger.info("Initializing database")
    # Set username and email as unique keys
    await db.client[DATABASE_NAME]["users"].create_index(
        [("username", ASCENDING), ("email", ASCENDING)],
        unique=True,
    )

    if INITIAL_ADMIN_USER and INITIAL_ADMIN_PASSWORD:
        # Get admin user
        admin_user = await db.client[DATABASE_NAME]["users"].find_one(
            {"username": INITIAL_ADMIN_USER}
        )

        # Create admin user if not exists
        if not admin_user:
            user = UserInCreate(
                username=INITIAL_ADMIN_USER,
                password=INITIAL_ADMIN_PASSWORD,
                email="admin@telezon.dev",
            )

            admin_user = await crud_create_user(db.client, user, admin=True)
            logger.info("Admin user created")
            logger.info("Admin user: %s", INITIAL_ADMIN_USER)
            logger.info("Your bucket is the same as your username")
            bucket = BucketInCreate(
                name=admin_user.username, owner_username=admin_user.username
            )
            await crud_create_bucket(db.client, bucket, User(**admin_user.model_dump()))


async def connect_to_mongodb():
    db.client = AsyncIOMotorClient(DATABASE_URL)
    logger.info("Connected to MongoDB")
    await init_db()


async def close_mongodb_connection():
    db.client.close()
    logger.info("Disconnected from MongoDB")
