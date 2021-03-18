from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from app.db.mongodb import get_database
from app.models.blob import BlobFilterParams, BlobInCreate
from app.s3.awssig import AWSSigV4Verifier

from app.s3.utils import aws_sig_verify
from app.crud.blob import crud_get_all_blobs, crud_create_blob
from app.crud.bucket import crud_get_bucket_by_name

from app.storage import storage

router = APIRouter(tags=['S3'])


@router.put('/{bucket_name}/{path}')
async def upload_file(
        request: Request,
        bucket_name: str,
        path: str,
        db: AsyncIOMotorClient = Depends(get_database),
):
    bucket = await crud_get_bucket_by_name(db, bucket_name)

    if not bucket:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )

    if not await aws_sig_verify(bucket, request):
        return Response(
            status_code=HTTP_403_FORBIDDEN
        )

    filters = BlobFilterParams(
        path=path,
        bucket_name=bucket_name
    )

    blobs = await crud_get_all_blobs(db, filters)

    blob: BlobInCreate
    update: bool

    if len(blobs) == 0:
        update = False
        blob = BlobInCreate(
            path=path
        )
    else:
        update = True
        blob = BlobInCreate(**blobs[0].dict())

    blob.content_type = request.headers.get('content-type', '')
    blob.size = request.headers['content-length']
    body = await request.body()
    file_id = storage.put_file(body, path)
    blob.file = file_id

    await crud_create_blob(db, blob, bucket_name, update)

    return Response('')


@router.get('/{bucket_name}/{path}')
async def download_file(
        request: Request,
        bucket_name: str,
        path: str,
        db: AsyncIOMotorClient = Depends(get_database),
):
    bucket = await crud_get_bucket_by_name(db, bucket_name)

    if not bucket:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )

    if not await aws_sig_verify(bucket, request):
        return Response(
            status_code=HTTP_403_FORBIDDEN
        )

    filters = BlobFilterParams(
        path=path,
        bucket_name=bucket_name
    )

    blobs = await crud_get_all_blobs(db, filters)

    if len(blobs) == 0:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )

    blob = blobs[0]

    result_file = storage.get_file(blob.file)

    return StreamingResponse(result_file, media_type=blob.content_type)


@router.head('{bucket_name}/{path}')
async def check_file(
        bucket_name: str,
        path: str,
        db: AsyncIOMotorClient = Depends(get_database),
):
    filters = BlobFilterParams(
        path=path,
        bucket_name=bucket_name
    )

    blobs = await crud_get_all_blobs(db, filters)

    if len(blobs) > 0:
        return Response('')
    else:
        return Response(status_code=HTTP_404_NOT_FOUND)
