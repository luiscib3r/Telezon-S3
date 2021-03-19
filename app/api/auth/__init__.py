from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.status import HTTP_400_BAD_REQUEST

from app.core.jwt import create_access_token, get_current_user
from app.crud.bucket import crud_create_bucket
from app.crud.shortcuts import check_free_username_and_email, check_free_bucket_name
from app.crud.user import crud_get_user_by_username, crud_create_user
from app.db.mongodb import get_database
from app.models.bucket import BucketInCreate
from app.models.token import Token
from app.models.user import User, UserInCreate

router = APIRouter(prefix='/auth', tags=['Auth'])

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # One week


@router.post('/login', response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncIOMotorClient = Depends(get_database)
):
    user = await crud_get_user_by_username(db, form_data.username)
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )

    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/signup', response_model=User)
async def signup(
        user: UserInCreate = Body(...),
        db: AsyncIOMotorClient = Depends(get_database),
):
    await check_free_username_and_email(db, user.username, user.email)
    new_user = await crud_create_user(db, user)

    # create bucket to new user
    try:
        await check_free_bucket_name(db, user.username)
        bucket = BucketInCreate(
            name=user.username,
            owner_username=user.username,
        )
        await crud_create_bucket(db, bucket, User(**new_user.dict()))
    except:
        pass

    return new_user


@router.get('/current_user', response_model=User)
def get_current_user_info(
        current_user: User = Depends(get_current_user),
):
    return current_user
