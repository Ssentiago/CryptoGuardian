import secrets

from sqlalchemy import and_

from database.models import Password, SessionLocal, Token, User
from service import db_hash, regex_login, regex_password, regex_secret


def check_enter(login, password):
    if regex_login(login):
        with SessionLocal() as session:
            password = db_hash(password)
            user = session.query(User).filter(User.login == login, User.password == password).first()
            if user:
                return createToken(user.id)
    return False


def createToken(user: int):
    with SessionLocal() as session:
        token = Token(user_id = user, value = secrets.token_hex(30))
        session.add(token)
        session.commit()
        return token.value


def check_token(token: str):
    with SessionLocal() as session:
        token = session.query(Token).filter(Token.value == token).first()
        if token:
            return True
        return False


def delete_token(token: str):
    with SessionLocal() as session:
        token = session.query(Token).filter(Token.value == token).first()
        session.delete(token)
        session.commit()
        return True


def get_user_name(token: str):
    with SessionLocal() as session:
        user = session.query(User).join(Token, and_(token == Token.value, User.id == Token.user_id)).first()
        if user:
            return user.login


def make_new_user(login, password, secret):
    if regex_login(login) and regex_password(password) and regex_secret(secret):
        with SessionLocal() as session:
            user = User(login = login, password = password, secret = secret)
            session.add(user)
            session.commit()
            return True
    else:
        return False


def forgot_password(login, secret):
    if regex_login(login) and regex_secret(secret):
        with SessionLocal() as session:
            secret = db_hash(secret)
            user = session.query(User).filter(User.login == login, User.secret == secret).first()
            if user:
                return createToken(user.id)
    else:
        return False


def check_exists_user(login):
        with SessionLocal() as session:
            check = session.query(User).filter(User.login == login).first()
            return not bool(check)



def add_new_data(user, service, login, password):
    with SessionLocal() as session:
        db_user = session.query(User).filter(User.login == user).first()
        check = session.query(Password).filter(db_user.id == Password.user_id, Password.service == service,
                                               Password.login == login).first()
        if not check:
            db_password = Password(user_id = db_user.id, service = service, login = login, password = password)
            session.add(db_password)
            session.commit()

            return True
    return False


def delete_data(user, service, login):
    with SessionLocal() as session:
        db_user = session.query(User).filter(User.login == user).first()
        del_data = session.query(Password).filter(Password.user_id == db_user.id,
                                                  Password.service == service,
                                                  Password.login == login).first()
        if del_data:
            session.delete(del_data)
            session.commit()
        return True


def get_all_data(user):
    with SessionLocal() as session:
        query = session.query(Password, User).join(Password, onclause = and_(User.login == user, User.id == Password.user_id)).all()
        data = list(map(lambda x: (x[0].service, x[0].login, x[0].password), query))
        return data


def del_all_data(user):
    with SessionLocal() as session:
        query = session.query(Password).join(User, onclause = and_(User.id == Password.user_id, User.login == user)).all()
        for obj in query:
            session.delete(obj)
        session.commit()
        return True


def change_password(token, password):
    if regex_password(password):
        with SessionLocal() as session:
            user = session.query(User).join(Token, and_(token == Token.value, User.id == Token.user_id)).first()

            password = db_hash(password)
            user.password = password
            session.commit()
            return True
    else:
        return False
