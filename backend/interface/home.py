import logging
import os
from typing import Optional

from fastapi import APIRouter, Cookie, Request
from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates

from backend.core.config import settings

router = APIRouter()

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)
logger = logging.getLogger(__name__)


@router.get("/")
async def home(request: Request, token: Optional[str] = Cookie(None)):
    # if token and check_token(token):
    # return RedirectResponse(url = "/main")
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/favicon.ico")
def favicon():
    return FileResponse(settings.static_files_path + "/favicon.ico")
