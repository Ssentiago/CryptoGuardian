import logging
import os

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from backend.api_v1.schemas.user_schemas import UserSchema
from backend.api_v1.views.credential_views import get_all_credentials
from backend.auth.auth import access
from backend.core.config import settings

router = APIRouter()

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)
logger = logging.getLogger(__name__)


@router.get("/")
async def get_main(
    request: Request,
    user: UserSchema = Depends(access),
    all_data: dict = Depends(get_all_credentials),
):
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "user_name": user.username,
            "count_passwords": len(all_data["data"]) - 1,
        },
    )
