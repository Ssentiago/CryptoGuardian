from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse, Response

from backend.api_v1.crud import user_crud as crud
from backend.api_v1.schemas.service_schemas import TokenInfo
from backend.api_v1.schemas.user_schemas import UserCreate, UserSchema
from backend.core import db_helper
from backend.core.log_config import get_logger
from backend.jwt_authorization.generate_tokens import (
    gen_token_by_login,
    get_token_by_recovery,
)
from backend.utils import createResponce, get_pass_score, get_pwned

logger = get_logger(__name__)
router = APIRouter()


@router.post("/register", response_model=UserSchema)
async def post_register(
    user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.create_user(user_in, session)


@router.post("/login", response_model=TokenInfo)
def login_into(
    token: TokenInfo = Depends(gen_token_by_login),
):
    response = createResponce(
        JSONResponse,
        status_code=status.HTTP_200_OK,
        data={"accessToken": token.access_token},
    )
    response.set_cookie(
        key="xxx_access_token",
        value=token.access_token,
        httponly=True,  # Устанавливаем флаг HttpOnly
        samesite="strict",  # Устанавливаем политику SameSite для предотвращения CSRF атак
    )

    # Устанавливаем политику SameSite для предотвращения CSRF атак
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


@router.get("/passwordStrength/{password}")
async def password_strength(password: Optional[str]):
    if password:
        score = get_pass_score(password)
        pwned = await get_pwned(password)
        logger.info(pwned)
        logger.info(score)
        return createResponce(
            JSONResponse,
            status.HTTP_200_OK,
            {"password": password, "score": score, "pwned": pwned},
        )
    logger.warning("Не был передан пароль")
    return createResponce(Response, status.HTTP_404_NOT_FOUND)
