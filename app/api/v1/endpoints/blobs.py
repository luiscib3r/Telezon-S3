from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_404_NOT_FOUND

from app.api.auth.utils import check_role_admin
from app.core.jwt import get_current_user
from app.db.mongodb import get_database
from app.models.blob import Blob, BlobFilterParams
from app.models.user import User
from app.crud.blob import crud_get_all_blobs, crud_get_blob_by_path, crud_create_blob

router = APIRouter(prefix='/blobs', tags=['Blobs'])


@router.get('/', response_model=List[Blob])
async def get_all_blobs(
        path: str = '',
        bucket_name: str = '',
        limit: int = Query(20),
        offset: int = Query(0),
        db: AsyncIOMotorClient = Depends(get_database),
        current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    filters = BlobFilterParams(
        path=path,
        bucket_name=bucket_name,
        limit=limit,
        offset=offset
    )

    blobs = await crud_get_all_blobs(db, filters)
    return blobs


@router.get('/{path}', response_model=Blob)
async def get_blob_by_path(
        path: str,
        db: AsyncIOMotorClient = Depends(get_database),
        current_user: User = Depends(get_current_user),
):
    check_role_admin(current_user)
    blob = await crud_get_blob_by_path(db, path)

    if not blob:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f'Blob {path} not found',
        )

    return blob
