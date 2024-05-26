import os

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from backend.core.config import settings
from backend.core.log_config import get_logger

logger = get_logger(__name__)

router = APIRouter()

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)


@router.get("/")
async def home(
    request: Request,
):
    user = request.scope.get("user")
    if user:
        return RedirectResponse("/protected/main")
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/favicon.ico")
def favicon():
    return FileResponse(settings.static_files_path + "/favicon.ico")
