function toggleListening() {
    const micBtn = document.getElementById('mic-btn');
    const statusText = document.getElementById('status-text');
    const chatBox = document.getElementById('chat-box');

    if (micBtn.classList.contains('listening')) {
        // Already listening, maybe stop? For now, we rely on backend timeout.
        return;
    }

    // Start listening UI
    micBtn.classList.add('listening');
    statusText.textContent = "Listening...";

    // Call backend
    fetch('/process_command', {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            // Stop listening UI
            micBtn.classList.remove('listening');
            statusText.textContent = "Ready to listen...";

            // Add user message to chat
            if (data.command) {
                addMessage(data.command, 'user');
            }

            // Add assistant response to chat
            if (data.response) {
                addMessage(data.response, 'assistant');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            micBtn.classList.remove('listening');
            statusText.textContent = "Error occurred. Try again.";
        });
}

function addMessage(text, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);

    const textP = document.createElement('p');
    textP.textContent = text;

    messageDiv.appendChild(textP);
    chatBox.appendChild(messageDiv);

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}
