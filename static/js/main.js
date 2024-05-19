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
    const loginForm = document.getElementById('RegisterForm');
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
        const response = await fetch('/main', {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "DeleteData"},
            body: JSON.stringify({
                'serviceName': serviceName,
                'login': login_,
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
    const response = await fetch(window.location.href, {
        method: 'POST',
        headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "getAllData"},
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

    const response = await fetch(window.location.href, {
        method: 'POST',
        headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "deleteAllData"},
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

// async function checkLogin(log_id) {
//     let user = document.getElementById(log_id).value
//     if (user) {
//         console.log(user)
//         const response = await fetch('/validate', {
//             method: 'POST',
//             headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "CheckLogin"},
//             body: JSON.stringify({
//                 'obj': user,
//             })
//         })
//         el = document.getElementById('checklogin')
//         if (response.status !== 200) {
//             responceData = await response.json();
//             msg = responceData.message
//             displayToast('Ошибка', msg, 'error')
//         } else {
//             el.textContent = ''
//         }
//     }
//
// };


async function exportData() {
    const responce = await fetch('/export', {
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
        console.log('Произошла ошибка', responce.status)
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


async function fetchPasswordValidation(password) {
    const response = await fetch('/api/validate', {
        method: 'POST',
        headers: {"Accept": "application/json", "Content-Type": "application/json", "Action": "CheckPassword"},
        body: JSON.stringify({
            'obj': password
        })
    })

    if (response.status === 200) {
        return true
    } else {
        return false
    }
};

async function fetchPasswordStrengthAndPwns(password) {
    const response = await fetch('/api/passwordStrength/' + password, {
        method: 'GET',
        body: null
    })
    if (response.status === 200) {
        responseData = await response.json();
        return responseData
    } else {
        return false
    }

};


async function passwordEventsCatcher(event) {
    pass1_el = document.getElementById('password')
    pass2_el = document.getElementById('passwordAgain')
    pass1 = pass1_el.value.trim()
    pass2 = pass2_el.value.trim()

    if (pass1 !== '' || pass2 !== '') {
        if (pass1 === pass2) {
            password = pass1

            validationCheck = await fetchPasswordValidation(password)
            if (validationCheck) {
                el = document.getElementById('passwordData')
                container = document.getElementById('passData')
                container.style.display = 'inline'
                el.innerHTML = 'Проверяем силу пароля и был ли он слит...'
                let passwordData = await fetchPasswordStrengthAndPwns(password)

                if (passwordData !== false) {
                    setTimeout(async function () {
                        output = 'Оценка пароля: ' + passwordData.score + '<br>' + 'pwned: ' + passwordData.pwned
                        el.innerHTML = output
                    }, 3000)


                }

            } else {
                console.log('waiting for good passws...')
            }


        } else {
            console.log('waiting for same inputs...')
        }

    } else {
        console.log('waiting for inputs...')
    }


}

async function checkPasswords(pass1_id, pass2_id) {
    console.log('started...')
    password1 = document.getElementById(pass1_id)
    password2 = document.getElementById(pass2_id)

    password1.addEventListener('blur', passwordEventsCatcher)
    password2.addEventListener('blur', passwordEventsCatcher)
};

async function addEventListenersInputs() {
    // прослушиватели поля логина
    log_inp = document.getElementById('username')
    log_inp.addEventListener('focus', function () {
        el = document.getElementById('requirements')
        el.setAttribute('open', '')
    })
    log_inp.addEventListener('blur', function () {
        el = document.getElementById('requirements')
        el.removeAttribute('open')
    })
    log_inp.addEventListener('input', logTooltips)
    // прослушиватели полей пароля
    pass1 = document.getElementById('password')
    pass2 = document.getElementById('passwordAgain')
    reqs = document.getElementById('requirements')

    pass1.addEventListener('focus', function () {
        reqs.setAttribute('open', '')
    })
    pass1.addEventListener('blur', function () {
        reqs.removeAttribute('open')
    })
    pass2.addEventListener('focus', function () {
        reqs.setAttribute('open', '')
    })
    pass2.addEventListener('blur', function () {
        reqs.removeAttribute('open')
    })

    pass1.addEventListener('input', passwordTooltips)
    pass2.addEventListener('input', passwordTooltips)


    // прослушиватель поля секретного слова
    secret = document.getElementById('secret')
    secret.addEventListener('focus', function () {
        reqs.setAttribute('open', '')
    })
    secret.addEventListener('blur', function () {
        reqs.removeAttribute('open')
    })
    secret.addEventListener('input', secretTooltips)

}

async function changeClass(obj, bef, aft) {
    obj.classList.remove(bef)
    obj.classList.add(aft)
}

async function logTooltips(event) {
    console.log('catched login')
    el_login = event.currentTarget
    el_value = el_login.value
    tooltip_val = document.getElementById('logVals')
    console.log(el_value.match(/[0-9a-zA-Z!@#$%&*_.-]+/))
    if (el_value.trim() !== '') {
        if (el_value.match(/[0-9a-zA-Z!@#$%&*_.-]+/)) {
            console.log('matched')
            changeClass(tooltip_val, 'invalid', 'valid')
        } else {
            console.log('not matched')
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