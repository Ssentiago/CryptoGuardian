from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse

from backend.api_v1.schemas.service_schemas import TokenInfo
from backend.api_v1.schemas.user_schemas import UserSchema
from backend.auth.dependencies import (
    get_user_by_access_token,
    get_user_by_refresh_token,
    login_dependency,
    recovery_dependency,
)
from backend.auth.helpers import (
    create_access_token,
    create_refresh_token,
)
from backend.core import db_helper

bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/AUTH", tags=["AUTH"], dependencies=[Depends(bearer)])


@router.post("/generate_token_by_login")
async def gen_token_by_login(
    user: UserSchema = Depends(login_dependency),
) -> TokenInfo:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/generate_token_by_recovery")
async def get_token_by_recovery(
    user: UserSchema = Depends(recovery_dependency),
) -> TokenInfo:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def refresh(
    user: UserSchema = Depends(get_user_by_refresh_token),
):
    if isinstance(user, UserSchema):
        access_token: str = create_access_token(user)

        return TokenInfo(
            access_token=access_token,
        )
    return user


@router.get("/access")
def access(
    user: UserSchema = Depends(get_user_by_access_token),
):
    return user


# todo: блэклист для токенов


@router.get("/authentication")
async def authentication(
    request: Request,
    user_access: UserSchema | None = Depends(access),
    user_new_access_token: TokenInfo = Depends(refresh),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    # если куки не установлены, редиректим на accessDenied
    if isinstance(user_access, RedirectResponse) and isinstance(
        user_new_access_token, RedirectResponse
    ):
        return user_new_access_token

    # если refresh истёк, редиректим на sessionExpired
    if isinstance(user_new_access_token, RedirectResponse):
        return user_new_access_token

    # если access и refresh валидны и нам удалось получить пользователя, то возвращаем пользователя
    if user_access and not isinstance(user_new_access_token, RedirectResponse):
        return user_access

    # access не валиден, но refresh валиден и мы получили из него новый access
    red = RedirectResponse(url=request.url)
    red.set_cookie("xxx_access_token", user_new_access_token.access_token)
    return red
