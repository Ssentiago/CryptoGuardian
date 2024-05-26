from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.api_v1.schemas.user_schemas import UserLogin, UserSchema, UserValidation
from backend.core import db_helper, User as UserModel
from backend.utils.utils import validate_confinedtial_data


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
