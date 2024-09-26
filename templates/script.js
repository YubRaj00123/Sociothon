window.addEventListener('load', function() {
    const loader = document.getElementById('loader-section');
    const mainContent = document.getElementById('main-content');
    setTimeout(() => {
        loader.style.display = 'none';
        mainContent.style.display = 'flex';
    }, 5000);
});

const loginForm = document.getElementById('loginForm');
loginForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    if (email === 'admin@puti.com' && password === 'admin') {
        alert('Login successful!');
        window.location.href = 'dashboard.html';
    } else {
        showError('Invalid email or password');
    }
});

function showError(message) {
    let errorMessage = document.getElementById('error-message');
    if (!errorMessage) {
        errorMessage = document.createElement('div');
        errorMessage.id = 'error-message';
        errorMessage.style.color = 'red';
        errorMessage.style.marginTop = '10px';
        loginForm.appendChild(errorMessage);
    }
    errorMessage.textContent = message;
}

const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle.addEventListener('change', function() {
    document.body.classList.toggle('dark-mode');
});

const passwordToggle = document.querySelector('.password-toggle');
const passwordField = document.getElementById('password');
passwordToggle.addEventListener('click', function() {
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);
    this.classList.toggle('fa-eye-slash');
});