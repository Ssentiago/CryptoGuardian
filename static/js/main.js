// В этом блоке расположены функции, работающие с учетной записью пользователя
// authenticateUser выполняется на экране /login.html и добавляет "прослушиватель" события "submit", в форме отправки учетных данных, затем возвращает результат их проверки на сервере
// createAccount выполняется на экране /register.html и также добавляет "прослушиватель" события "submit" в форме отправки учетных данных. Возвращает результат операции добавления пользователя в БД
// validateUserForPasswordReset выполняется на экране /forgot.html и проверяет валидность пользователя по его логину и секретному слову. Если валиден, то пропускает его на экран смены пароля
// changePassword выполняется на экране /change_passsword.html и меняет пароль пользователя в БД
// logout выполняется на главном экране при нажатии кнопки "выйти", разлогинивает пользователя и возвращает на главный экран

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


        const responseData = await response.json();
        const isAuthenticated = responseData.isValidated;

        if (isAuthenticated) {
            displayToast('Вы успешно вошли в систему', 'Сейчас вы будете перенаправлены на страницу входа')
            setTimeout(function () {
                document.cookie = "isLogged=true; path=/";
                document.cookie = "user=" + document.getElementById('username').value + '; path=/';
                window.location.href = 'main.html'
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

    let form = document.getElementById('ForgotForm')

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


        const responseData = await response.json();
        const isAuthenticated = responseData.isValidated;

        if (isAuthenticated) {
            displayToast('Валидация прошла успешно', 'Сейчас вы будете перенаправлены на страницу смены пароля')
            setTimeout(function () {
                document.cookie = "isLogged=true; path=/";
                document.cookie = "user=" + document.getElementById('username').value + '; path=/';
                window.location.href = 'change_password.html'
            }, 2000)

        } else {
            displayToast('Пользователь не найден в системе', 'Попробуйте ещё раз', 'error')
        }
    })


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
                    'user': getCookieValue('user'),
                    'password': password1
                })
            });

            const responseData = await response.json();
            const changed = responseData.changed;

            if (changed) {
                displayToast('Смена пароля произошла успешно', 'Сейчас вы будете перенаправлены на главную страницу')
                setTimeout(function () {
                    document.cookie = "isLogged=true; path=/";
                    window.location.href = 'main.html';
                }, 2000)

            } else {
                displayToast('Что-то пошло не так...', 'Проверьте введённые данные', 'error')
            }
        }
    });

};

function logout() {
    displayToast('До встречи!', '', '')
    setTimeout(function () {
        deleteCookie('user')
        document.cookie = "isLogged=false"
        window.location.href = '/'
    }, 2000)


};

// в этом блоке расположены функции сервисного назначения
// generatePassword - генерирует пароль по полученным из формы критериям
// displayToast - отображает для пользователя всплывающее уведомление
// getUserName - маленькая функция, единственное её назначение - получить имя пользователя, который сейчас залогинен и отобразить его в приветствии на главном экране
// getCookieValue - извлекает значение имени пользователя из куки
// deleteCookie - удаляет куки с именем пользователя


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

function getUserName() {
    let elem = document.getElementById('catch_user')
    let name_user = getCookieValue('user')
    elem.textContent = name_user
};

const getCookieValue = (name) => {
    return document.cookie.split('; ').reduce((r, v) => {
        const parts = v.split('=');
        return parts[0] === name ? decodeURIComponent(parts[1]) : r;
    }, '');
};

function deleteCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
};


// функции в этом блоке оперируют с данными пользователя в БД
// addLoginCredentials - добавляет связку "сервис-логин-пароль" в БД
// deleteLoginCredentials - удаляет связку "сервис-логин-пароль" из БД на основании связки "сервис-логин"
// retrieveAllLoginCredentials - выводит все сохранённые данные пользователя из БД
// confirmDeleteAllLoginCredentials - выводит подтверждение при попытке пользователя запустить процесс удаления всех его данных из БД
// deleteAllLoginCredentials - запускает процесс удаления всех данных пользователя из БД

async function addLoginCredentials() {
    let el1 = document.getElementById('AddServiceName')
    let el2 = document.getElementById('AddLogin')
    let el3 = document.getElementById('AddPassword')
    let serviceName = el1.value
    let login_ = el2.value;
    let password = el3.value;

    if (serviceName && login_ && password) {
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'user': getCookieValue('user'),
                'action': 'AddNewData',
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
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'user': getCookieValue('user'),
                'action': 'DeleteData',
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
    let user = getCookieValue('user')

    const response = await fetch(window.location.href, {
        method: 'POST',
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
        body: JSON.stringify({
            'user': getCookieValue('user'),
            'action': 'getAllData',
        })
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
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
        body: JSON.stringify({
            'user': getCookieValue('user'),
            'action': 'delAllData',
        })
    });

    const responseData = await response.json();
    displayToast('Удаление данных', 'Все ваши данные успешно удалены из базы');
};

