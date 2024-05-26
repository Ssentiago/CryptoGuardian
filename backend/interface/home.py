import logging
import os

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from backend.core.config import settings

router = APIRouter()

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)
logger = logging.getLogger(__name__)


@router.get("/")
async def home(
    request: Request,
):
    user = request.scope.get("user")
    if user:

        return RedirectResponse("/main/")
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/favicon.ico")
def favicon():
    return FileResponse(settings.static_files_path + "/favicon.ico")
