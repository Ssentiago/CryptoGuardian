import hashlib
import random
import re
import string

from cryptography.fernet import Fernet
from environs import Env


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


def check_login(login):
    return bool(re.fullmatch(r'[0-9a-zA-Z!@#$%&*_.-]{3,}', login))


def check_password(password):
    return bool(re.fullmatch(r'^(?=.+[A-Za-z])(?=.+[0-9])(?=\S+$)[0-9a-zA-Z!@#$%&*_.-]{8,}$', password))


def check_secret(secret):
    return bool(re.fullmatch(r'[0-9a-zA-Zа-яА-Я!@#$%&*_.-]', secret))


def db_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()
