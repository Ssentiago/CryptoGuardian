import logging
from typing import Optional

from fastapi import APIRouter, Body, Cookie, Header
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from database.database import add_new_data, del_all_data, delete_data, get_all_data, get_user_name
from service import generate_password, join_data

router = APIRouter()
router.mount("/static", StaticFiles(directory = "./static"), name = "static")
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory = "static/templates")


@router.get('/main')
async def get_main(request: Request, token: Optional[str] = Cookie(None)):
    if token:
        user = get_user_name(token)
        return templates.TemplateResponse('main.html', {"request": request,
                                                        'user_name': user,
                                                        "count_passwords": len(get_all_data(user))})
    else:
        return templates.TemplateResponse('auth/auth_access_denied.html', {"request": request})


@router.post('/main')
async def post_main(data: Optional[dict] = Body(None), action: str = Header(None), token: Optional[str] = Cookie(None)):
    match action:
        case "GeneratePassword":
            password_length = int(data['password_length'])
            include_lows = data['include_lows']
            include_ups = data['include_ups']
            include_digs = data['include_digs']
            include_spec = data['include_spec']
            generated_password = await generate_password(password_length,
                                                         include_lows,
                                                         include_ups,
                                                         include_digs,
                                                         include_spec)
            return {'password': generated_password}
        case "AddNewData":
            user = get_user_name(token)
            service = data['serviceName']
            login = data['login']
            password = data['password']
            check = add_new_data(user, service, login, password)
            return {'added': check}
        case "DeleteData":
            user = get_user_name(token)
            service = data['serviceName']
            login = data['login']
            return {'deleted': delete_data(user, service, login)}
        case "getAllData":
            user = get_user_name(token)
            return {'data': join_data(get_all_data(user))}
        case "deleteAllData":
            user = get_user_name(token)
            return {'deleted': del_all_data(user)}
