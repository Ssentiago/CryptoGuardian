import os

from fastapi import Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from backend.api_v1.crud import user_crud as crud
from backend.api_v1.views.authorized_views.user.user_service_views import router
from backend.core import db_helper
from backend.core.config import settings
from backend.core.log_config import get_logger

logger = get_logger(__name__)

templates = Jinja2Templates(
    directory=os.path.join(settings.static_files_path, "templates")
)


@router.post("/change_password")
async def post_change_password(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
    password: str = Body(embed=True),
):
    user = request.scope.get("user")
    return await crud.change_password(user, session, password)


@router.get("/logout")
def logout(request: Request):
    response = templates.TemplateResponse("index.html", {"request": request})
    response.delete_cookie("xxx_access_token")
    response.delete_cookie("xxx_refresh_token")
    return response
