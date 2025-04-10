document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('register-form');
    const emailInput = document.getElementById('id_email');
    const password1Input = document.getElementById('id_password1');
    const password2Input = document.getElementById('id_password2');
    const usernameInput = document.getElementById('id_username');

    emailInput.addEventListener('input', function() {
        const email = emailInput.value;
        const emailError = document.getElementById('email-error');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            emailError.textContent = 'Введите корректный email';
            emailError.className = 'error';
        } else {
            emailError.textContent = 'Email корректен';
            emailError.className = 'success';

            fetch(`/auth/check-email/?email=${encodeURIComponent(email)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        emailError.textContent = 'Этот email уже зарегистрирован';
                        emailError.className = 'error';
                    }
                })
                .catch(error => {
                    console.error('Ошибка AJAX:', error);
                    emailError.textContent = 'Ошибка проверки email';
                    emailError.className = 'error';
                });
        }
    });

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
        const emailError = document.getElementById('email-error');
        const password1Error = document.getElementById('password1-error');
        const password2Error = document.getElementById('password2-error');

        if (emailError.className === 'error' || 
            password1Error.className === 'error' || 
            password2Error.className === 'error') {
            event.preventDefault();
            alert('Исправьте ошибки перед отправкой формы.');
        }
    });
});
