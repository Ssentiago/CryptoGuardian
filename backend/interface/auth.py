import logging
import os

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from backend.api_v1.schemas.user_schemas import UserSchema
from backend.auth.auth import access
from backend.core.config import settings

router = APIRouter()

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)
logger = logging.getLogger(__name__)

print(os.path.join(settings.static_files_path, "templates"))


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("auth/auth_login.html", {"request": request})


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("auth/auth_register.html", {"request": request})


@router.get("/change_password")
async def get_change_password(request: Request, user: UserSchema = Depends(access)):
    return templates.TemplateResponse(
        "auth/auth_change_password.html", {"request": request}
    )


@router.get("/forgot")
async def get_forgot(request: Request):
    return templates.TemplateResponse(
        "auth/auth_reset_password.html", {"request": request}
    )


@router.get("/accessDenied")
async def get_access_denied(request: Request):
    return templates.TemplateResponse(
        "auth/auth_access_denied.html", {"request": request}
    )
