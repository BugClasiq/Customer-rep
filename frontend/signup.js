const API_BASE = '/api';

document.addEventListener('DOMContentLoaded', () => {
  const signupForm = document.querySelector('.auth-form');
  if (!signupForm) return;

  signupForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const payload = {
      first_name: document.getElementById('first-name').value.trim(),
      last_name: document.getElementById('last-name').value.trim(),
      email: document.getElementById('email').value.trim(),
      phone_number: document.getElementById('phone').value.trim(),
      address: document.getElementById('address').value.trim(),
      password: document.getElementById('password').value,
      confirm_password: document.getElementById('confirm-password').value
    };

    try {
      const response = await fetch(`${API_BASE}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await response.json().catch(() => ({}));

      if (!response.ok) {
        alert(result.error || 'Sign up failed');
        return;
      }

      alert('Account created! Please log in.');
      window.location.href = 'login.html';
    } catch (error) {
      console.error('Signup request failed', error);
      alert('Unable to connect to server. Please try again.');
    }
  });
});
