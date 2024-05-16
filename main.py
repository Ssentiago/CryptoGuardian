import logging

import uvicorn
from fastapi import Body, FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from database.db import *
from service import generate_password

app = FastAPI()
app.mount("/static", StaticFiles(directory = "./static"), name = "static")
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory = "static/templates")


@app.get('/')
async def home(request: Request):
    token = request.cookies.get('token')
    if token and check_token(token):
        return templates.TemplateResponse('main.html', {"request": request, 'user_name': 'GOTCHA!'})
    return templates.TemplateResponse('index.html', {"request": request})


@app.get('/login.html')
async def login(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})


@app.post('/login.html')
async def check_login(request: Request, data: dict = Body()):
    username = data['user']
    password = data['password']
    token = check_enter(username, password)
    if token:
        responce = JSONResponse({'Authentication': True})
        responce.set_cookie('token', token)
        responce.status_code = 200
        return responce
    else:
        responce = JSONResponse({'Authentication': False})
        responce.status_code = 401
        return responce


@app.get('/register.html')
async def register(request: Request):
    return templates.TemplateResponse('register.html', {"request": request})


@app.post('/register.html')
async def post_register(data: dict = Body(...)):
    username = data['user']
    password = data['password']
    secret = data['secret']
    check = False
    if not check_exists_user(username):
        if make_new_user(username, password, secret):
            responce = Response()
            responce.status_code = 200
            return responce
    responce = Response()
    responce.status_code = 401
    return responce


@app.get('/main.html')
async def get_main(request: Request):
    token = request.cookies.get('token')
    if token:
        user = get_user_name(token)
        return templates.TemplateResponse('main.html', {"request": request, 'user_name': user})


@app.post('/main.html')
async def post_main(action: dict = Body(...)):
    if action['action'] == 'GeneratePassword':
        password_length = int(action['password_length'])
        include_lows = action['include_lows']
        include_ups = action['include_ups']
        include_digs = action['include_digs']
        include_spec = action['include_spec']
        generated_password = await generate_password(password_length, include_lows, include_ups,
                                                     include_digs, include_spec)
        return {'password': generated_password}

    if action['action'] == 'AddNewData':
        token = action['token']
        user = get_user_name(token)
        service = action['serviceName']
        login = action['login']
        password = action['password']
        check = add_new_data(user, service, login, password)
        return {'added': check}

    if action['action'] == 'DeleteData':
        token = action['token']
        user = get_user_name(token)
        service = action['serviceName']
        login = action['login']
        return {'deleted': delete_data(user, service, login)}

    if action['action'] == 'getAllData':
        token = action['token']
        user = get_user_name(token)
        return {'data': get_all_data(user)}

    if action['action'] == 'delAllData':
        token = action['token']
        user = get_user_name(token)
        return {'deleted': del_all_data(user)}


@app.get('/forgot.html')
async def get_forgot(request: Request):
    return templates.TemplateResponse('forgot.html', {"request": request})


@app.post('/forgot.html')
async def post_forgot(data: dict = Body(...)):
    user = data['user']
    secret = data['secret']
    token = forgot_password(user, secret)
    if token:
        responce = Response()
        responce.set_cookie('token', token)
        responce.status_code = 200
        return responce
    responce = Response()
    responce.status_code = 401
    return responce


@app.get('/change_password.html')
async def get_change_password(request: Request):
    return templates.TemplateResponse('change_password.html', {"request": request})


@app.post('/change_password.html')
async def post_change_password(data: dict = Body(...)):
    token = data['token']
    password = data['password']
    response = Response()
    if change_password(token, password):
        response.status_code = 200
        return response
    response.status_code = 403
    return response


@app.post('/token')
def post_token(data: dict = Body(...)):
    responce = Response()
    if data.get('deleteRequest'):
        check = delete_token(data['token'])
        if check:
            responce.status_code = 200
            return responce
    token = data['token']
    userReq = data.get('nameRequest')
    if not userReq and check_token(token):
        responce.status_code = 200
        return responce
    if userReq:
        userName = get_user_name(token)
        responce = JSONResponse({'name': userName})
        responce.status_code = 200
        return responce
    responce.status_code = 403
    return responce


if __name__ == '__main__':
    uvicorn.run("main:app", host = '127.0.0.1', port = 8000, reload = True)
