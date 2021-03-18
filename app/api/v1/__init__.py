from fastapi import APIRouter
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.buckets import router as buckets_router
from app.api.v1.endpoints.blobs import router as blobs_router

router = APIRouter(prefix='/v1')

router.include_router(users_router)
router.include_router(buckets_router)
router.include_router(blobs_router)
