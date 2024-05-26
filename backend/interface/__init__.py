from fastapi import APIRouter

from .home import router as home_router
from .non_protected import router as non_protected_router
from .protected import router as protected_router

interface_router = APIRouter()
interface_router.include_router(home_router)
interface_router.include_router(
    protected_router, prefix="/protected", tags=["protected"]
)
interface_router.include_router(non_protected_router)
