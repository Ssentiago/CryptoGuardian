from fastapi import APIRouter

from .user import router as user_router
from .user_service_views import router as user_service_router

router = APIRouter()
router.include_router(user_router)
router.include_router(user_service_router, prefix="/service")
