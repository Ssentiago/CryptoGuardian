import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from backend.api_v1 import API
from backend.auth.auth import router as AUTH
from backend.core import Base, db_helper
from backend.core.config import settings
from backend.interface import interface_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan, title=settings.API_PROJECT_NAME)
app.mount("/static", StaticFiles(directory=settings.static_files_path), name="static")

logger = logging.getLogger(__name__)


app.include_router(API)
app.include_router(AUTH)
app.include_router(interface_router)


@app.middleware("http")
async def log_request(request: Request, call_next):
    # Логируем информацию о запросе
    print(f"Received request:")
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Client host: {request.client.host}")
    print(f"Headers: {request.headers}")
    print(f"Query parameters: {request.query_params}")
    print(f"Path parameters: {request.path_params}")
    print(f"Query string: {request.query_params}")
    print(f"Body: {await request.body()}")

    response = await call_next(request)

    print(f"Responded with status code: {response.status_code}")

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
