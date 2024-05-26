from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from backend.api_v1 import API
from backend.core import Base, db_helper
from backend.core.config import settings
from backend.core.log_config import get_logger
from backend.interface_routers import interface_router
from backend.jwt_authorization.authorization_middleware import AuthorizationMiddleware
from backend.jwt_authorization.generate_tokens import router as AUTH
from backend.utils.logging_middleware import log_request

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


# protected: требуют от пользователя наличие токена доступа (обязательно наличие токена refresh!)
# non-protected: не требуют от пользователя наличие токена доступа. Можно посещать без ограничений.
tags_metadata = [
    {
        "name": "credential",
        "description": "Операции с пользовательскими данными. Protected",
    },
    {"name": "user", "description": "Операции с пользователями. Protected"},
    {"name": "AUTH", "description": "Модуль аутентификации. Non-protected"},
    {"name": "default", "description": "Операции по умолчанию. Non-protected"},
]


app = FastAPI(
    lifespan=lifespan,
    title=settings.API_PROJECT_NAME,
    redoc_url=None,
    openapi_tags=tags_metadata,
)
app.mount("/static", StaticFiles(directory=settings.static_files_path), name="static")


app.include_router(API)
app.include_router(AUTH)
app.include_router(interface_router)
app.middleware("http")(log_request)

app.add_middleware(
    AuthorizationMiddleware,
)


if __name__ == "__main__":
    for route in app.routes:
        logger.info(f"{route.path} ---> {route.name})")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
