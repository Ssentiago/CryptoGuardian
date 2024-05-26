from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from backend.api_v1.crud import credential_crud as crud
from backend.api_v1.schemas.credential_schemas import CredentialCreate, CredentialDelete
from backend.api_v1.schemas.user_schemas import UserSchema
from backend.auth.auth import access
from backend.core import db_helper
from backend.utils import createResponce, raw_data_to_tuples

router = APIRouter()


@router.post("/add")
async def create_credential(
    credential_in: CredentialCreate,
    user: UserSchema = Depends(access),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if await crud.create_credential(credential_in, user, session):
        return createResponce(Response, status_code=status.HTTP_200_OK)
    return createResponce(Response, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/delete")
async def delete_credential(
    credential_in: CredentialDelete,
    user: UserSchema = Depends(access),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.delete_credential(credential_in, user, session)


@router.get("/get_all")
async def get_all_credentials(
    user: UserSchema = Depends(access),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    header = [("#", "Имя сервиса", "Логин", "Пароль")]
    raw_body = await crud.get_all_credentials(user, session)
    body = raw_data_to_tuples(raw_body)
    header.extend(body)
    return {"data": header}


@router.get("/delete_all")
async def delete_all_credentials(
    user: UserSchema = Depends(access),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.delete_all_credentials(user, session)
