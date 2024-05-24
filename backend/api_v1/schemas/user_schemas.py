import re

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from starlette import status


class UserBase(BaseModel):
    __abstract__ = True
    model_config = ConfigDict(strict=True)
    username: str = Field(pattern=r"[0-9a-zA-Z!@#$%&*_.-]{3,}")

    @field_validator("password", check_fields=False)
    @classmethod
    def validate_password(cls, value: str):
        if bool(
            re.fullmatch(
                r"^(?=.+[A-Za-z])(?=.+[0-9])(?=\S+$)[0-9a-zA-Z!@#$%&*_.-]{8,}$",
                value,
            )
        ):
            return value
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least 8 characters, one letter, and one number",
        )


class UserCreate(UserBase):
    password: str
    secret: str


class UserLogin(UserBase):
    password: str


class UserValidation(UserBase):
    secret: str


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    password: str
    secret: str
