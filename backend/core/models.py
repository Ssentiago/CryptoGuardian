from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from backend.utils import cipher, db_hash


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(Base):
    username = Column(String, unique=True)
    password = Column(String)
    secret = Column(String)
    created = Column(String, default=datetime.utcnow)
    updated = Column(String)

    def __init__(self, username, password, secret):
        self.username = username
        self.password = db_hash(password)
        self.secret = db_hash(secret)


class Credential(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    service = Column(String)
    username = Column(String)
    password = Column(String)

    def __init__(self, user_id, service, username, password):
        self.password = cipher.encrypt(password.encode("utf-8"))
        self.user_id = user_id
        self.service = service
        self.username = username

    def __getattribute__(self, item):
        if item == "password":
            value = super().__getattribute__(item)
            return cipher.decrypt(value).decode("utf-8")
        else:
            return super().__getattribute__(item)


class Token(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    value = Column(String)
