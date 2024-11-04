# pylint: disable=redefined-outer-name,unused-argument
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.api import router as api_router
from app.core.config import PROJECT_NAME
from app.core.errors import http_422_error_handler, http_error_handler
from app.db.mongodb import close_mongodb_connection, connect_to_mongodb
from app.s3 import router as s3_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB
    await connect_to_mongodb()
    yield
    # Disconnect from MongoDB
    await close_mongodb_connection()


app = FastAPI(title=PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

app.include_router(s3_router)
app.include_router(api_router)
