from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from backend.api_v1.crud import credential_crud as crud
from backend.api_v1.schemas.credential_schemas import CredentialCreate, CredentialDelete
from backend.core import db_helper
from backend.core.log_config import get_logger
from backend.utils import createResponce, raw_data_to_tuples

logger = get_logger(__name__)


router = APIRouter()


@router.post("/add")
async def create_credential(
    request: Request,
    credential_in: CredentialCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = request.scope.get("user")
    if await crud.create_credential(credential_in, user, session):
        return createResponce(Response, status_code=status.HTTP_200_OK)
    logger.warning("Не смогли создать пользовательскую запись в базе данных")
    return createResponce(Response, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/delete")
async def delete_credential(
    request: Request,
    credential_in: CredentialDelete,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = request.scope.get("user")
    if await crud.delete_credential(credential_in, user, session):
        return createResponce(Response, status_code=status.HTTP_200_OK)
    return createResponce(Response, status_code=status.HTTP_404_NOT_FOUND)


@router.get("/get_all")
async def get_all_credentials(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = request.scope.get("user")
    header = [("#", "Имя сервиса", "Логин", "Пароль")]
    raw_body = await crud.get_all_credentials(user, session)
    body = raw_data_to_tuples(raw_body)
    header.extend(body)
    return {"data": header}


@router.get("/delete_all")
async def delete_all_credentials(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = request.scope.get("user")
    return await crud.delete_all_credentials(user, session)
