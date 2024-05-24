from fastapi import APIRouter

from .auth import router as auth_router
from .home import router as home_router
from .main import router as main_router

interface_router = APIRouter()
interface_router.include_router(home_router)
interface_router.include_router(auth_router, prefix="/auth", tags=["auth"])
interface_router.include_router(main_router, prefix="/main", tags=["main"])
