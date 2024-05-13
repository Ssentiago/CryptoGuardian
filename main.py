import uvicorn
from fastapi import Body, FastAPI
from fastapi.responses import FileResponse

from db import *
from service import generate_password

app = FastAPI()


@app.get('/')
async def home():
    return FileResponse("pages/index.html")


@app.get('/login.html')
async def some():
    return FileResponse("pages/login.html")


@app.post('/login.html')
async def check_login(data: dict = Body()):
    username = data['user']
    password = data['password']
    if check_enter(username, password):
        return {'isValidated': True}
    else:
        return {'isValidated': False}


@app.get('/register.html')
async def register():
    return FileResponse("pages/register.html")


@app.post('/register.html')
async def post_register(data: dict = Body(...)):
    username = data['user']
    password = data['password']
    secret = data['secret']
    if not check_exists_user(username):

        if check_password(password):
            make_new_user(username, password, secret)
            return {'Created': True}
        else:
            return {'Created': False}
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
        check = add_new_data(user, service, login, password)
        print(user)
        if check:
            return {'added': True}
    elif action['action'] == 'DeleteData':
        user = action['user']
        service = action['serviceName']
        login = action['login']
        delete_data(user, service, login)
        return {'deleted': True}
    elif action['action'] == 'getAllData':
        user = action['user']
        res = get_all_data(user)
        return {'data': res}


@app.get('/forgot.html')
async def get_forgot():
    return FileResponse('pages/forgot.html')


@app.post('/forgot.html')
async def post_forgot(data: dict = Body(...)):
    user = data['user']
    secret = data['secret']
    if forgot_password(user, secret):
        return {'isValidated': True}
    else:
        return {'isValidated': False}


@app.get('/change_password.html')
async def get_change_password():
    return FileResponse('pages/change_password.html')


@app.post('/change_password.html')
async def post_change_password(data: dict = Body(...)):
    user = data['user']
    password = data['password']
    check = change_password(user, password)
    if check:
        return {'changed': True}
    else:
        return {'changed': False}


if __name__ == '__main__':
    uvicorn.run("main:app", host = '127.0.0.1', port = 8000, reload = True)
