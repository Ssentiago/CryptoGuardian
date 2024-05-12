import hashlib
import random
import re
import string


async def generate_password(length: int, include_digs: bool) -> str:
    alphabet = string.ascii_uppercase + string.ascii_lowercase
    if include_digs:
        alphabet += string.digits

    return ''.join(random.choice(alphabet) for _ in range(length))


def check_data(data):
    return re.fullmatch(r'[A-Za-z0-9]+', data)


def check_password(password):
    return bool(re.fullmatch(r'^(?=.+[A-Z])(?=.+[0-9])(?=.+[a-z])(?=\S+$)[0-9a-zA-Z]{8,}$', password))
14

def db_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()
