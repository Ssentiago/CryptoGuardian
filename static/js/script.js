function login() {
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        username = document.getElementById('username').value
        password = document.getElementById('password').value


        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'user': username,
                'password': password
            })
        });


        const responseData = await response.json();
        const isAuthenticated = responseData.isValidated;

        if (isAuthenticated) {
            createToast('Вы успешно вошли в систему', 'Сейчас вы будете перенаправлены на главную страницу')
            setTimeout(function () {
                document.cookie = "isLogged=true; path=/";
                document.cookie = "user=" + document.getElementById('username').value + '; path=/';
                window.location.href = 'main.html'
            }, 3000)

        } else {
            createToast('Что-то пошло не так...', 'Проверьте логин и пароль', 'error');
        }


    });
};

function register() {
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const user = document.getElementById('username').value
        const password = document.getElementById('password').value
        const secret = document.getElementById('secret').value

        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'user': user,
                'password': password,
                'secret': secret
            })
        });

        const responseData = await response.json();
        const Created = responseData.Created;

        if (Created) {
            createToast('Аккаунт успешно создан', 'Сейчас вы будете перенаправлены на главную страницу')

            setTimeout(function () {
                window.location.href = '/'

            }, 5000)
        } else {
            createToast('Что-то пошло не так...', 'Возможно, пользователь уже существует или ваш ввод содержит запрещённые символы', 'error')
        }


    });

};


async function forgot() {

    form = document.getElementById('ForgotForm')

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        username = document.getElementById('username').value
        secret = document.getElementById('secret').value


        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'user': username,
                'secret': secret
            })
        });


        const responseData = await response.json();
        const isAuthenticated = responseData.isValidated;

        if (isAuthenticated) {
            createToast('Валидация прошла успешно', 'Сейчас вы будете перенаправлены на страницу смены пароля')
            setTimeout(function () {
                document.cookie = "isLogged=true; path=/";
                document.cookie = "user=" + document.getElementById('username').value + '; path=/';
                window.location.href = 'change_password.html'
            }, 2000)

        } else {
            createToast('Пользователь не найден в системе', 'Попробуйте ещё раз', 'error')
        }
    })


};

function change_pass() {

    const form = document.getElementById('ChangeForm');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Предотвращаем стандартное поведение формы

        const password1 = document.getElementById('pass1').value;
        const password2 = document.getElementById('pass2').value;

        if (password1 !== password2) {
            createToast('Пароли не совпадают', '', 'error')
        } else {
            const response = await fetch(window.location.href, {
                method: 'POST',
                headers: {"Accept": "application/json", "Content-Type": "application/json"},
                body: JSON.stringify({
                    'user': getCookie('user'),
                    'password': password1
                })
            });

            const responseData = await response.json();
            const changed = responseData.changed;

            if (changed) {
                createToast('Смена пароля произошла успешно', 'Сейчас вы будете перенаправлены на главную страницу')
                setTimeout(function () {
                    document.cookie = "isLogged=true; path=/";
                    window.location.href = 'main.html';
                }, 2000)

            } else {
                createToast('Что-то пошло не так...', 'Проверьте введённые данные', 'error')
            }
        }
    });

};


const getCookie = (name) => {
    return document.cookie.split('; ').reduce((r, v) => {
        const parts = v.split('=');
        return parts[0] === name ? decodeURIComponent(parts[1]) : r;
    }, '');
};

function delete_cookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
};


async function getGeneratedPassword() {

    const generateOutput = document.getElementById('generatedPassword');
    const p_length_field = document.getElementById('passwordLength')

    if (parseInt(p_length_field.value) > parseInt(p_length_field.max)) {
        p_length_field.value = p_length_field.max;
    }

    let p_length = p_length_field.value


    includeLows = document.getElementById('includeLows').checked;
    includeUps = document.getElementById('includeUps').checked;
    include_digs = document.getElementById('includeNumbers').checked;
    include_spec = document.getElementById('includeSpecialSymbols').checked;
    check = includeLows || includeUps || include_digs || include_spec;
    if (!check) {
        createToast('Вы не отметили ни одного чекбокса', '', 'warning')
    } else {
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'action': 'GeneratePassword',
                'password_length': p_length,
                'include_lows': includeLows,
                'include_ups': includeUps,
                'include_digs': include_digs,
                'include_spec': include_spec,
            })
        });

        const responseData = await response.json();

        const password = await responseData.password


        generateOutput.textContent = password;
    }


};

async function AddLoginPassword() {
    el1 = document.getElementById('AddServiceName')
    el2 = document.getElementById('AddLogin')
    el3 = document.getElementById('AddPassword')
    serviceName = el1.value
    login_ = el2.value;
    password = el3.value;

    if (serviceName && login_ && password) {
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'user': getCookie('user'),
                'action': 'AddNewData',
                'serviceName': serviceName,
                'login': login_,
                'password': password
            })
        });

        const responseData = await response.json();
        if (responseData.added) {
            createToast('Данные были успешно добавлены в базу')
            el1.value = ''
            el2.value = ''
            el3.value = ''
        } else {
            createToast('Что-то пошло не так...', 'Проверьте введённые данные', 'error')
        }
    } else {
        createToast('Заполните все поля ввода', '', 'warning')
    }

};

async function DeleteLoginPassword() {
    el1 = document.getElementById('DeleteServiceName')
    el2 = document.getElementById('DeleteLogin')
    serviceName = el1.value;
    login_ = el2.value;

    if (serviceName && login_) {
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'user': getCookie('user'),
                'action': 'DeleteData',
                'serviceName': serviceName,
                'login': login_,
            })
        });

        const responseData = await response.json();
        if (responseData.deleted) {
            createToast('Данные были успешно удалены из базы')
            el1.value = ''
            el2.value = ''
        }
    } else {
        createToast('Заполните все поля ввода!', '', 'warning')
    }

};

async function getAllData() {
    user = getCookie('user')

    const response = await fetch(window.location.href, {
        method: 'POST',
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
        body: JSON.stringify({
            'user': getCookie('user'),
            'action': 'getAllData',
        })
    });

    const responseData = await response.json();
    let data = responseData.data;
    data = data.replace(/\n/g, '<br>');
    element = document.getElementById('passwordListContainer');
    element.innerHTML = data;
};

function unlogin() {
    delete_cookie('user')
    document.cookie = "isLogged=false"
    window.location.href = '/'

};

function get_user() {
    elem = document.getElementById('catch_user')
    name_user = getCookie('user')
    elem.textContent = name_user
};


function confirmDelAllData() {
    Swal.fire({
        title: 'Удалить все сохранённые данные?',
        text: 'Внимание! Эта операция необратима!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Да, удалить',
        cancelButtonText: 'Отмена'
    }).then((result) => {
        if (result.isConfirmed) {
            delAllData();
        }
    });
};

async function delAllData() {

    const response = await fetch(window.location.href, {
        method: 'POST',
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
        body: JSON.stringify({
            'user': getCookie('user'),
            'action': 'delAllData',
        })
    });

    const responseData = await response.json();
    createToast('Удаление данных', 'Все ваши данные успешно удалены из базы');


};

function createToast(title, content = '', icon = 'success') {
    return Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    }).fire({
        icon: icon,
        title: title,
        text: content
    });
}