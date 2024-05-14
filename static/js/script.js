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
            window.location.href = 'main.html'
            document.cookie = "isLogged=true; path=/";
            document.cookie = "user=" + document.getElementById('username').value + '; path=/';
        } else {
            alert('check your login and passwords')
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
            alert('CREATED')
            window.location.href = '/'
        } else {
            alert('Something has went wrong... Сheck your pass and usr again')
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
            window.location.href = 'change_password.html'
            document.cookie = "isLogged=true; path=/";
            document.cookie = "user=" + document.getElementById('username').value + '; path=/';
        } else {
            alert('Cant identify you')
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
            alert('Passwords dont match');
        } else {
            const response = await fetch(window.location.href, {
                method: 'POST',
                headers: {"Accept": "application/json", "Content-Type": "application/json"},
                body: JSON.stringify({
                    'user': getCookie('user'),
                    'password': password1 // Используем password1 вместо неопределенной переменной username
                })
            });

            const responseData = await response.json();
            const changed = responseData.changed;

            if (changed) {
                alert('changed');
                window.location.href = 'main.html';
                document.cookie = "isLogged=true; path=/";
            } else {
                alert('Something has went wrong. Check your password.')
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
        generateOutput.textContent = 'Вы не отметили ни одного чекбокса!'
    } else {
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                'action': 'GeneratePassword',
                'password_length': p_length,
                'includeLows': includeLows,
                'includeUps': includeUps,
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
    serviceName = document.getElementById('AddServiceName').value;
    login_ = document.getElementById('AddLogin').value;
    password = document.getElementById('AddPassword').value;

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
            alert('added')
        }
    } else {
        alert('ENTER SOMETHING IN THE INPUT FIELD')
    }

};

async function DeleteLoginPassword() {
    serviceName = document.getElementById('DeleteServiceName').value;
    login_ = document.getElementById('DeleteLogin').value;

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
            alert('Deleted')
        }
    } else {
        alert('ENTER SOMETHING IN THE INPUT FIELD')
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
