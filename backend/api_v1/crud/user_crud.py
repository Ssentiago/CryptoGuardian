from fastapi import Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.api_v1.schemas.user_schemas import (
    UserChangePassword,
    UserCreate,
    UserValidation,
)
from backend.core import db_helper, User
from backend.utils.utils import hash_confidential_data, validate_confinedtial_data


async def create_user(
    user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)
) -> User:
    await not_exists_user(user_in, session)
    user: User = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def not_exists_user(user_in: UserCreate, session: AsyncSession):
    stat = select(User).where(User.username == user_in.username)
    user_db = await session.execute(stat)
    if user_db.scalar():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return True


async def forgot_password(user_in: UserValidation, session: AsyncSession):
    stat = select(User).where(and_(User.username == user_in.username))
    user_db = await session.execute(stat)
    user = user_db.scalar()
    if user:
        if validate_confinedtial_data(user_in.secret, user.secret.encode("utf-8")):
            return True
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def change_password(user_in: UserChangePassword, session: AsyncSession):
    stat = select(User).where(User.username == user_in.username)
    user_db = await session.execute(stat)
    user: User = user_db.scalar()
    if user:
        user.password = hash_confidential_data(user_in.password)
        await session.refresh(user)
        await session.commit()
        return True
