const API_BASE = '/api';

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.querySelector('.auth-form');
  if (!loginForm) return;

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
      const response = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const result = await response.json().catch(() => ({}));

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
