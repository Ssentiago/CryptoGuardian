import logging
import os

from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from backend.core.config import settings

router = APIRouter()

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)
logger = logging.getLogger(__name__)


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("/auth/auth_login.html", {"request": request})


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("/auth/auth_register.html", {"request": request})


@router.get("/forgot")
async def get_forgot(request: Request):
    return templates.TemplateResponse(
        "/auth/auth_reset_password.html", {"request": request}
    )


@router.get("/accessDenied")
async def get_access_denied(request: Request):
    return templates.TemplateResponse(
        "/auth/auth_access_denied.html", {"request": request}
    )


@router.get("/sessionExpired")
def session_expired(request: Request):
    return templates.TemplateResponse(
        "/auth/session_expired.html", {"request": request}
    )
