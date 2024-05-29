function handleLoginFormSubmission() {
  const loginForm = document.getElementById("loginForm");
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    const response = await fetch("/login", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    if (response.status === 200) {
      showNotification(
        "Вы успешно вошли в систему",
        "Сейчас вы будете перенаправлены на страницу входа",
      );

      setTimeout(function () {
        window.location.replace("/protected/main");
      }, 3000);
    } else {
      showNotification(
        "Что-то пошло не так...",
        "Проверьте логин и пароль",
        "error",
      );
    }
  });
}

function handleRegistrationFormSubmission() {
  const loginForm = document.getElementById("RegisterForm");
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const user = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const secret = document.getElementById("secret").value;

    if ((await validateInputRequirements()) === true) {
      const response = await fetch("/register", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: user,
          password: password,
          secret: secret,
        }),
      });

      if (response.status === 200) {
        showNotification(
          "Аккаунт успешно создан",
          "Сейчас вы будете перенаправлены на главную страницу",
        );
        setTimeout(function () {
          window.location.replace("/");
        }, 3000);
      } else {
        showNotification(
          "Что-то пошло не так...",
          "Произошла ошибка при обработке введенных данных. Пожалуйста, проверьте их и попробуйте еще раз.",
          "error",
        );
      }
    } else {
      showNotification(
        "Проверьте ввод",
        "Ввши данные соответствуют не всем требованиям",
        "warning",
      );
    }
  });
}

async function handlePasswordResetRequest() {
  let form = document.getElementById("forgotForm");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    let username = document.getElementById("username").value;
    let secret = document.getElementById("secret").value;

    const response = await fetch("/forgot", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        secret: secret,
      }),
    });

    if (response.status === 200) {
      showNotification(
        "Валидация прошла успешно",
        "Сейчас вы будете перенаправлены на страницу смены пароля",
      );
      setTimeout(function () {
        window.location.replace("/protected/change_password");
      }, 2000);
    } else {
      showNotification(
        "Пользователь не найден в системе",
        "Попробуйте ещё раз",
        "error",
      );
    }
  });
}

async function handleChangePasswordFormSubmission() {
  const form = document.getElementById("ChangeForm");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const password1 = document.getElementById("pass1").value;
    const password2 = document.getElementById("pass2").value;

    if (password1 !== password2) {
      showNotification("Пароли не совпадают", "", "error");
    } else {
      const response = await fetch("/protected/user/change_password", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          password: password1,
        }),
      });

      if (response.status === 200) {
        showNotification(
          "Смена пароля произошла успешно",
          "Сейчас вы будете перенаправлены на главную страницу",
        );
        setTimeout(function () {
          window.location.replace("/protected/main");
        }, 2000);
      } else {
        showNotification(
          "Ваш пароль содержит некорректные данные",
          "",
          "error",
        );
      }
    }
  });
}

async function handleLogout() {
  showNotification("До встречи!", "", "");

  const response = await fetch("/protected/user/service/logout", {
    method: "GET",
  });

  if (response.status === 200) {
    setTimeout(async function () {
      window.location.replace("/");
    }, 2000);
  }
}

async function handlePasswordGeneration() {
  const generateOutput = document.getElementById("generatedPassword");
  const scoreOutput = document.getElementById("score");
  const pwnedOutput = document.getElementById("pwned");
  const p_length_field = document.getElementById("passwordLength");

  if (parseInt(p_length_field.value) > parseInt(p_length_field.max)) {
    p_length_field.value = p_length_field.max;
  }

  let p_length = p_length_field.value;

  let includeLows = document.getElementById("includeLows").checked;
  let includeUps = document.getElementById("includeUps").checked;
  let include_digs = document.getElementById("includeNumbers").checked;
  let include_spec = document.getElementById("includeSpecialSymbols").checked;
  let check = includeLows || includeUps || include_digs || include_spec;
  if (!check) {
    showNotification("Вы не отметили ни одного чекбокса", "", "warning");
  } else {
    const response = await fetch("/protected/user/service/generatePassword", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Action: "GeneratePassword",
      },
      body: JSON.stringify({
        length: p_length,
        include_lower: includeLows,
        include_upper: includeUps,
        include_digits: include_digs,
        include_symbols: include_spec,
      }),
    });
    const responseData = await response.json();
    const password = await responseData.password;
    generateOutput.textContent = password;
  }
}

function showNotification(title, content = "", icon = "success") {
  return Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener("mouseenter", Swal.stopTimer);
      toast.addEventListener("mouseleave", Swal.resumeTimer);
    },
  }).fire({
    icon: icon,
    title: title,
    text: content,
  });
}

async function handleCredentialAddition() {
  let el1 = document.getElementById("AddServiceName");
  let el2 = document.getElementById("AddLogin");
  let el3 = document.getElementById("AddPassword");
  let serviceName = el1.value;
  let login_ = el2.value;
  let password = el3.value;

  if (serviceName && login_ && password) {
    const response = await fetch("/protected/credential/add", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Action: "AddNewData",
      },
      body: JSON.stringify({
        service: serviceName,
        username: login_,
        password: password,
      }),
    });

    if (response.status === 200) {
      el1.value = "";
      el2.value = "";
      el3.value = "";

      showNotification("Данные были успешно добавлены в базу");
      await updatePasswordListAndCounter();
    } else {
      showNotification(
        "Что-то пошло не так...",
        "Проверьте введённые данные. Возможно, такая связка Сервис-Логин уже есть в базе",
        "error",
      );
    }
  } else {
    showNotification("Заполните все поля ввода", "", "warning");
  }
}

async function handleCredentialDeletion() {
  let el1 = document.getElementById("DeleteServiceName");
  let el2 = document.getElementById("DeleteLogin");
  let serviceName = el1.value;
  let login_ = el2.value;

  if (serviceName && login_) {
    const response = await fetch("/protected/credential/delete", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Action: "DeleteData",
      },
      body: JSON.stringify({
        service: serviceName,
        username: login_,
      }),
    });

    if (response.status === 200) {
      showNotification("Данные были успешно удалены из базы");
      el1.value = "";
      el2.value = "";
      await updatePasswordListAndCounter();
    } else {
      showNotification("Такая запись не была найдена в базе", "", "warning");
    }
  } else {
    showNotification("Заполните все поля ввода!", "", "warning");
  }
}

async function fetchAllCredentials() {
  const response = await fetch("/protected/credential/get_all", {
    method: "GET",
    headers: { Accept: "application/json", "Content-Type": "application/json" },
    body: null,
  });

  const responseData = await response.json();
  let data = responseData.data;
  table = generateHTMLTable(data);

  element = document.getElementById("passwordListContainer");

  element.innerHTML = table;
  el = document.getElementById("tablecontainer");
  el.style.display = "block";
}

function confirmDeleteAllCredentials() {
  Swal.fire({
    title: "Удалить все сохранённые данные?",
    text: "Внимание! Эта операция необратима!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Да, удалить",
    cancelButtonText: "Отмена",
  }).then((result) => {
    if (result.isConfirmed) {
      deleteAllLoginCredentials();
    }
  });
}

async function deleteAllLoginCredentials() {
  const response = await fetch("/protected/credential/delete_all", {
    method: "GET",
    headers: { Accept: "application/json", "Content-Type": "application/json" },
  });

  if (response.status === 200) {
    showNotification(
      "Удаление данных",
      "Все ваши данные успешно удалены из базы",
    );
    await updatePasswordListAndCounter();
  }
}

function togglePasswordVisibility(id) {
  let pass = document.getElementById(id);
  if (pass.type === "password") {
    pass.type = "text";
  } else {
    pass.type = "password";
  }
}

async function exportUserData() {
  const responce = await fetch("/protected/user/service/export", {
    method: "GET",
  });

  if (responce.status === 200) {
    const blob = await responce.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;

    const filename = responce.headers
      .get("Content-Disposition")
      .split("filename=")[1]
      .replace(/"/g, "");
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
  } else if (responce.status === 404) {
    showNotification("У вас пока нет данных для скачивания", "", "info");
  } else {
    showNotification(
      "Во время скачивания файла произошла ошибка",
      "Если подобное повторится, обратитесь к администратору сайта",
      "error",
    );
  }
}

function generateHTMLTable(data) {
  let table = "<table><thread><tr>";

  data[0].forEach((element) => {
    table += "<th>" + element + "</th>";
  });
  table += "</tr></thread><tbody>";

  data.splice(0, 1);

  data.forEach((row) => {
    table += "<tr>";

    row.forEach((val) => {
      table += "<td>" + val + "</td>";
    });
    table += "</tr>";
  });
  table += "</tbody></table>";
  return table;
}

async function fetchPasswordInfo(password) {
  el = document.getElementById("passwordData");
  container = document.getElementById("passData");
  container.style.display = "inline";
  el.innerHTML = "Проверяем силу пароля и был ли он слит...";

  const response = await fetch("/passwordStrength/" + password, {
    method: "GET",
    body: null,
  });
  if (response.status === 200) {
    responseData = await response.json();
    setTimeout(async function () {
      output =
        "Оценка пароля: " +
        responseData.score +
        "<br>" +
        "pwned: " +
        responseData.pwned;
      el.innerHTML = output;
    }, 3000);
  } else {
    return false;
  }
}

async function addInputEventListeners() {
  //  прослушиваем событие наведения мыши на контейнер с формой RegisterForm
  form = document.getElementById("RegisterForm");
  req = document.getElementById("requirements");
  form.addEventListener("mouseover", function (event) {
    req.setAttribute("open", "");
  });
  form.addEventListener("mouseout", function (event) {
    req.removeAttribute("open");
  });

  // прослушиватели поля логина
  log_inp = document.getElementById("username");
  log_inp.addEventListener("input", showLoginTooltips);
  // прослушиватели полей пароля
  pass1 = document.getElementById("password");
  pass2 = document.getElementById("passwordAgain");

  pass1.addEventListener("input", showPasswordTooltips);
  pass2.addEventListener("input", showPasswordTooltips);

  // прослушиватель поля секретного слова
  secret = document.getElementById("secret");

  secret.addEventListener("input", showSecretTooltips);
}

async function changeElementClass(obj, bef, aft) {
  obj.classList.remove(bef);
  obj.classList.add(aft);
}

async function showLoginTooltips(event) {
  el_login = event.currentTarget;
  el_value = el_login.value;
  tooltip_val = document.getElementById("logVals");

  if (el_value.trim() !== "") {
    if (el_value.match(/^[0-9a-zA-Z!@#$%&*_.-]+$/)) {
      changeElementClass(tooltip_val, "invalid", "valid");
    } else {
      changeElementClass(tooltip_val, "valid", "invalid");
    }
  } else {
    changeElementClass(tooltip_val, "invalid", "valid");
  }
  tooltip_length = document.getElementById("logLength");
  if (el_value.length >= 3) {
    changeElementClass(tooltip_length, "invalid", "valid");
  } else {
    changeElementClass(tooltip_length, "valid", "invalid");
  }
}

async function showPasswordTooltips(event) {
  pass_1 = document.getElementById("password");
  pass_2 = document.getElementById("passwordAgain");

  pass1_value = pass1.value;
  pass2_value = pass2.value;

  pass_same = document.getElementById("passSame");
  if (pass1_value === pass2_value) {
    changeElementClass(pass_same, "invalid", "valid");
  } else {
    changeElementClass(pass_same, "valid", "invalid");
  }

  pass_length = document.getElementById("passLength");

  if (pass_same.classList.contains("valid")) {
    if (pass1_value.length >= 8) {
      changeElementClass(pass_length, "invalid", "valid");
    } else {
      changeElementClass(pass_length, "valid", "invalid");
    }

    passVals = document.getElementById("passVals");
    if (pass1_value.match(/^[0-9a-zA-Z!@#$%&*_.-]+$/)) {
      changeElementClass(passVals, "invalid", "valid");
    } else {
      changeElementClass(passVals, "valid", "invalid");
    }

    passReqs = document.getElementById("passReqs");
    if (pass1_value.match(/(?=.*[a-zA-Z])(?=.*[0-9])/)) {
      changeElementClass(passReqs, "invalid", "valid");
    } else {
      changeElementClass(passReqs, "valid", "invalid");
    }

    passReqs = document
      .getElementById("requirements")
      .querySelectorAll('[id^="pass"]');
    if ((await validatePasswordRequirements(passReqs)) === true) {
      await fetchPasswordInfo(pass1_value);
    }
  }
}

async function showSecretTooltips(event) {
  secret = document.getElementById("secret");
  secret_value = secret.value;

  secretVals = document.getElementById("secretVals");
  secretLength = document.getElementById("secretLength");
  if (secret_value !== "") {
    if (secret.value.length > 2) {
      changeElementClass(secretLength, "invalid", "valid");
    } else {
      changeElementClass(secretLength, "valid", "invalid");
    }
    if (secret_value.match(/^[a-zA-Zа-яА-Я0-9!@#$%&*_.-]+$/)) {
      changeElementClass(secretVals, "invalid", "valid");
    } else {
      changeElementClass(secretVals, "valid", "invalid");
    }
  } else {
    changeElementClass(secretVals, "invalid", "valid");
  }
}

async function validateInputRequirements() {
  reqs = document.getElementById("requirements");
  req_lis = reqs.querySelectorAll("li");

  for (i = 0; i < req_lis.length; i++) {
    if (req_lis[i].classList.contains("invalid")) {
      return false;
    }
  }
  return true;
}

async function validatePasswordRequirements(req) {
  for (let i = 0; i < req.length; i++) {
    if (req[i].classList.contains("invalid")) {
      return false;
    }
  }
  return true;
}

function CreateAjaxRequest() {
  var Request = false;

  if (window.XMLHttpRequest) {
    //Gecko-совместимые браузеры, Safari, Konqueror
    Request = new XMLHttpRequest();
  } else if (window.ActiveXObject) {
    //Internet explorer
    try {
      Request = new ActiveXObject("Microsoft.XMLHTTP");
    } catch (CatchException) {
      Request = new ActiveXObject("Msxml2.XMLHTTP");
    }
  }

  return Request;
}

function sendAjaxRequest(method, path, args, handler) {
  // Создаём запрос
  var Request = CreateAjaxRequest();

  // Проверяем существование запроса еще раз
  if (!Request) {
    return;
  }

  // Назначаем пользовательский обработчик
  Request.onreadystatechange = function () {
    // Если обмен данными завершен
    if (Request.readyState == 4) {
      // Передаем управление обработчику пользователя
      handler(Request);
    }
  };

  // Инициализируем соединение
  Request.open(method, path, true);

  // Посылаем запрос
  Request.send();
}

async function updatePasswordListAndCounter() {
  var handler = async function (Request) {
    if (Request.status === 200) {
      responseData = JSON.parse(Request.responseText);
      let data = responseData.data;
      console.log(data.length);
      table = generateHTMLTable(data);
      document.getElementById("passwordListContainer").innerHTML = table;
      document.getElementById("passwordsCounter").textContent =
        await formatDataForAjax(data.length);
    } else {
      console.error("Failed to update passwords list.");
    }
  };

  sendAjaxRequest("GET", "/protected/credential/get_all", "", handler);
}

async function formatDataForAjax(count) {
  if (count === 0) {
    return "У вас пока не сохранено никаких паролей";
  } else if (count === 1) {
    return "У вас сохранён " + count + " пароль";
  } else if (count % 10 > 1 && count % 10 < 5) {
    return "У вас сохранено " + count + " пароля";
  } else {
    return "У вас сохранено " + count + " паролей";
  }
}
