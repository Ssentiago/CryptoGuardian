import datetime
import logging
from typing import Optional

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse, Response

from backend.api_v1.schemas.service_schemas import PasswordSettings
from backend.api_v1.schemas.user_schemas import UserSchema
from backend.api_v1.views.credential_views import get_all_credentials
from backend.auth.auth import access
from backend.utils import (
    createResponce,
    generate_csv,
    generate_password,
    get_pass_score,
    get_pwned,
)

router = APIRouter()

logger = logging.getLogger(__name__)


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
    return createResponce(Response, status.HTTP_404_NOT_FOUND)


@router.post("/generatePassword")
async def post_generate_password(password_settings: PasswordSettings):
    password_settings_dump = password_settings.model_dump(exclude_none=True)
    return {"password": generate_password(**password_settings_dump)}


@router.get("/export")
async def get_download(
    user: UserSchema = Depends(access), all_data: dict = Depends(get_all_credentials)
):
    if len(all_data) > 0:
        content = generate_csv(all_data)
        response = Response(content=content, status_code=status.HTTP_200_OK)
        response.headers["Content-Type"] = "text/csv"
        response.headers["Content-Disposition"] = (
            f"attachment; filename=export_data_{datetime.datetime.now()}.csv"
        )

        return response
