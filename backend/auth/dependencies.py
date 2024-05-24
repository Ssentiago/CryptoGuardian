from fastapi import Cookie, Depends, HTTPException
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from backend.api_v1.schemas.user_schemas import UserLogin, UserSchema, UserValidation
from backend.auth.helpers import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from backend.core import db_helper, User as UserModel
from backend.utils.utils import decode_jwt, validate_confinedtial_data


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/generate_token")


async def login_dependency(
    user_in: UserLogin,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserSchema:
    stat = select(UserModel).where(UserModel.username == user_in.username)
    sess_obj = await session.execute(stat)
    user_db: UserModel | None = sess_obj.scalar()
    if user_db:
        if validate_confinedtial_data(
            user_in.password, user_db.password.encode("utf-8")
        ):
            return UserSchema.model_validate(user_db)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def recovery_dependency(
    user_in: UserValidation,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserSchema:
    stat = select(UserModel).where(UserModel.username == user_in.username)
    sess_obj = await session.execute(stat)
    user_db: UserModel | None = sess_obj.scalar()
    if user_db:
        if validate_confinedtial_data(user_in.secret, user_db.secret.encode("utf-8")):
            return UserSchema.model_validate(user_db)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)

    if current_token_type == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def get_user_by_access_token(
    xxx_access_token: str = Cookie(...),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    try:
        decoded_credential = decode_jwt(xxx_access_token)
    except InvalidTokenError as e:
        return RedirectResponse(url="/auth/accessDenied")

    validate_token_type(decoded_credential, ACCESS_TOKEN_TYPE)
    id: str | None = decoded_credential.get("sub")
    user: None | UserModel = await session.get(UserModel, id)
    if user:
        return UserSchema.model_validate(user)
    return RedirectResponse(url="/auth/accessDenied")


async def get_user_by_refresh_token(
    xxx_refresh_token: str = Cookie(...),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    try:
        decoded_credential = decode_jwt(xxx_refresh_token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    validate_token_type(decoded_credential, REFRESH_TOKEN_TYPE)
    id: str | None = decoded_credential.get("sub")
    user: None | UserModel = await session.get(UserModel, id)
    if user:
        return UserSchema.model_validate(user)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
