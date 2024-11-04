from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import DATABASE_NAME
from app.models.blob import Blob, BlobFilterParams, BlobInCreate, BlobInDb

COLLECTION = "blobs"

aggregate_bucket = {
    "$lookup": {
        "from": "buckets",
        "localField": "bucket_name",
        "foreignField": "name",
        "as": "bucket",
    }
}

aggregate_owner = {
    "$lookup": {
        "from": "users",
        "localField": "bucket.owner_username",
        "foreignField": "username",
        "as": "owner",
    }
}


async def crud_get_all_blobs(
    db: AsyncIOMotorClient, filters: BlobFilterParams
) -> List[Blob]:
    blobs: List[Blob] = []
    base_query = {}

    if filters.path:
        paths = filters.path.replace(", ", ",").split(",")
        base_query["path"] = {"$in": paths}

    if filters.bucket_name:
        bucket_names = filters.bucket_name.replace(", ", ",").split(",")
        base_query["bucket_name"] = {"$in": bucket_names}

    blob_docs = db[DATABASE_NAME][COLLECTION].aggregate(
        [
            {"$match": base_query},
            {"$limit": filters.offset + filters.limit},
            {"$skip": filters.offset},
            aggregate_bucket,
            aggregate_owner,
            {"$unwind": {"path": "$bucket"}},
            {"$unwind": {"path": "$owner"}},
        ]
    )

    async for row in blob_docs:
        blobs.append(Blob(**row))

    return blobs


async def crud_create_blob(
    db: AsyncIOMotorClient, blob: BlobInCreate, bucket_name: str, update: bool = False
) -> BlobInDb:
    data_blob = BlobInDb(**blob.model_dump())
    data_blob.bucket_name = bucket_name

    if not update:
        row = await db[DATABASE_NAME][COLLECTION].insert_one(data_blob.model_dump())

        data_blob.created_at = ObjectId(row.inserted_id).generation_time
        data_blob.updated_at = ObjectId(row.inserted_id).generation_time
    else:
        updated_at = await db[DATABASE_NAME][COLLECTION].update_one(
            {"path": data_blob.path}, {"$set": data_blob.model_dump()}
        )

        data_blob.updated_at = updated_at

    return data_blob
