from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import DATABASE_NAME
from app.models.bucket import BucketFilterParams, Bucket, BucketInDb, BucketInCreate
from app.models.user import User

COLLECTION = 'buckets'

aggregate_owner = {
    '$lookup': {
        'from': 'users',
        'localField': 'owner_username',
        'foreignField': 'username',
        'as': 'owner',
    },
}

aggregate_blobs = {
    '$lookup': {
        'from': 'blobs',
        'localField': 'name',
        'foreignField': 'bucket_name',
        'as': 'blobs',
    }
}

project = {
    '$project': {
        'name': 1,
        'owner': 1,
        'created_at': 1,
        'updated_at': 1,
        'size': {
            '$sum': '$blobs.size'
        },
    }
}


async def crud_get_all_buckets(db: AsyncIOMotorClient, filters: BucketFilterParams) -> List[Bucket]:
    buckets: List[Bucket] = []
    base_query = {}

    if filters.name:
        names = filters.name.replace(', ', ',').split(',')
        base_query['name'] = {'$in': names}

    bucket_docs = db[DATABASE_NAME][COLLECTION].aggregate([
        {'$match': base_query},
        {'$limit': filters.offset + filters.limit},
        {'$skip': filters.offset},
        aggregate_owner,
        aggregate_blobs,
        {'$unwind': {'path': '$owner'}},
        project
    ])

    async for row in bucket_docs:
        buckets.append(
            Bucket(**row)
        )

    return buckets


async def crud_get_bucket_by_name(db: AsyncIOMotorClient, name: str) -> Bucket:
    base_query = {'name': {'$in': [name]}}
    bucket_docs = db[DATABASE_NAME][COLLECTION].aggregate([
        {'$match': base_query},
        aggregate_owner,
        aggregate_blobs,
        {'$unwind': {'path': '$owner'}},
        project
    ])

    async for row in bucket_docs:
        return Bucket(**row)


async def crud_create_bucket(db: AsyncIOMotorClient, bucket: BucketInCreate, current_user: User) -> BucketInDb:
    data_bucket = BucketInDb(**bucket.dict())
    data_bucket.owner_username = current_user.username

    row = await db[DATABASE_NAME][COLLECTION].insert_one(data_bucket.dict())

    data_bucket.created_at = ObjectId(row.inserted_id).generation_time
    data_bucket.updated_at = ObjectId(row.inserted_id).generation_time

    return data_bucket
