import logging
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.config import settings

logger = logging.getLogger(__name__)


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factor = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def get_scope_session(self):
        session = async_scoped_session(
            session_factory=self.session_factor, scopefunc=current_task
        )
        return session

    async def session_dependency(self) -> AsyncGenerator:
        session = await self.get_scope_session()
        yield session
        await session.close()

    @asynccontextmanager
    async def session_context(self):
        session = await self.get_scope_session()
        try:
            yield session
        finally:
            await session.close()


db_helper = DataBaseHelper(url=settings.Database.db_url)
logger.error(settings.Database.db_url)
