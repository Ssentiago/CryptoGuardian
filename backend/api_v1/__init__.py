from fastapi import APIRouter

from .views import api_v1_router

API = APIRouter()
API.include_router(api_v1_router)
