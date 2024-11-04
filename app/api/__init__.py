from fastapi import APIRouter
from app.api.auth import router as auth
from app.api.v1 import router as v1

router = APIRouter(prefix="/api")

router.include_router(auth)
router.include_router(v1)
