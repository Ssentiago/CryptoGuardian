import asyncio
import csv
import hashlib
import io
import random
import re
import string
from typing import Any, Optional

import aiohttp
import requests
import zxcvbn
from cryptography.fernet import Fernet
from environs import Env
from starlette.responses import JSONResponse, Response

from logs.log import *

logger = logging.getLogger(__name__)


def db_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()


def sha1_hash(data):
    return hashlib.sha1(data.encode()).hexdigest()


def generate_password(length: int,
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


def get_pass_score(password: str) -> list[int, int]:
    pass_data = zxcvbn.zxcvbn(password)
    score = pass_data['score']
    match score:
        case 0:
            return 'Очень слабый пароль'
        case 1:
            return 'Слабый пароль'
        case 2:
            return 'Нормальный пароль'
        case 3:
            return 'Хороший пароль'
        case 4:
            return 'Отличный пароль'





async def get_pwned(password):
    hash = sha1_hash(password)
    head = hash[:5].upper()
    tail = hash[5:].upper()
    pwned = 0
    url = fr'https://api.pwnedpasswords.com/range/{head}'

    req = requests.get(url)
    if req.status_code == 200:
        for line in req.text.splitlines():
            line, count = line.strip().split(':')
            if tail == line:
                pwned += int(count)
        return f"Пароль был скомпроментирован {pwned} раз"


env: Env = Env()
env.read_env(None)
cipher = Fernet(env('secret').encode('utf-8'))


def regex_login(login):
    return bool(re.fullmatch(r'[0-9a-zA-Z!@#$%&*_.-]{3,}', login))


def regex_password(password):
    return bool(re.fullmatch(r'^(?=.+[A-Za-z])(?=.+[0-9])(?=\S+$)[0-9a-zA-Z!@#$%&*_.-]{8,}$', password))


def regex_secret(secret):
    return bool(re.fullmatch(r'[0-9a-zA-Zа-яА-Я!@#$%&*_.-]+', secret))


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


def generate_csv(data: list[tuple[str]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(('#', 'Имя сервиса', 'Логин', 'Пароль'))
    writer.writerows(data)

    return output.getvalue()
