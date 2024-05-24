function authenticateUser() {
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        let username = document.getElementById('username').value
        let password = document.getElementById('password').value


        const response = await fetch('/user/login', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'username': username,
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
    const loginForm = document.getElementById('RegisterForm');
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const user = document.getElementById('username').value
        const password = document.getElementById('password').value
        const secret = document.getElementById('secret').value


        if (await checkRequirements() === true) {

            const response = await fetch('/user/register', {
                method: 'POST',
                headers: {"Accept": "application/json", "Content-Type": "application/json"},
                body: JSON.stringify({
                    'username': user,
                    'password': password,
                    'secret': secret
                })
            });


            if (response.status === 200) {
                displayToast('Аккаунт успешно создан', 'Сейчас вы будете перенаправлены на главную страницу')

                setTimeout(function () {
                    window.location.href = '/'

                }, 3000)
            } else {
                displayToast('Что-то пошло не так...', 'Произошла ошибка при обработке введенных данных. Пожалуйста, проверьте их и попробуйте еще раз.', 'error')
            }

        } else {
            displayToast('Проверьте ввод', 'Ввши данные соответствуют не всем требованиям', 'warning')
        }


    });

};


async function validateUserForPasswordReset() {

    let form = document.getElementById('forgotForm')

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        let username = document.getElementById('username').value
        let secret = document.getElementById('secret').value


        const response = await fetch('/user/forgot', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'username': username,
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


            const response = await fetch('/user/change_password', {
                method: 'POST',
                headers: {"Accept": "application/json", "Content-Type": "application/json", },
                body: JSON.stringify({
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
    const scoreOutput = document.getElementById('score');
    const pwnedOutput = document.getElementById('pwned');
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
        const response = await fetch('/user/service/generatePassword', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "GeneratePassword", },
            body: JSON.stringify({
                'length': p_length,
                'include_lower': includeLows,
                'include_upper': includeUps,
                'include_digits': include_digs,
                'include_symbols': include_spec,
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
        const response = await fetch('/credential/add', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "AddNewData", },
            body: JSON.stringify({
                'service': serviceName,
                'username': login_,
                'password': password
            })
        });

        if (response.status === 200) {
            el1.value = ''
            el2.value = ''
            el3.value = ''

            displayToast('Данные были успешно добавлены в базу')
            setTimeout(async function () {
                    window.location.reload()
                }, 1500
            )
        } else {
            displayToast('Что-то пошло не так...', 'Проверьте введённые данные. Возможно, такая связка Сервис-Логин уже есть в базе', 'error')
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
        const response = await fetch('/credential/delete', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "DeleteData", },
            body: JSON.stringify({
                'service': serviceName,
                'username': login_,
            })
        });


        if (response.status === 200) {
            displayToast('Данные были успешно удалены из базы')
            el1.value = ''
            el2.value = ''
            setTimeout(async function () {
                    window.location.reload()
                }, 1500
            )
        }
    } else {
        displayToast('Заполните все поля ввода!', '', 'warning')
    }

};

async function retrieveAllLoginCredentials() {
    const response = await fetch('/credential/get_all', {
        method: 'GET',
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
        body: null
    });

    const responseData = await response.json();
    let data = responseData.data;
    table = generateTable(data)

    element = document.getElementById('passwordListContainer');

    element.innerHTML = table;
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

    const response = await fetch('/credential/delete_all', {
        method: 'GET',
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
    });

    if (response.status === 200) {
        displayToast('Удаление данных', 'Все ваши данные успешно удалены из базы');
        setTimeout(async function () {
                window.location.reload()
            }, 1500
        )
    }
};


function toggdlePassword(id) {
    let pass = document.getElementById(id)
    if (pass.type === "password") {
        pass.type = "text"
    } else {
        pass.type = "password"
    }
};

async function exportData() {
    const responce = await fetch('/user/service/export', {
        method: 'GET',
    });

    if (responce.status === 200) {
        const blob = await responce.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.href = url

        const filename = responce.headers.get('Content-Disposition')
            .split('filename=')[1]
            .replace(/"/g, '')
        a.download = filename
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
    } else if (responce.status === 404) {
        displayToast('У вас пока нет данных для скачивания', '', 'info')
    } else {

        displayToast('Во время скачивания файла произошла ошибка', 'Если подобное повторится, обратитесь к администратору сайта', 'error')
    }

};

function generateTable(data) {
    let table = '<table><thread><tr>'

    data[0].forEach(element => {
        table += '<th>' + element + '</th>'
    })
    table += '</tr></thread><tbody>';

    data.splice(0, 1)

    data.forEach(row => {
        table += '<tr>'

        row.forEach(val => {
            table += '<td>' + val + '</td>'
        })
        table += '</tr>'
    })
    table += '</tbody></table>'
    return table
};


async function fetchPasswordStrengthAndPwns(password) {

    el = document.getElementById('passwordData')
    container = document.getElementById('passData')
    container.style.display = 'inline'
    el.innerHTML = 'Проверяем силу пароля и был ли он слит...'


    const response = await fetch('/user/service/passwordStrength/' + password, {
        method: 'GET',
        body: null
    })
    if (response.status === 200) {
        responseData = await response.json();
        setTimeout(async function () {
            output = 'Оценка пароля: ' + responseData.score + '<br>' + 'pwned: ' + responseData.pwned
            el.innerHTML = output
        }, 3000)


    } else {
        return false
    }

};


async function addEventListenersForInputs() {
    //  прослушиваем событие наведения мыши на контейнер с формой RegisterForm
    form = document.getElementById('RegisterForm')
    req = document.getElementById('requirements')
    form.addEventListener('mouseover', function (event) {
        req.setAttribute('open', '')
    })
    form.addEventListener('mouseout', function (event) {
        req.removeAttribute('open')
    })

    // прослушиватели поля логина
    log_inp = document.getElementById('username')
    log_inp.addEventListener('input', logTooltips)
    // прослушиватели полей пароля
    pass1 = document.getElementById('password')
    pass2 = document.getElementById('passwordAgain')

    pass1.addEventListener('input', passwordTooltips)
    pass2.addEventListener('input', passwordTooltips)


    // прослушиватель поля секретного слова
    secret = document.getElementById('secret')

    secret.addEventListener('input', secretTooltips)


}


async function changeClass(obj, bef, aft) {
    obj.classList.remove(bef)
    obj.classList.add(aft)
}

async function logTooltips(event) {

    el_login = event.currentTarget
    el_value = el_login.value
    tooltip_val = document.getElementById('logVals')

    if (el_value.trim() !== '') {
        if (el_value.match(/^[0-9a-zA-Z!@#$%&*_.-]+$/)) {

            changeClass(tooltip_val, 'invalid', 'valid')
        } else {

            changeClass(tooltip_val, 'valid', 'invalid')
        }
    } else {
        changeClass(tooltip_val, 'invalid', 'valid')
    }
    tooltip_length = document.getElementById('logLength')
    if (el_value.length >= 3) {
        changeClass(tooltip_length, 'invalid', 'valid')
    } else {
        changeClass(tooltip_length, 'valid', 'invalid')
    }


}

async function passwordTooltips(event) {
    pass_1 = document.getElementById('password')
    pass_2 = document.getElementById('passwordAgain')

    pass1_value = pass1.value
    pass2_value = pass2.value

    pass_same = document.getElementById('passSame')
    if (pass1_value === pass2_value) {
        changeClass(pass_same, 'invalid', 'valid')
    } else {
        changeClass(pass_same, 'valid', 'invalid')
    }

    pass_length = document.getElementById('passLength')

    if (pass_same.classList.contains('valid')) {
        if (pass1_value.length >= 8) {
            changeClass(pass_length, 'invalid', 'valid')
        } else {
            changeClass(pass_length, 'valid', 'invalid')
        }

        passVals = document.getElementById('passVals')
        if (pass1_value.match(/^[0-9a-zA-Z!@#$%&*_.-]+$/)) {
            changeClass(passVals, 'invalid', 'valid')
        } else {
            changeClass(passVals, 'valid', 'invalid')
        }

        passReqs = document.getElementById('passReqs')
        if (pass1_value.match(/(?=.*[a-zA-Z])(?=.*[0-9])/)) {
            changeClass(passReqs, 'invalid', 'valid')
        } else {
            changeClass(passReqs, 'valid', 'invalid')
        }

        passReqs = document.getElementById('requirements').querySelectorAll('[id^="pass"]')
        if (await checkValidPassReqs(passReqs) === true) {
            await fetchPasswordStrengthAndPwns(pass1_value)
        }

    }
}

async function secretTooltips(event) {
    secret = document.getElementById('secret')
    secret_value = secret.value

    secretVals = document.getElementById('secretVals')
    if (secret_value !== '') {
        if (secret_value.match(/^[a-zA-Zа-яА-Я0-9!@#$%&*_.-]+$/)) {
            changeClass(secretVals, 'invalid', 'valid')
        } else {
            changeClass(secretVals, 'valid', 'invalid')
        }
    } else {
        changeClass(secretVals, 'invalid', 'valid')
    }
}

async function checkRequirements() {
    reqs = document.getElementById('requirements')
    req_lis = reqs.querySelectorAll('li')


    for (i = 0; i < req_lis.length; i++) {
        if (req_lis[i].classList.contains('invalid')) {
            return false
        }
    }
    return true
}

async function checkValidPassReqs(req) {

    for (let i = 0; i < req.length; i++) {
        if (req[i].classList.contains('invalid')) {
            return false
        }
    }
    return true
}

// TODO: reformat js functions file. Delete old functions like changePasswords etc...
