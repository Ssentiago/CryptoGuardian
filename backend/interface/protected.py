import logging
import os

from fastapi import APIRouter, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from backend.api_v1.views.authorized_views.credential_views import get_all_credentials
from backend.core.config import settings

router = APIRouter()

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)
logger = logging.getLogger(__name__)



@router.get("/main")
async def get_main(
    request: Request,
):
    user = request.scope.get("user")
    session: AsyncSession = request.scope.get("session")
    if user:

        all_data = await get_all_credentials(user, session)
        return templates.TemplateResponse(
            "main.html",
            {
                "request": request,
                "user_name": user.username,
                "count_passwords": len(all_data),
            },
        )
    return RedirectResponse("/auth/sessionExpired")


@router.get("/change_password")
async def get_change_password(request: Request):
    user = request.scope.get("user")
    if user:
        return templates.TemplateResponse(
            "/auth/auth_change_password.html", {"request": request}
        )
    return RedirectResponse("/auth/accessDenied")
