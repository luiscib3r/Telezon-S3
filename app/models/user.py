from typing import Optional

from pydantic import BaseModel, EmailStr

from app.core.security import verify_password, generate_salt, get_password_hash
from app.models.db_model import DateTimeModelMixin

ADMIN_ROLE = 'admin'
USER_ROLE = 'user'


class UserFilterParams(BaseModel):
    username: str = ""
    email: str = ""
    limit: int = 20
    offset: int = 0


class UserBase(BaseModel):
    username: str
    email: EmailStr
    description: Optional[str] = ''
    role: str = USER_ROLE
    access_key_id: str = ''
    secret_key: str = ''


class UserInDb(UserBase, DateTimeModelMixin):
    salt: str = ''
    hashed_password: str = ''

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class User(UserBase, DateTimeModelMixin):
    pass


class UserInLogin(BaseModel):
    username: str
    password: str


class UserInCreate(UserInLogin):
    email: EmailStr


class UserInUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    description: Optional[str] = None
    role: str = USER_ROLE
