import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from backend.api_v1.schemas.service_schemas import PasswordSettings
from backend.api_v1.views.authorized_views.credential_views import get_all_credentials
from backend.core import db_helper
from backend.core.log_config import get_logger
from backend.utils import (
    createResponce,
    generate_csv,
    generate_password,
)

router = APIRouter()


logger = get_logger(__name__)


@router.post("/generatePassword")
async def post_generate_password(password_settings: PasswordSettings):
    password_settings_dump = password_settings.model_dump(exclude_none=True)
    return {"password": generate_password(**password_settings_dump)}


@router.get("/export")
async def get_download(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    all_data = await get_all_credentials(request, session)
    logger.info(all_data)
    if len(all_data["data"]) > 1:
        content = generate_csv(all_data["data"])
        response = Response(content=content, status_code=status.HTTP_200_OK)
        response.headers["Content-Type"] = "text/csv"
        response.headers["Content-Disposition"] = (
            f"attachment; filename=export_data_{datetime.datetime.now()}.csv"
        )

        return response
    logger.info("Нет данных для экспорта")
    return createResponce(Response, status.HTTP_404_NOT_FOUND)
