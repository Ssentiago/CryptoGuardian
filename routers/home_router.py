import logging
from typing import Optional

from fastapi import APIRouter, Cookie, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from database.database import get_all_data, get_user_name
from database.database import check_token

router = APIRouter()
router.mount("/static", StaticFiles(directory = "./static"), name = "static")
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory = "static/templates")


@router.get('/')
async def home(request: Request, token: Optional[str] = Cookie(None)):
    if token and check_token(token):
        user = get_user_name(token)
        return templates.TemplateResponse('main.html', {"request": request, 'user_name': user, 'count_passwords': len(get_all_data(user))})
    return templates.TemplateResponse('index.html', {"request": request})


@router.get('/favicon.ico')
def favicon():
    return FileResponse("static/favicon.ico")
