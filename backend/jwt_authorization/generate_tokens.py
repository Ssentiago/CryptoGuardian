from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from backend.api_v1.schemas.service_schemas import TokenInfo
from backend.api_v1.schemas.user_schemas import UserSchema
from backend.jwt_authorization.dependencies import (
    login_dependency,
    recovery_dependency,
)
from backend.jwt_authorization.helpers import (
    create_access_token,
    create_refresh_token,
)

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
