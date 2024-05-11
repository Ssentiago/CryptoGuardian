import hashlib
import re
import sqlite3


def check_password(password):
    return re.fullmatch(r'^(?=.+[A-Z])(?=.+[0-9])(?=.+[a-z])(?=\S+$)[0-9a-zA-Z]{8,20}$', password)


def hash(data):
    return hashlib.sha256(data.encode()).hexdigest()


def check_enter(log, pas):
    db = sqlite3.connect('db.db')
    pas = hash(pas)
    password = db.execute('''SELECT login
                        FROM user
                        WHERE login = (?) AND login_password = (?)''', (log, pas))
    return bool(password.fetchone())


def make_new_user(log, pas):
    db = sqlite3.connect('db.db')

    pas = hash(pas)

    db.execute('INSERT INTO user(login, login_password)'
               'VALUES (?, ?)', (log, pas))

    db.commit()
    db.close()


def check_exists_user(log):
    db = sqlite3.connect('db.db')
    check = db.execute('''SELECT * FROM user WHERE login = (?)''', (log,))

    return bool(check.fetchall())


def add_new_data(user, service, login, password):
    db = sqlite3.connect('db.db')

    db.execute('''INSERT INTO password(user_id, service, login, password)
                      VALUES ((SELECT id FROM user WHERE login = (?)), (?), (?), (?))''', (user, service, login, password))

    db.commit()


def delete_data(user, service, login):
    db = sqlite3.connect('db.db')
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
        res += 'Password: ' + password + '\n'
    return res
