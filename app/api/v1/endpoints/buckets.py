from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_404_NOT_FOUND

from app.api.auth.utils import check_role_admin, is_admin
from app.core.token import get_current_user
from app.crud.bucket import (
    crud_create_bucket,
    crud_get_all_buckets,
    crud_get_bucket_by_name,
    crud_update_bucket,
)
from app.crud.shortcuts import check_free_bucket_name
from app.db.mongodb import get_database
from app.models.bucket import Bucket, BucketFilterParams, BucketInCreate, BucketInUpdate
from app.models.user import User

router = APIRouter(prefix="/buckets", tags=["Buckets"])


@router.get("/", response_model=List[Bucket])
async def get_all_buckets(
    name: str = "",
    owner_username: str = "",
    limit: int = Query(20),
    offset: int = Query(0),
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    if not is_admin(current_user):
        owner_username = current_user.username

    filters = BucketFilterParams(
        name=name, owner_username=owner_username, limit=limit, offset=offset
    )

    buckets = await crud_get_all_buckets(db, filters)
    return buckets


@router.get("/{name}", response_model=Bucket)
async def get_bucket(
    name: str,
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    bucket = await crud_get_bucket_by_name(db, name)

    if not bucket:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Bucket {name} not found",
        )

    return bucket


@router.post("/", response_model=BucketInCreate)
async def create_bucket(
    bucket: BucketInCreate,
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    await check_free_bucket_name(db, bucket.name)

    new_bucket = await crud_create_bucket(db, bucket, current_user)

    return new_bucket


@router.put("/{bucket_name}")
async def update_bucket(
    bucket_name: str,
    bucket: BucketInUpdate = Body(...),
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)

    response_bucket = await crud_update_bucket(db, bucket_name, bucket)

    return response_bucket
