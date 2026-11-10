// Customer support chat — talks to the Flask backend at /api (proxied by nginx in Docker).
const API_BASE = '/api';
const chatForm = document.querySelector('.chat-input-form');
const chatInput = document.getElementById('chat-message');
const chatWindow = document.querySelector('.chat-window');

if (chatForm && chatInput && chatWindow) {
  chatForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const userText = chatInput.value.trim();
    if (userText === '') return;

    appendMessageToDOM('You', userText, 'outgoing');
    chatInput.value = '';

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userText })
      });

      const result = await response.json().catch(() => ({}));

      if (!response.ok) {
        appendMessageToDOM('Support', result.error || 'Something went wrong.', 'incoming');
        return;
      }

      appendMessageToDOM('Support', result.response, 'incoming');
    } catch (error) {
      console.error('Failed to send message to backend:', error);
      appendMessageToDOM('Support', 'Unable to reach the server. Please try again.', 'incoming');
    }
  });
}

function appendMessageToDOM(sender, text, type) {
  const newMessageDiv = document.createElement('div');
  newMessageDiv.classList.add('message', type);

  const paragraph = document.createElement('p');
  const strong = document.createElement('strong');
  strong.textContent = `${sender}: `;
  paragraph.appendChild(strong);
  paragraph.appendChild(document.createTextNode(text));

  newMessageDiv.appendChild(paragraph);
  chatWindow.appendChild(newMessageDiv);

  // Auto scroll down to the newest message
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
