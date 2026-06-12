const API_URL = "http://127.0.0.1:8000";

const emailInput = document.getElementById('email');
const telnumberInput = document.getElementById('telnumber');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

async function register() {
    const email = emailInput.value;
    const phone = telnumberInput.value;
    const username = usernameInput.value;
    const password = passwordInput.value;

    const response = await fetch(`${API_URL}/api/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, phone, username, password })
    });

    if (response.ok) {
        errorText.style.color = "green";
        errorText.innerText = "Регистрация успешна! Теперь войдите.";
    } else {
        const error = await response.json();
        errorText.style.color = "red";
        errorText.innerText = error.detail;
    }
}