import string
import random


async def generate_password(length: int, include_digs: bool) -> str:
    alphabet = string.ascii_uppercase + string.ascii_lowercase
    if include_digs:
        alphabet += string.digits

    return ''.join(random.choice(alphabet) for _ in range(length))