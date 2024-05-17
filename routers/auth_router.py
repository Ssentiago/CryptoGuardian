import logging
from typing import Optional

from fastapi import APIRouter, Body, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from database.database import change_password, check_enter, check_exists_user, check_token, delete_token, forgot_password, get_user_name, \
    make_new_user
from service import createResponce

router = APIRouter()
router.mount("/static", StaticFiles(directory = "./static"), name = "static")
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory = "static/templates")


@router.get('/login.html')
async def login(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})




@router.post('/login.html')
async def check_login(request: Request, data: dict = Body()):
    username = data['user']
    password = data['password']
    token = check_enter(username, password)
    if token:
        return createResponce(JSONResponse, status.HTTP_200_OK, {'Authentication': True}, {'token': token})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get('/register.html')
async def register(request: Request):
    return templates.TemplateResponse('register.html', {"request": request})


@router.post('/register.html')
async def post_register(request: Request, data: dict = Body(...)):
    if request.headers.get('Action') == "CheckExistsUser":
        user = data['user']
        if check_exists_user(user):
            return createResponce(Response, status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    elif request.headers.get('Action') == "Register":
        username = data['user']
        password = data['password']
        secret = data['secret']
        check = False
        if check_exists_user(username):
            if make_new_user(username, password, secret):
                return createResponce(Response, status.HTTP_200_OK)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post('/token')
async def post_token(data: dict = Body(...)):
    if data.get('deleteRequest'):
        check = delete_token(data['token'])
        if check:
            return createResponce(Response, status.HTTP_200_OK)
    token = data['token']
    userReq = data.get('nameRequest')
    if not userReq and check_token(token):
        return createResponce(Response, status.HTTP_200_OK)
    if userReq:
        userName = get_user_name(token)
        return createResponce(JSONResponse, status.HTTP_200_OK, {'name': userName})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get('/change_password.html')
async def get_change_password(request: Request):
    token = request.cookies.get('token')
    if token:
        return templates.TemplateResponse('change_password.html', {"request": request})
    return templates.TemplateResponse('AccessDenied.html', {"request": request})


@router.post('/change_password.html')
async def post_change_password(data: dict = Body(...)):
    token = data['token']
    password = data['password']
    if change_password(token, password):
        return createResponce(Response, status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get('/forgot.html')
async def get_forgot(request: Request):
    return templates.TemplateResponse('forgot.html', {"request": request})


@router.post('/forgot.html')
async def post_forgot(data: dict = Body(...)):
    user = data['user']
    secret = data['secret']
    token = forgot_password(user, secret)
    if token:
        return createResponce(Response, status.HTTP_200_OK, cookies = {'token': token})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
