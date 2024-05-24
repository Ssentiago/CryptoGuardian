import logging
import os

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from backend.api_v1.crud import user_crud as crud
from backend.api_v1.schemas.service_schemas import TokenInfo
from backend.api_v1.schemas.user_schemas import (
    UserCreate,
    UserSchema,
)
from backend.auth.auth import access, gen_token_by_login, get_token_by_recovery
from backend.core import db_helper
from backend.core.config import settings

router = APIRouter()
router.mount(
    "/static", StaticFiles(directory=settings.static_files_path), name="static"
)
logger = logging.getLogger(__name__)
templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)


@router.post("/register", response_model=UserSchema)
async def post_register(
    user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.create_user(user_in, session)


@router.post("/login", response_model=TokenInfo)
def login_into(
    token: TokenInfo = Depends(gen_token_by_login),
):
    response = Response(status_code=status.HTTP_200_OK)
    response.set_cookie(
        key="xxx_access_token",
        value=token.access_token,
        httponly=True,  # Устанавливаем флаг HttpOnly
        samesite="strict",  # Устанавливаем политику SameSite для предотвращения CSRF атак
    )
    response.set_cookie(
        key="xxx_refresh_token",
        value=token.refresh_token,
        httponly=True,  # Устанавливаем флаг HttpOnly
        samesite="strict",  # Устанавливаем политику SameSite для предотвращения CSRF атак
    )

    return response


@router.post("/forgot", response_model=TokenInfo)
async def recovery(token: TokenInfo = Depends(get_token_by_recovery)):
    response = Response(status_code=status.HTTP_200_OK)
    response.set_cookie(
        key="xxx_access_token",
        value=token.access_token,
        httponly=True,  # Устанавливаем флаг HttpOnly
        samesite="strict",  # Устанавливаем политику SameSite для предотвращения CSRF атак
    )
    response.set_cookie(
        key="xxx_refresh_token",
        value=token.refresh_token,
        httponly=True,  # Устанавливаем флаг HttpOnly
        samesite="strict",  # Устанавливаем политику SameSite для предотвращения CSRF атак
    )

    return response


@router.post("/change_password")
async def post_change_password(
    user_in: UserSchema = Depends(access),
    password: str = Body(embed=True),
    session: AsyncSession = Depends(db_helper.session_dependency),
):

    return await crud.change_password(user_in, session, password)


@router.get("/logout")
def logout(request: Request):
    response = templates.TemplateResponse("index.html", {"request": request})
    response.delete_cookie("xxx_access_token")
    response.delete_cookie("xxx_refresh_token")
    return response
