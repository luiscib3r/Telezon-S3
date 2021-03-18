import string
import random

from bson import ObjectId
from fastapi.exceptions import HTTPException
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_404_NOT_FOUND

from app.core.config import DATABASE_NAME
from app.models.user import UserFilterParams, UserInDb, UserInCreate, UserInUpdate

COLLECTION = 'users'


async def crud_get_all_users(db: AsyncIOMotorClient, filters: UserFilterParams) -> List[UserInDb]:
    users: List[UserInDb] = []
    base_query = {}

    if filters.username:
        user_names = filters.username.replace(', ', ',').split(',')
        base_query['username'] = {'$in': user_names}

    if filters.email:
        emails = filters.email.replace(', ', ',').split(',')
        base_query['email'] = {'$in': emails}

    user_docs = db[DATABASE_NAME][COLLECTION].find(
        base_query, limit=filters.limit, skip=filters.offset
    )

    async for row in user_docs:
        users.append(
            UserInDb(**row)
        )

    return users


async def crud_get_user_by_username(db: AsyncIOMotorClient, username: str) -> UserInDb:
    row = await db[DATABASE_NAME][COLLECTION].find_one({'username': username})

    if row:
        return UserInDb(**row)


async def crud_get_user_by_email(db: AsyncIOMotorClient, email: str) -> UserInDb:
    row = await db[DATABASE_NAME][COLLECTION].find_one({'email': email})

    if row:
        return UserInDb(**row)


async def crud_get_user_by_access_key_id(db: AsyncIOMotorClient, access_key_id: str) -> UserInDb:
    row = await db[DATABASE_NAME][COLLECTION].find_one({'access_key_id': access_key_id})

    if row:
        return UserInDb(**row)


async def crud_create_user(db: AsyncIOMotorClient, user: UserInCreate) -> UserInDb:
    data_user = UserInDb(**user.dict())
    data_user.change_password(user.password)

    if not data_user.access_key_id:
        data_user.access_key_id = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(16))

    if not data_user.secret_key:
        data_user.secret_key = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(16))

    row = await db[DATABASE_NAME][COLLECTION].insert_one(data_user.dict())

    data_user.created_at = ObjectId(row.inserted_id).generation_time
    data_user.updated_at = ObjectId(row.inserted_id).generation_time

    return UserInDb(**data_user.dict())


async def crud_update_user(db: AsyncIOMotorClient, username: str, user: UserInUpdate) -> UserInDb:
    simple_user = await crud_get_user_by_username(db, username)
    data_user = UserInDb(**simple_user.dict())

    if not data_user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'Username {username} not found',
        )

    data_user.email = user.email or data_user.email
    data_user.description = user.description or data_user.description
    data_user.role = user.role or data_user.role

    if user.password:
        data_user.change_password(user.password)

    updated_at = await db[DATABASE_NAME][COLLECTION] \
        .update_one({"username": data_user.username}, {'$set': data_user.dict()})

    data_user.updated_at = updated_at
    return UserInDb(**data_user.dict())


async def crud_delete_user(db: AsyncIOMotorClient, username: str):
    await db[DATABASE_NAME][COLLECTION].delete_one({'username': username})
