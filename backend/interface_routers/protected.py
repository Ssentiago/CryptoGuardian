import os

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from backend.api_v1.crud.credential_crud import get_all_credentials
from backend.core import db_helper
from backend.core.config import settings
from backend.core.log_config import get_logger

logger = get_logger(__name__)

router = APIRouter()

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)


@router.get("/main")
async def get_main(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = request.scope.get("user")
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
    return RedirectResponse("/sessionExpired")


@router.get("/change_password")
async def get_change_password(request: Request):
    user = request.scope.get("user")
    if user:
        return templates.TemplateResponse(
            "/auth/auth_change_password.html", {"request": request}
        )
    return RedirectResponse("/auth/accessDenied")
