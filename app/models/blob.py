from pydantic import BaseModel

from app.models.bucket import BucketBase
from app.models.db_model import DateTimeModelMixin
from app.models.user import User


class BlobFilterParams(BaseModel):
    path: str = ''
    bucket_name: str = ''
    limit: int = 20
    offset: int = 0


class BlobBase(BaseModel):
    path: str
    file: str = ''
    content_type: str = ''
    size: int = 0


class BlobInDb(BlobBase, DateTimeModelMixin):
    bucket_name: str = ''


class Blob(BlobBase, DateTimeModelMixin):
    bucket: BucketBase
    owner: User


class BlobInCreate(BlobBase):
    pass
