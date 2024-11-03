from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_404_NOT_FOUND

from app.api.auth.utils import check_role_admin
from app.core.config import logger
from app.core.token import get_current_user
from app.crud.bucket import crud_create_bucket
from app.crud.shortcuts import check_free_bucket_name, check_free_username_and_email
from app.crud.user import (
    crud_create_user,
    crud_delete_user,
    crud_get_all_users,
    crud_get_user_by_username,
    crud_update_user,
)
from app.db.mongodb import get_database
from app.models.bucket import BucketInCreate
from app.models.user import User, UserFilterParams, UserInCreate, UserInUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
async def get_all_users(
    username: str = "",
    email: str = "",
    limit: int = Query(20),
    offset: int = Query(0),
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    filters = UserFilterParams(
        username=username, email=email, limit=limit, offset=offset
    )

    users = await crud_get_all_users(db, filters)
    return users


@router.get("/{username}", response_model=User)
async def get_user(
    username: str,
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    user = await crud_get_user_by_username(db, username)

    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Username {username} not found",
        )

    return user


@router.post("/", response_model=User)
async def create_user(
    user: UserInCreate = Body(...),
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    await check_free_username_and_email(db, user.username, user.email)

    new_user = await crud_create_user(db, user)

    # create bucket to new user
    try:
        await check_free_bucket_name(db, user.username)
        bucket = BucketInCreate(
            name=user.username,
            owner_username=user.username,
        )
        await crud_create_bucket(db, bucket, current_user)
    except Exception as exc:
        logger.error(exc)

    return new_user


@router.put("/{username}", response_model=User)
async def update_user(
    username: str,
    user: UserInUpdate = Body(...),
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    await check_free_username_and_email(db, None, user.email)

    response_user = await crud_update_user(db, username, user)

    return response_user


@router.delete("/{username}")
async def delete_user(
    username: str,
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    await crud_delete_user(db, username)
