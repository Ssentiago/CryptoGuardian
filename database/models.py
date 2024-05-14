import os
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from service import cipher, db_hash

db_url = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'db.db')
engine = create_engine(db_url, connect_args = {'check_same_thread': False})

SessionLocal = sessionmaker(autoflush = False, bind = engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True, autoincrement = True)
    login = Column(String)
    password = Column(String)
    secret = Column(String)
    created = Column(String, default = datetime.utcnow)
    updated = Column(String)

    def __init__(self, login, password, secret):
        self.login = db_hash(login)
        self.password = db_hash(password)
        self.secret = db_hash(secret)




class Password(Base):
    __tablename__ = 'password'
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    service = Column(String)
    login = Column(String)
    password = Column(String)

    def __init__(self, user_id, service, login, password):
        self.password = cipher.encrypt(password.encode('utf-8'))
        self.user_id = user_id
        self.service = service
        self.login = login

    def __getattribute__(self, item):
        if item == 'password':
            value = super().__getattribute__(item)
            return cipher.decrypt(value).decode()
        else:
            return super().__getattribute__(item)

Base.metadata.create_all(bind = engine)
