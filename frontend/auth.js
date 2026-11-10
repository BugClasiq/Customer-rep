document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.querySelector('.auth-form');

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
      const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const result = await response.json();

      if (!response.ok) {
        alert(result.error || 'Login failed');
        return;
      }

      // Successful login
      window.location.href = 'chat_page.html';
    } catch (error) {
      console.error('Login request failed', error);
      alert('Unable to connect to server. Please try again.');
    }
  });
});


const BACKEND_URL = 'http://127.0.0.1:5000/api';

async function login(email, password) {
  const response = await fetch(`${BACKEND_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  return response.json();
}