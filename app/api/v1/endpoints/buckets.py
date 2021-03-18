from typing import List

from fastapi import APIRouter, Query, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_404_NOT_FOUND

from app.api.auth.utils import check_role_admin
from app.core.jwt import get_current_user
from app.db.mongodb import get_database
from app.models.bucket import Bucket, BucketFilterParams, BucketInCreate, BucketInDb
from app.models.user import User
from app.crud.bucket import crud_get_all_buckets, crud_get_bucket_by_name, crud_create_bucket
from app.crud.shortcuts import check_free_bucket_name

router = APIRouter(prefix='/buckets', tags=['Buckets'])


@router.get('/', response_model=List[Bucket])
async def get_all_buckets(
        name: str = '',
        limit: int = Query(20),
        offset: int = Query(0),
        db: AsyncIOMotorClient = Depends(get_database),
        current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    filters = BucketFilterParams(
        name=name,
        limit=limit,
        offset=offset
    )

    buckets = await crud_get_all_buckets(db, filters)
    return buckets


@router.get('/{name}', response_model=Bucket)
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
            detail=f'Bucket {name} not found',
        )

    return bucket


@router.post('/', response_model=BucketInCreate)
async def create_bucket(
        bucket: BucketInCreate,
        db: AsyncIOMotorClient = Depends(get_database),
        current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    await check_free_bucket_name(db, bucket.name)

    new_bucket = await crud_create_bucket(db, bucket, current_user)

    return new_bucket
