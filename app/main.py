from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.core.config import PROJECT_NAME
from app.db.mongodb import connect_to_mongodb, close_mongodb_connection
from app.core.errors import http_error_handler, http_422_error_handler

from app.s3 import router as s3_router
from app.api import router as api_router

app = FastAPI(title=PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler('startup', connect_to_mongodb)
app.add_event_handler('shutdown', close_mongodb_connection)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

app.include_router(s3_router)
app.include_router(api_router)
