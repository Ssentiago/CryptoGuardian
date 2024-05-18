function authenticateUser() {
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        let username = document.getElementById('username').value
        let password = document.getElementById('password').value


        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'user': username,
                'password': password
            })
        });


        if (response.status === 200) {
            displayToast('Вы успешно вошли в систему', 'Сейчас вы будете перенаправлены на страницу входа')
            setTimeout(function () {
                window.location.href = '/main'
            }, 3000)
        } else {
            displayToast('Что-то пошло не так...', 'Проверьте логин и пароль', 'error');

        }


    });
};

function createAccount() {
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const user = document.getElementById('username').value
        const password = document.getElementById('password').value
        const secret = document.getElementById('secret').value

        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "Register"},
            body: JSON.stringify({
                'user': user,
                'password': password,
                'secret': secret
            })
        });


        if (response.status === 200) {
            displayToast('Аккаунт успешно создан', 'Сейчас вы будете перенаправлены на главную страницу')

            setTimeout(function () {
                window.location.href = '/'

            }, 5000)
        } else {
            displayToast('Что-то пошло не так...', 'Возможно, пользователь уже существует или ваш ввод содержит запрещённые символы', 'error')
        }


    });

};


async function validateUserForPasswordReset() {

    let form = document.getElementById('forgotForm')

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        let username = document.getElementById('username').value
        let secret = document.getElementById('secret').value


        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'user': username,
                'secret': secret
            })
        });


        if (response.status === 200) {
            displayToast('Валидация прошла успешно', 'Сейчас вы будете перенаправлены на страницу смены пароля')
            setTimeout(function () {

                window.location.href = '/change_password'
            }, 2000)

        } else {
            displayToast('Пользователь не найден в системе', 'Попробуйте ещё раз', 'error')
        }
    });


};


function changePassword() {

    const form = document.getElementById('ChangeForm');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Предотвращаем стандартное поведение формы

        const password1 = document.getElementById('pass1').value;
        const password2 = document.getElementById('pass2').value;

        if (password1 !== password2) {
            displayToast('Пароли не совпадают', '', 'error')
        } else {


            const response = await fetch(window.location.href, {
                method: 'POST',
                headers: {"Accept": "application/json", "Content-Type": "application/json"},
                body: JSON.stringify({
                    'token': getCookieValue('token'),
                    'password': password1
                })
            });

            if (response.status === 200) {
                displayToast('Смена пароля произошла успешно', 'Сейчас вы будете перенаправлены на главную страницу')
                setTimeout(function () {
                    window.location.href = '/main';
                }, 2000)

            } else {
                displayToast('Ваш пароль содержит некорректные данные', '', 'error')
            }
        }
    });

};

function logout() {
    displayToast('До встречи!', '', '')
    setTimeout(async function () {

        const response = await fetch('/token', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'token': getCookieValue('token'),
                'deleteRequest': true
            })
        });
        deleteCookie('token')
        deleteCookie('AuthenticationData')
        window.location.href = '/'
    }, 2000);


};


async function generatePassword() {
    const generateOutput = document.getElementById('generatedPassword');
    const p_length_field = document.getElementById('passwordLength')

    if (parseInt(p_length_field.value) > parseInt(p_length_field.max)) {
        p_length_field.value = p_length_field.max;
    }

    let p_length = p_length_field.value


    let includeLows = document.getElementById('includeLows').checked;
    let includeUps = document.getElementById('includeUps').checked;
    let include_digs = document.getElementById('includeNumbers').checked;
    let include_spec = document.getElementById('includeSpecialSymbols').checked;
    let check = includeLows || includeUps || include_digs || include_spec;
    if (!check) {
        displayToast('Вы не отметили ни одного чекбокса', '', 'warning')
    } else {
        const response = await fetch('/main', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "GeneratePassword"},
            body: JSON.stringify({
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


function displayToast(title, content = '', icon = 'success') {
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
};


function getCookieValue(name) {
    return document.cookie.split('; ').reduce((r, v) => {
        const parts = v.split('=');
        return parts[0] === name ? decodeURIComponent(parts[1]) : r;
    }, '')
};


function deleteCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
};


async function addLoginCredentials() {
    let el1 = document.getElementById('AddServiceName')
    let el2 = document.getElementById('AddLogin')
    let el3 = document.getElementById('AddPassword')
    let serviceName = el1.value
    let login_ = el2.value;
    let password = el3.value;

    if (serviceName && login_ && password) {
        const response = await fetch('/main', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "AddNewData"},
            body: JSON.stringify({
                'serviceName': serviceName,
                'login': login_,
                'password': password
            })
        });

        const responseData = await response.json();
        if (responseData.added) {
            displayToast('Данные были успешно добавлены в базу')
            el1.value = ''
            el2.value = ''
            el3.value = ''
        } else {
            displayToast('Что-то пошло не так...', 'Проверьте введённые данные', 'error')
        }
    } else {
        displayToast('Заполните все поля ввода', '', 'warning')
    }

};

async function deleteLoginCredentials() {
    let el1 = document.getElementById('DeleteServiceName')
    let el2 = document.getElementById('DeleteLogin')
    let serviceName = el1.value;
    let login_ = el2.value;

    if (serviceName && login_) {
        const response = await fetch('/main', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "DeleteData"},
            body: JSON.stringify({
                'serviceName': serviceName,
                'login': login_,
            })
        });

        const responseData = await response.json();
        if (responseData.deleted) {
            displayToast('Данные были успешно удалены из базы')
            el1.value = ''
            el2.value = ''
        }
    } else {
        displayToast('Заполните все поля ввода!', '', 'warning')
    }

};

async function retrieveAllLoginCredentials() {
    const response = await fetch('/main', {
        method: 'POST',
        headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "getAllData"},
        body: null
    });

    const responseData = await response.json();
    let data = responseData.data;
    data = data.replace(/\n/g, '<br>');
    element = document.getElementById('passwordListContainer');
    element.innerHTML = data;
};

function confirmDeleteAllLoginCredentials() {
    Swal.fire({
        title: 'Удалить все сохранённые данные?',
        text: 'Внимание! Эта операция необратима!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Да, удалить',
        cancelButtonText: 'Отмена'
    }).then((result) => {
        if (result.isConfirmed) {
            deleteAllLoginCredentials();
        }
    });
};

async function deleteAllLoginCredentials() {

    const response = await fetch(window.location.href, {
        method: 'POST',
        headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "deleteAllData"},
    });


    displayToast('Удаление данных', 'Все ваши данные успешно удалены из базы');
};


function toggdlePassword(id) {
    let pass = document.getElementById(id)
    if (pass.type === "password") {
        pass.type = "text"
    } else {
        pass.type = "password"
    }
};

async function checkLogin(log_id) {
    let user = document.getElementById(log_id).value
    if (user) {
        console.log(user)
        const response = await fetch('/validate', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "CheckLogin"},
            body: JSON.stringify({
                'obj': user,
            })
        })
        el = document.getElementById('checklogin')
        if (response.status !== 200) {
            responceData = await response.json();
            msg = responceData.message
            displayToast('Ошибка', msg, 'error')
        } else {
            el.textContent = ''
        }
    }

};

async function checkPassword(pass_id) {
    const pass = document.getElementById(pass_id)
    const password = pass.value
    if (password) {
        const response = await fetch('/validate', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "CheckPassword"},
            body: JSON.stringify({
                'obj': password
            })
        })

        if (response.status !== 200) {
            displayToast('Ошибка!', 'Пароль некорректен!', 'error')
        } else {
            el.textContent = ''
        }
    }

}

