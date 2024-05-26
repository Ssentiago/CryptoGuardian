from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api_v1.schemas.credential_schemas import CredentialCreate, CredentialDelete
from backend.api_v1.schemas.user_schemas import UserSchema
from backend.core import Credential
from backend.core.log_config import get_logger

logger = get_logger(__name__)


async def create_credential(
    credential_in: CredentialCreate,
    user: UserSchema,
    session: AsyncSession,
) -> Credential:
    credential_in.user_id = user.id
    credential = Credential(**credential_in.model_dump())
    session.add(credential)
    await session.commit()
    return credential


async def delete_credential(
    credential_in: CredentialDelete, user: UserSchema, session: AsyncSession
) -> Credential:
    credential_in.user_id = user.id
    stat = select(Credential).where(
        and_(
            credential_in.user_id == Credential.user_id,
            credential_in.service == Credential.service,
            credential_in.username == Credential.username,
        )
    )
    raw = await session.execute(stat)
    credential = raw.scalar()
    if credential:
        await session.delete(credential)
        await session.commit()
        return True
    logger.info("Нечего удалять")


async def get_all_credentials(
    user: UserSchema, session: AsyncSession
) -> list[Credential]:
    stat = select(Credential).where(Credential.user_id == user.id)
    raw = await session.execute(stat)
    res = raw.scalars().all()
    return res


async def delete_all_credentials(user: UserSchema, session: AsyncSession):
    stat = delete(Credential).where(Credential.user_id == user.id)
    raw = await session.execute(stat)
    await session.commit()
