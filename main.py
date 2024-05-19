import logging

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from routers.api_router import router as api_router
from routers.auth_router import router as auth_router
from routers.home_router import router as home_router
from routers.service_router import router as service_router

app = FastAPI()
app.mount("/static", StaticFiles(directory = "./static"), name = "static")
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory = "static/templates")

app.include_router(home_router)
app.include_router(auth_router)
app.include_router(auth_router)
app.include_router(service_router)
app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host = '127.0.0.1', port = 8000, reload = True)
