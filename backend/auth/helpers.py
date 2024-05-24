from datetime import timedelta

from backend.api_v1.schemas.user_schemas import UserSchema
from backend.core.config import settings
from backend.utils.utils import encode_jwt

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
TOKEN_TYPE_FIELD = "type"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int | None = None,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload: dict = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)

    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timdelta=expire_timedelta,
    )


def create_access_token(user: UserSchema) -> str:
    jwt_payload: dict = {"sub": user.id, "usr": user.username}

    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload: dict = {"sub": user.id}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
