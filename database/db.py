import sqlite3
import os
from cryptography.fernet import Fernet
from environs import Env

from service import check_password, db_hash, injectionValidate

env: Env = Env()
env.read_env(None)

cipher = Fernet(env('secret').encode('utf-8'))

def db_connect():
    path = os.path.join(os.path.dirname(__file__), 'db.db')
    print(path)
    db = sqlite3.connect(path)
    return db

def check_enter(login, password):
    db = db_connect()
    password = db_hash(password)

    if injectionValidate(login):
        login = db_hash(login)
        password = db.execute('''SELECT login
                            FROM user
                            WHERE login = (?) AND password = (?)''', (login, password))
        return bool(password.fetchone())


def make_new_user(login, password, secret):
    db = db_connect()
    if injectionValidate(login) and check_password(password):
        login = db_hash(login)
        password = db_hash(password)
        secret = db_hash(secret)
        db.execute('INSERT INTO user(login, password, secret, created, updated)'
                   'VALUES (?, ?, ?, DATETIME(), null)', (login, password, secret))

        db.commit()


def forgot_password(login, secret):
    db = db_connect()
    if injectionValidate(login) and injectionValidate(secret):
        login = db_hash(login)
        secret = db_hash(secret)
        check = db.execute('SELECT * '
                           'FROM user WHERE login = (?) AND secret = (?)', (login, secret))

        return bool(check.fetchall())


def check_exists_user(login):
    if injectionValidate(login):
        db = db_connect()
        login = db_hash(login)
        check = db.execute('''SELECT * FROM user WHERE login = (?)''', (login,))

        return bool(check.fetchall())


def add_new_data(user, service, login, password):
    if injectionValidate(user) and injectionValidate(service) and injectionValidate(login):
        db = db_connect()
        user = db_hash(user)
        password = cipher.encrypt(password.encode('utf-8'))
        db.execute('''INSERT INTO password(user_id, service, login, password)
                                  VALUES ((SELECT id FROM user WHERE login = (?)), (?), (?), (?))''', (user, service, login, password))

        db.commit()
        return True


def delete_data(user, service, login):
    db = db_connect()
    if injectionValidate(user) and injectionValidate(service) and injectionValidate(login):
        user = db_hash(user)

        db.execute('DELETE FROM password '
                   'WHERE user_id = (SELECT id FROM user WHERE login = (?)) '
                   'AND service = (?) AND login = (?)', (user, service, login))
        db.commit()


def get_all_data(user):
    db = db_connect()
    user = db_hash(user)
    data = db.execute('SELECT service, login, password '
                      '   FROM password '
                      'WHERE user_id = (SELECT id FROM user WHERE login = (?))', (user,))
    res = 'Your Data:\n'
    for service, login, password in data.fetchall():
        res += 'Service: ' + service + '\n'
        res += 'Login: ' + login + '\n'
        res += 'Password: ' + cipher.decrypt(password).decode() + '\n'
    return res


def change_password(user, password):
    db = db_connect()
    if injectionValidate(user) and check_password(password):
        user = db_hash(user)
        password = db_hash(password)
        db.execute('UPDATE user '
                   'SET password = (?), updated = DATETIME() WHERE login = (?) ', (password, user))
        db.commit()
        return True


