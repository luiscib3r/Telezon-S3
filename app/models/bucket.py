from pydantic import BaseModel

from app.models.db_model import DateTimeModelMixin
from app.models.user import User


class BucketFilterParams(BaseModel):
    name: str = ''
    limit: int = 20
    offset: int = 0


class BucketBase(BaseModel):
    name: str


class BucketInDb(BucketBase, DateTimeModelMixin):
    owner_username: str = ''


class Bucket(BucketBase, DateTimeModelMixin, ):
    owner: User
    size: int = 0


class BucketInCreate(BucketBase):
    pass
