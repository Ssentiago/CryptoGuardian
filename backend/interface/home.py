import logging
import os
from typing import Optional

from fastapi import APIRouter, Cookie, Request
from starlette.responses import FileResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from backend.core.config import settings

router = APIRouter()

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)
logger = logging.getLogger(__name__)


@router.get("/")
async def home(request: Request, xxx_access_token: Optional[str] = Cookie(None)):
    if not xxx_access_token:
        return templates.TemplateResponse("index.html", {"request": request})
    return RedirectResponse("/main/")


@router.get("/favicon.ico")
def favicon():
    return FileResponse(settings.static_files_path + "/favicon.ico")
