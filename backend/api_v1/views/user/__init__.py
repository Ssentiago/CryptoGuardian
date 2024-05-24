from fastapi import APIRouter

from .user_service_views import router as service_router
from .user_views import router as user_router

router = APIRouter()
router.include_router(service_router, prefix="/service")
router.include_router(user_router)
