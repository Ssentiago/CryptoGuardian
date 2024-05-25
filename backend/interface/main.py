import logging
import os

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from backend.api_v1.crud.credential_crud import get_all_credentials
from backend.api_v1.schemas.user_schemas import UserSchema
from backend.auth import auth
from backend.core import db_helper
from backend.core.config import settings

router = APIRouter()

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)
logger = logging.getLogger(__name__)


@router.get("/")
async def get_main(
    request: Request,
    # user: UserSchema = Depends(access),
    user: UserSchema = Depends(auth.authentication),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if isinstance(user, RedirectResponse):
        return user

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
    return RedirectResponse("/auth/accessDenied")
