document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('register-form');
    const emailInput = document.getElementById('id_email');
    const password1Input = document.getElementById('id_password1');
    const password2Input = document.getElementById('id_password2');
    const usernameInput = document.getElementById('id_username');

    let emailValid = false;
    let usernameValid = false;

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    const validateUsername = debounce(function() {
        const username = usernameInput.value;
        const usernameError = document.getElementById('username-error');
        const usernameRegex = /^[a-zA-Z0-9_]+$/;

        if (username.length < 3) {
            usernameError.textContent = 'Имя пользователя должно быть не менее 3 символов';
            usernameError.className = 'error';
            usernameValid = false;
        } else if (!usernameRegex.test(username)) {
            usernameError.textContent = 'Имя пользователя может содержать только буквы, цифры и подчёркивания';
            usernameError.className = 'error';
            usernameValid = false;
        } else {
            usernameError.textContent = 'Имя пользователя корректно';
            usernameError.className = 'success';

            fetch(`${checkUsernameUrl}?username=${encodeURIComponent(username)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Ошибка запроса. Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        usernameError.textContent = `Ошибка: ${data.error}`;
                        usernameError.className = 'error';
                        usernameValid = false;
                    } else if (data.exists) {
                        usernameError.textContent = 'Это имя пользователя уже занято';
                        usernameError.className = 'error';
                        usernameValid = false;
                    } else {
                        usernameError.textContent = 'Имя пользователя свободно';
                        usernameError.className = 'success';
                        usernameValid = true;
                    }
                })
                .catch(error => {
                    console.error('Ошибка AJAX:', error);
                    usernameError.textContent = 'Ошибка проверки имени пользователя: ' + error.message;
                    usernameError.className = 'error';
                    usernameValid = false;
                });
        }
    }, 500);

    usernameInput.addEventListener('input', validateUsername);

    const validateEmail = debounce(function() {
        const email = emailInput.value;
        const emailError = document.getElementById('email-error');
        const emailRegex = /^[^\s<>(),;:!?#$%&*@]+@[^\s<>(),;:!?#$%&*@]+\.[^\s<>(),;:!?#$%&*@]+$/;

        if (!emailRegex.test(email)) {
            emailError.textContent = 'Введите корректный email';
            emailError.className = 'error';
            emailValid = false;
        } else {
            emailError.textContent = 'Email корректен';
            emailError.className = 'success';

            fetch(`${checkEmailUrl}?email=${encodeURIComponent(email)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Ошибка запроса! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        emailError.textContent = `Ошибка: ${data.error}`;
                        emailError.className = 'error';
                        emailValid = false;
                    } else if (data.exists) {
                        emailError.textContent = 'Этот email уже зарегистрирован';
                        emailError.className = 'error';
                        emailValid = false;
                    } else {
                        emailError.textContent = 'Email свободен';
                        emailError.className = 'success';
                        emailValid = true;
                    }
                })
                .catch(error => {
                    console.error('Ошибка AJAX:', error);
                    emailError.textContent = 'Ошибка проверки email: ' + error.message;
                    emailError.className = 'error';
                    emailValid = false;
                });
        }
    }, 500);

    emailInput.addEventListener('input', validateEmail);

    password1Input.addEventListener('input', function() {
        const password = password1Input.value;
        const passwordError = document.getElementById('password1-error');

        if (password.length < 6) {
            passwordError.textContent = 'Пароль должен быть не менее 6 символов';
            passwordError.className = 'error';
        } else {
            passwordError.textContent = 'Пароль корректен';
            passwordError.className = 'success';
        }

        validatePasswords();
    });

    password2Input.addEventListener('input', validatePasswords);

    function validatePasswords() {
        const password1 = password1Input.value;
        const password2 = password2Input.value;
        const password2Error = document.getElementById('password2-error');

        if (password1 !== password2) {
            password2Error.textContent = 'Пароли не совпадают';
            password2Error.className = 'error';
        } else {
            password2Error.textContent = 'Пароли совпадают';
            password2Error.className = 'success';
        }
    }

    form.addEventListener('submit', function(event) {
        const usernameError = document.getElementById('username-error');
        const emailError = document.getElementById('email-error');
        const password1Error = document.getElementById('password1-error');
        const password2Error = document.getElementById('password2-error');

        if (usernameError.className === 'error' || 
            emailError.className === 'error' || 
            password1Error.className === 'error' || 
            password2Error.className === 'error' ||
            !emailValid || 
            !usernameValid) {
            event.preventDefault();
            alert('Исправьте ошибки перед отправкой формы.');
        }
    });
});