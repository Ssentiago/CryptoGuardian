from fastapi import APIRouter

from .authorized_views import router as authorized_router
from .non_authorized_views import router as non_authorized_router

api_v1_router = APIRouter()
api_v1_router.include_router(authorized_router, prefix="/protected")
api_v1_router.include_router(non_authorized_router)
