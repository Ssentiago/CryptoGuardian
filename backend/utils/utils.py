import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from backend.core.config import settings


# TODO: jwt
# TODO: fix mobile version of site
# TODO: find most responsible way to encrypt user data
# TODO: views /main endpoint


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timdelta: timedelta | None = None,
):
    to_encode = payload.copy()

    now = datetime.now(timezone.utc)
    if expire_timdelta:
        expire = now + expire_timdelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
        jti=str(uuid.uuid4()),
    )

    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm=settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, key, algorithms=[algorithm])
    return decoded


def hash_confidential_data(data: str) -> bytes:
    salt = bcrypt.gensalt()
    data_bytes: bytes = data.encode("utf-8")
    return bcrypt.hashpw(data_bytes, salt)


def validate_confinedtial_data(data: str, hashed_data: bytes) -> bool:
    return bcrypt.checkpw(data.encode("utf-8"), hashed_data)
