from json import JSONDecodeError

import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from starlette.datastructures import FormData

from db import *
from service import generate_password

app = FastAPI()


async def get_body(request: Request):
    content_type = request.headers.get('Content-Type')
    if content_type is None:
        raise HTTPException(status_code = 400, detail = 'No Content-Type provided!')
    elif content_type == 'application/json':
        try:
            return await request.json()
        except JSONDecodeError:
            raise HTTPException(status_code = 400, detail = 'Invalid JSON data')
    elif (content_type == 'application/x-www-form-urlencoded' or
          content_type.startswith('multipart/form-data')):
        try:
            return await request.form()
        except Exception:
            raise HTTPException(status_code = 400, detail = 'Invalid Form data')
    else:
        raise HTTPException(status_code = 400, detail = 'Content-Type not supported!')


@app.get('/')
async def home():
    return FileResponse("pages/index.html")


@app.get('/login.html')
async def some():
    return FileResponse("pages/login.html")


@app.post('/login.html')
async def check_login(body = Depends(get_body)):
    match body:
        case FormData():
            username = body['username']
            password = body['password']
            if check_enter(username, password):
                return {'isValidated': True}


@app.get('/register.html')
async def register():
    return FileResponse("pages/register.html")


@app.post('/register.html')
async def post_register(body = Depends(get_body)):
    match body:
        case FormData():
            username = body['username']
            password = body['password']

            if not check_exists_user(username):
                if check_password(password):
                    make_new_user(username, password)
                    return {'Created': True}
            else:
                return {'Created': False}


@app.get('/main.html')
async def get_main():
    return FileResponse("pages/main.html")


@app.post('/main.html')
async def post_main(action: dict = Body(...)):
    if action['action'] == 'GeneratePassword':
        password_length = int(action['password_length'])
        include_digs = action['include_digs']
        generated_password = await generate_password(password_length, include_digs)
        return {'password': generated_password}
    if action['action'] == 'AddNewData':
        user = action['user']
        service = action['serviceName']
        login = action['login']
        password = action['password']
        add_new_data(user, service, login, password)
    elif action['action'] == 'DeleteData':
        user = action['user']
        service = action['serviceName']
        login = action['login']
        delete_data(user, service, login)
    elif action['action'] == 'getAllData':
        user = action['user']
        res = get_all_data(user)
        return {'data': res}


if __name__ == '__main__':
    uvicorn.run("main:app", host = '127.0.0.1', port = 8000, reload = True)
