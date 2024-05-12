import sqlite3

from cryptography.fernet import Fernet
from environs import Env

from service import check_data, check_password, db_hash

env: Env = Env()
env.read_env(None)

cipher = Fernet(env('secret').encode('utf-8'))


def check_enter(login, password):
    db = sqlite3.connect('db.db')
    password = db_hash(password)

    if check_data(login):
        password = db.execute('''SELECT login
                            FROM user
                            WHERE login = (?) AND password = (?)''', (login, password))
        return bool(password.fetchone())


def make_new_user(login, password, secret):
    db = sqlite3.connect('db.db')
    if check_data(login) and check_password(password):
        password = db_hash(password)
        secret = db_hash(secret)
        db.execute('INSERT INTO user(login, password, secret)'
                   'VALUES (?, ?, ?)', (login, password, secret))

    db.commit()


def forgot_password(login, secret):
    db = sqlite3.connect('db.db')
    if check_data(login) and check_data(secret):
        secret = db_hash(secret)
        check = db.execute('SELECT * '
                           'FROM user WHERE login = (?) AND secret = (?)', (login, secret))

        return bool(check.fetchall())


def check_exists_user(login):
    if check_data(login):
        db = sqlite3.connect('db.db')
        check = db.execute('''SELECT * FROM user WHERE login = (?)''', (login,))

        return bool(check.fetchall())


def add_new_data(user, service, login, password):
    if check_data(user) and check_data(service) and check_data(login):
        db = sqlite3.connect('db.db')
        password = cipher.encrypt(password.encode('utf-8'))
        db.execute('''INSERT INTO password(user_id, service, login, password)
                                  VALUES ((SELECT id FROM user WHERE login = (?)), (?), (?), (?))''', (user, service, login, password))

        db.commit()
        return True


def delete_data(user, service, login):
    db = sqlite3.connect('db.db')
    if check_data(user) and check_data(service) and check_data(login):
        db.execute('DELETE FROM password '
                   'WHERE user_id = (SELECT id FROM user WHERE login = (?)) '
                   'AND service = (?) AND login = (?)', (user, service, login))
        db.commit()


def get_all_data(user):
    db = sqlite3.connect('db.db')
    data = db.execute('SELECT service, login, password '
                      '   FROM password '
                      'WHERE user_id = (SELECT id FROM user WHERE login = (?))', (user,))
    res = 'Your Data:\n'
    for service, login, password in data.fetchall():
        res += 'Service: ' + service + '\n'
        res += 'Login: ' + login + '\n'
        res += 'Password: ' + cipher.decrypt(password).decode() + '\n'
    return res

print(get_all_data('dsfsedresrsrrsdaa'))

def change_password(user, password):
    db = sqlite3.connect('db.db')
    if check_data(user) and check_password(password):
        password = db_hash(password)
        print(password)
        db.execute('UPDATE user '
                   'SET password = (?) WHERE login = (?)', (password, user))
        db.commit()
        return True

