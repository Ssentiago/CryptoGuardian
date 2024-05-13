# **Описание**

**CryptoGuardian**- это проект, который позволяет локально запустить у себя **CryptoGuardian** вы сможете сохранять и удалять свои пароли, генерировать новые пароли по запросу, выбирая из перечня настроек для генерации, а также просматривать список своих сохраненных данныхкопию сайта-менеджера паролей и начать с ним работу. С 

Используемый стек технологий:

* HTML 
* JavaScript
* Python 
* FastApi
* SQLite
* SQLs

# **Установка**

* git clone https://github.com/Ssentiago/CryptoGuardian
* cd CryptoGuardian
* python3 -m venv \<env name> \[OPTIONAL]
* pip install -r requirements.txt
* python3 main.py

# **Использование**

После того, как вы запустили main.py, у вас должен был открыться терминал, в котором выведется 
приглашение от сервера с адресом (приблизительно - 127.0.0.1:8000). Скопируйте этот адрес и 
вставьте в адресную строку вашего браузера, перейдите по ссылке. Перед вами появится окно входа 
на сайт,  где у вас будет возможность или зарегистрироваться, или войти. 

При регистрации учтите, что пароль сверяется на основе регулярного выражения: требования к нему 
включают, чтобы он включал в себя латинские буквы любых регистров и обязательно цифры. Вы 
можете настроить поведение в service/check\_password

Также при регистрации необходимо придумать секретное слово и использовать его в дальнейшем при восстановлении своего аккаунта (кнопка "Забыли пароль?" на экране входа). Кнопка "Забыли пароль?" переадресует вас на экран смены пароля, где вы сможете сменить свой пароль от сайта и сохранить его в базу данных.

На главном экране самого менеджера паролей у вас на выбор будут доступны следующие опции:

* Генерация пароля (включает в себя 4 опции, настраивается длина генерируемого пароля). 
* Добавление в базу данных связки "Сервис-Логин-Пароль"
* Удаление из базы данных записи по "Сервис-Логин"
* Вывод текущего состояния вашего хранилища паролей

# Описание структуры проекта
- database (папка) - содержит в себе файлы db.db (файл базы данных) и db.py (общение с базой данных)
- main.py # Точка входа в веб-приложение. Использует db.py
- README.md # Текущий файл README
- requirements.txt # Список зависимостей проекта
- service.py # Служебный модуль
- .env # Тут лежит секрет, необходимый для работы алгоритма шифрования данных. 
  Рекомендуется менять его почаще (генерация происходит с помощью класса Fernet библиотеки cryptograph)
- static # Статические файлы (JS, HTML)

# **Безопасность**

В данном проекте используются следующие меры безопасности:

* Возможные xss-инъекции предотвращаются на стороне сервера с помощью функции injectionValidate на основе регулярного выражения (пропускает только латинские буквы нижнего и верхнего регистров, а также цифры)
* SQL-инъекции предотвращаются за счёт либо хеширования, либо шифрования используемых в 
  контексте с базой данных строк
* Перед сохранением в базу данных логин и пароль от аккаунта пользователя хешируется на основе алгоритма sha256
* Пароль от сервиса, данные от которого пользователь сохраняет в базу данных, шифруется с использованием ключевого слова, находящегося в файле .env по ключу "secret"
