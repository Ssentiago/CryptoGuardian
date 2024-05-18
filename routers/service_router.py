import datetime
import logging
from typing import Optional

from fastapi import APIRouter, Body, Cookie, Header, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from database.database import add_new_data, check_token, del_all_data, delete_data, get_all_data, get_user_name
from service import generate_csv, generate_password, createResponce

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
        return RedirectResponse(url = "/accessDenied")


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
            if add_new_data(user, service, login, password):
                return createResponce(Response, status_code = status.HTTP_200_OK)

        case "DeleteData":
            user = get_user_name(token)
            service = data['serviceName']
            login = data['login']
            if delete_data(user, service, login):
                return createResponce(Response, status_code = status.HTTP_200_OK)
        case "getAllData":
            user = get_user_name(token)
            data = [('#', 'Имя сервиса', 'Логин', 'Пароль')]
            data.extend(get_all_data(user))
            return {'data': data}
        case "deleteAllData":
            user = get_user_name(token)
            if del_all_data(user):
                return createResponce(Response, status_code = status.HTTP_200_OK)


@router.get('/export')
async def get_download(token: Optional[str] = Cookie(None)):
    if check_token(token):
        user = get_user_name(token)
        raw_content = get_all_data(user)
        if len(raw_content) > 0:
            content = generate_csv(raw_content)
            response = Response(content = content, status_code = status.HTTP_200_OK)
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=export_data_{datetime.datetime.now()}.csv'

            return response
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url = '/accessDenied')
