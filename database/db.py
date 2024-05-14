from sqlalchemy import and_

from database.models import Password, SessionLocal, User
from service import check_password, db_hash, injectionValidate


def check_enter(login, password):
    if injectionValidate(login):
        with SessionLocal() as session:
            login = db_hash(login)
            password = db_hash(password)
            check = session.query(User).filter(User.login == login, User.password == password).first()
            return bool(check)
    else:
        return False


def make_new_user(login, password, secret):
    if all(map(injectionValidate, [login, secret])) and check_password(password):
        with SessionLocal() as session:
            user = User(login = login, password = password, secret = secret)
            session.add(user)
            session.commit()
            return True
    else:
        return False

def forgot_password(login, secret):
    if all(map(injectionValidate, [login, secret])):
        with SessionLocal() as session:
            login = db_hash(login)
            secret = db_hash(secret)
            check = session.query(User).filter(User.login == login, User.secret == secret).first()

            return bool(check)
    else:
        return False


def check_exists_user(login):
    if injectionValidate(login):
        with SessionLocal() as session:
            login = db_hash(login)
            check = session.query(User).filter(User.login == login).first()
            return bool(check)
    else:
        return False


def add_new_data(user, service, login, password):
    if all(map(injectionValidate, [user, service, login])):
        with SessionLocal() as session:
            user = db_hash(user)
            db_user = session.query(User).filter(User.login == user).first()
            db_password = Password(user_id = db_user.id, service = service, login = login, password = password)
            session.add(db_password)
            session.commit()

            return True
    else:
        return False


def delete_data(user, service, login):
    if all(map(injectionValidate, [user, service, login])):
        with SessionLocal() as session:
            user = db_hash(user)
            db_user = session.query(User).filter(User.login == user).first()
            del_data = session.query(Password).filter(Password.user_id == db_user.id,
                                                      Password.service == service,
                                                      Password.login == login).first()
            session.delete(del_data)
            session.commit()


def get_all_data(user):
    with SessionLocal() as session:
        user = db_hash(user)
        query = session.query(Password, User).join(Password, onclause = and_(User.login == user, User.id == Password.user_id))
        res = 'Ваши сохранённые данные:\n'
        for password, user in query:
            res += 'Имя сервиса: ' + password.service + '\n'
            res += 'Логин: ' + password.login + '\n'
            res += 'Пароль: ' + password.password + '\n'
        return res


def change_password(user, password):
    if injectionValidate(user) and check_password(password):
        with SessionLocal() as session:
            user = db_hash(user)
            password = db_hash(password)
            object = session.query(User).filter(User.login == user).first()
            object.password = password
            session.commit()
            return True
    else:
        return False
