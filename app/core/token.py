from datetime import UTC, datetime, timedelta
from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.core.config import SECRET_KEY
from app.crud.user import crud_get_user_by_username
from app.db.mongodb import get_database
from app.models.token import TokenPayload
from app.models.user import User

JWT_TOKEN_PREFIX = "Bearer"
ALGORITHM = "HS256"
access_token_jwt_subject = "access"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def _get_current_user(token: str) -> User:
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError as exc:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        ) from exc
    db = await get_database()
    db_user = await crud_get_user_by_username(db, token_data.username)
    if not db_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    user = User(**db_user.model_dump(), token=token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return await _get_current_user(token)


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt
