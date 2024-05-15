import uvicorn
from fastapi import Body, FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from database.db import *
from service import generate_password
from logs.log import *
app = FastAPI()
app.mount("/static", StaticFiles(directory = "./static"), name = "static")


@app.get('/')
async def home():
    return FileResponse("static/templates/index.html")


@app.get('/login.html')
async def login():
    return FileResponse("static/templates/login.html")


@app.post('/login.html')
async def check_login(data: dict = Body()):
    username = data['user']
    password = data['password']
    return {'isValidated': check_enter(username, password)}


@app.get('/register.html')
async def register():
    return FileResponse("static/templates/register.html")


@app.post('/register.html')
async def post_register(data: dict = Body(...)):
    username = data['user']
    password = data['password']
    secret = data['secret']
    check = False
    if not check_exists_user(username):
        check = make_new_user(username, password, secret)
    return {'Created': check}


@app.get('/main.html')
async def get_main():
    return FileResponse("static/templates/main.html")


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
        user = action['user']
        service = action['serviceName']
        login = action['login']
        password = action['password']
        check = add_new_data(user, service, login, password)
        return {'added': check}

    if action['action'] == 'DeleteData':
        user = action['user']
        service = action['serviceName']
        login = action['login']
        return {'deleted': delete_data(user, service, login)}

    if action['action'] == 'getAllData':
        user = action['user']
        return {'data': get_all_data(user)}

    if action['action'] == 'delAllData':
        user = action['user']
        return {'deleted': del_all_data(user)}


@app.get('/forgot.html')
async def get_forgot():
    return FileResponse("static/templates/forgot.html")


@app.post('/forgot.html')
async def post_forgot(data: dict = Body(...)):
    user = data['user']
    secret = data['secret']
    return {'isValidated': forgot_password(user, secret)}


@app.get('/change_password.html')
async def get_change_password():
    return FileResponse("static/templates/change_password.html")


@app.post('/change_password.html')
async def post_change_password(data: dict = Body(...)):
    user = data['user']
    password = data['password']
    return {'changed': change_password(user, password)}


if __name__ == '__main__':
    uvicorn.run("main:app", host = '0.0.0.0', port = 8000, reload = True)
