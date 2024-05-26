from fastapi import HTTPException
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from backend.api_v1.schemas.service_schemas import TokenInfo
from backend.api_v1.schemas.user_schemas import UserSchema
from backend.core import db_helper, User
from backend.core.log_config import get_logger
from backend.jwt_authorization.helpers import (
    ACCESS_TOKEN_TYPE,
    create_access_token,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
)
from backend.utils.utils import decode_jwt

logger = get_logger(__name__)


async def handle_protected_path(request, call_next):
    async with db_helper.session_context() as session:
        user_by_access_token, user_by_refresh_token, new_access_token = (
            await get_user_and_token(request, session)
        )

    # если токен refresh не валиден, то редиректим на sessionExpired
    if user_by_refresh_token is None:
        redirect = RedirectResponse(url="/sessionExpired")
        response = await call_next(redirect)
        response.delete_cookie("xxx_access_token")
        response.delete_cookie("xxx_refresh_token")
        return response

    # если оба токена валидны, то пропускаем как есть
    if user_by_access_token is not None and user_by_refresh_token is not None:
        request.scope["user"] = user_by_access_token
        return await call_next(request)

    # если access не валиден, но refresh валиден, обновляем access
    if user_by_access_token is None and user_by_refresh_token is not None:
        logger.info("У пользователя истёк access_token, обновляем его")
        access_token = new_access_token.access_token
        request.scope["user"] = user_by_refresh_token
        response = await call_next(request)
        response.set_cookie("xxx_access_token", access_token)
        return response

    return await call_next(request)


async def handle_unprotected_path(request, call_next):
    async with db_helper.session_context() as session:
        user_by_access_token, user_by_refresh_token, new_access_token = (
            await get_user_and_token(request, session)
        )
    if user_by_access_token:
        request.scope["user"] = user_by_access_token
        response = await call_next(request)
        return response
    if user_by_refresh_token is not None:
        logger.info("У пользователя истёк access_token, обновляем его")
        access_token = new_access_token.access_token
        response = await call_next(request)
        response.set_cookie("xxx_access_token", access_token)
        return response
    return await call_next(request)


class AuthorizationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/protected/"):
            if (
                request.cookies.get("xxx_access_token") is None
                and request.cookies.get("xxx_refresh_token") is None
            ):
                return RedirectResponse(url="/accessDenied")
            return await handle_protected_path(request, call_next)
        return await handle_unprotected_path(request, call_next)


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)

    if current_token_type == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def get_user_and_token(request, session: AsyncSession):
    access_token = request.cookies.get("xxx_access_token")
    refresh_token = request.cookies.get("xxx_refresh_token")

    user = await get_user_from_access_token(access_token, ACCESS_TOKEN_TYPE, session)
    user_again, new_access_token = (
        await get_user_and_new_access_token_from_refresh_token(
            refresh_token,
            REFRESH_TOKEN_TYPE,
            session,
        )
    )

    return user, user_again, new_access_token


async def get_user_by_decoded_token(
    decoded_credential: dict[str, str], session: AsyncSession
) -> UserSchema | None:
    id: str | None = decoded_credential.get("sub")
    user: None | User = await session.get(User, id)
    if user:
        return UserSchema.model_validate(user)


async def get_user_from_token(
    token: str,
    session: AsyncSession,
    token_type: str,
) -> UserSchema | None:
    try:
        decoded_credential = decode_jwt(token)
    except InvalidTokenError:
        return None
    try:
        validate_token_type(decoded_credential, token_type)
    except HTTPException:
        return None
    return await get_user_by_decoded_token(decoded_credential, session)


async def get_user_from_access_token(
    xxx_access_token: str, token_type: str, session: AsyncSession
) -> UserSchema | None:
    return await get_user_from_token(xxx_access_token, session, token_type)


async def get_user_and_new_access_token_from_refresh_token(
    xxx_refresh_token: str,
    token_type: str,
    session: AsyncSession,
) -> list[UserSchema, TokenInfo] | list[None, None]:
    user: UserSchema | None = await get_user_from_token(
        xxx_refresh_token, session, token_type
    )
    if user:
        new_access_token = create_access_token(user)
        return user, TokenInfo(
            access_token=new_access_token,
        )
    return None, None
