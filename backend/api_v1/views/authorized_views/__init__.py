from fastapi import APIRouter

from .credential_views import router as credential_router
from .user import router as user_router

router = APIRouter()
router.include_router(credential_router, prefix="/credential", tags=["credential"])
router.include_router(user_router, prefix="/user", tags=["user"])
