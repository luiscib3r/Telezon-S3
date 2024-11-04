from typing import Optional

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic.networks import EmailStr
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.crud.bucket import crud_get_bucket_by_name
from app.crud.user import crud_get_user_by_username, crud_get_user_by_email


async def check_free_username_and_email(
    conn: AsyncIOMotorClient,
    username: Optional[str] = None,
    email: Optional[EmailStr] = None,
):
    if username:
        user_by_username = await crud_get_user_by_username(conn, username)
        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this username already exists",
            )
    if email:
        user_by_email = await crud_get_user_by_email(conn, email)
        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists",
            )


async def check_free_bucket_name(db: AsyncIOMotorClient, name: str):
    bucket = await crud_get_bucket_by_name(db, name)

    if bucket:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Bucket with this name already exists",
        )
