import hashlib
import random
import re
import string
from typing import Optional

from cryptography.fernet import Fernet
from environs import Env
from starlette.responses import JSONResponse, Response


async def generate_password(length: int,
                            includeLows: bool,
                            includeUps: bool,
                            include_digs: bool, include_spec: bool) -> str:
    alphabet = ''
    if includeLows:
        alphabet += string.ascii_lowercase
    if includeUps:
        alphabet += string.ascii_uppercase
    if include_digs:
        alphabet += string.digits
    if include_spec:
        alphabet += '!@#$%&*_.-'
    return ''.join(random.choice(alphabet) for _ in range(length))


env: Env = Env()
env.read_env(None)
cipher = Fernet(env('secret').encode('utf-8'))


def regex_login(login):
    return bool(re.fullmatch(r'[0-9a-zA-Z!@#$%&*_.-]{3,}', login))


def regex_password(password):
    return bool(re.fullmatch(r'^(?=.+[A-Za-z])(?=.+[0-9])(?=\S+$)[0-9a-zA-Z!@#$%&*_.-]{8,}$', password))


def regex_secret(secret):
    return bool(re.fullmatch(r'[0-9a-zA-Zа-яА-Я!@#$%&*_.-]+', secret))


def db_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()


def createResponce(init: JSONResponse | Response, status_code, data: Optional[dict] = None,
                   cookies: Optional[dict[str, str]] = None) -> Response:
    if data:
        response = init(data)
    else:
        response = init()
    response.status_code = status_code
    if cookies:
        for key, value in cookies.items():
            response.set_cookie(key, value)
    return response

def join_data(data: dict[str, str]) -> str:
    return '\n\n'.join(f"Имя сервиса: {field[0]}\nИмя пользователя: {field[1]}\nПароль: {field[2]}" for field in data)