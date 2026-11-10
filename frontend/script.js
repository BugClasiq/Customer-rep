// 1. SELECT FRONT-END ELEMENTS
const chatForm = document.querySelector('.chat-input-form');
const chatInput = document.getElementById('chat-message');
const chatWindow = document.querySelector('.chat-window');

// The URL where your Python Flask server is listening
const BACKEND_URL = 'http://127.0.0.1:5000/api';








// ==============================================================================
// STEP A: FETCH & DISPLAY MESSAGES FROM PYTHON WHEN PAGE LOADS
// ==============================================================================
async function loadMessagesFromBackend() {
  try {
    // 1. Send a GET request to Python server
    const response = await fetch(BACKEND_URL);
    
    // 2. Parse the JSON response received from Flask
    const messages = await response.json();

    // 3. Clear existing window content before displaying fresh messages
    chatWindow.innerHTML = '';

    // 4. Loop through array received from Python and render each message
    messages.forEach(msg => {
      // Determine if it was sent by 'You' (outgoing) or Support (incoming)
      const isUser = msg.sender === 'You';
      appendMessageToDOM(msg.sender, msg.text, isUser ? 'outgoing' : 'incoming');
    });

  } catch (error) {
    console.error('Error connecting to Python backend:', error);
    chatWindow.innerHTML = '<p style="color:red;">Failed to load chat from server. Is app.py running?</p>';
  }
}

// ==============================================================================
// STEP B: POST A NEW MESSAGE TO PYTHON WHEN USER CLICKS SEND
// ==============================================================================
chatForm.addEventListener('submit', async function(event) {
  event.preventDefault(); // Stop normal form submit page reload

  const userText = chatInput.value.trim();
  if (userText === '') return;

  // Optimistically show message immediately on the screen for a fast UI feeling
  appendMessageToDOM('You', userText, 'outgoing');
  chatInput.value = '';

  try {
    // Send a POST request with JSON data to Python Flask backend
    const response = await fetch(BACKEND_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json' // Tells Python we are sending JSON text
      },
      body: JSON.stringify({
        text: userText
      })
    });

    const result = await response.json();
    console.log('Saved to Python backend:', result);

  } catch (error) {
    console.error('Failed to send message to Python:', error);
    alert('Message failed to send. Please check if your Python server is running!');
  }
});

// ==============================================================================
// HELPER: RENDER CHAT BUBBLE IN HTML
// ==============================================================================
function appendMessageToDOM(sender, text, type) {
  const newMessageDiv = document.createElement('div');
  newMessageDiv.classList.add('message', type);
  newMessageDiv.innerHTML = `
    <p><strong>${sender}:</strong> ${text}</p>
  `;
  chatWindow.appendChild(newMessageDiv);
  
  // Auto scroll down to the newest message
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// RUN IMMEDIATELY WHEN PAGE LOADS
// loadMessagesFromBackend();





async function loadMessagesFromBackend() {
  try {
    // 1. Send a GET request to Python server
    const response = await fetch(BACKEND_URL/api/orders);
    
    // 2. Parse the JSON response received from Flask
    const messages = await response.json();

    // 3. Clear existing window content before displaying fresh messages
    chatWindow.innerHTML = '';

    // 4. Loop through array received from Python and render each message
    messages.forEach(msg => {
      // Determine if it was sent by 'You' (outgoing) or Support (incoming)
      const isUser = msg.sender === 'You';
      appendMessageToDOM(msg.sender, msg.text, isUser ? 'outgoing' : 'incoming');
    });

  } catch (error) {
    console.error('Error connecting to Python backend:', error);
    chatWindow.innerHTML = '<p style="color:red;">Failed to load chat from server. Is app.py running?</p>';
  }
}

 let h3tags = document.getElementsByTagName("h3")//.innerHTML = "order_number"
for(let tag of h3tags){
  tag.innerHTML = "orderxxxsx`"
}