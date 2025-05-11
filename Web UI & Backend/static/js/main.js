document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const resetButton = document.getElementById('reset-button');
    const loadingIndicator = document.getElementById('loading');
    
    // Get user info from the page
    const userId = userInfo.userId || 'user_' + Math.random().toString(36).substring(2, 10);
    const threadId = 'thread_' + Math.random().toString(36).substring(2, 10);
    
    function addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message' : 'message agent-message';
        
        if (!isUser) {
            // Format agent messages for better display
            const parts = content.split(/Agent: ([^\n]+)/);
            
            if (parts.length > 1) {
                for (let i = 1; i < parts.length; i += 2) {
                    if (parts[i].trim() && parts[i+1]) {
                        const agentName = document.createElement('div');
                        agentName.className = 'agent-name';
                        agentName.textContent = parts[i].trim();
                        
                        const messageContent = document.createElement('div');
                        messageContent.className = 'message-content';
                        
                        // Process code blocks
                        const text = parts[i+1].trim();
                        const codeBlockRegex = /```([\s\S]*?)```/g;
                        let lastIndex = 0;
                        let match;
                        
                        while ((match = codeBlockRegex.exec(text)) !== null) {
                            // Add text before code block
                            if (match.index > lastIndex) {
                                const textNode = document.createTextNode(text.substring(lastIndex, match.index));
                                messageContent.appendChild(textNode);
                            }
                            
                            // Add code block
                            const pre = document.createElement('pre');
                            const code = document.createElement('code');
                            code.textContent = match[1].trim();
                            pre.appendChild(code);
                            messageContent.appendChild(pre);
                            
                            lastIndex = match.index + match[0].length;
                        }
                        
                        // Add remaining text after last code block
                        if (lastIndex < text.length) {
                            const textNode = document.createTextNode(text.substring(lastIndex));
                            messageContent.appendChild(textNode);
                        }
                        
                        messageDiv.appendChild(agentName);
                        messageDiv.appendChild(messageContent);
                        chatContainer.appendChild(messageDiv);
                    }
                }
            } else {
                // Fallback for messages without agent prefix
                const messageContent = document.createElement('div');
                messageContent.className = 'message-content';
                messageContent.textContent = content;
                messageDiv.appendChild(messageContent);
                chatContainer.appendChild(messageDiv);
            }
        } else {
            // User messages are simpler
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.textContent = content;
            messageDiv.appendChild(messageContent);
            chatContainer.appendChild(messageDiv);
        }
        
        // Auto scroll to bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, true);
        userInput.value = '';
        
        // Show loading indicator
        loadingIndicator.style.display = 'block';
        
        // Send to backend API
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                user_id: userId,
                thread_id: threadId
            })
        })
        .then(response => {
            if (!response.ok) {
                // Check if we got redirected due to session expiry
                if (response.url.includes('login')) {
                    window.location.href = '/login?session_expired=1';
                    throw new Error('Session expired');
                }
                return response.json();
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
            
            // Add agent response
            if (data.response) {
                addMessage(data.response, false);
            } else {
                addMessage("Sorry, I couldn't process your request.", false);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (!error.message.includes('Session expired')) {
                loadingIndicator.style.display = 'none';
                addMessage("Error connecting to the server.", false);
            }
        });
    }
    
    function resetChat() {
        // Clear chat UI
        while (chatContainer.children.length > 1) {
            chatContainer.removeChild(chatContainer.lastChild);
        }
        
        // Reset server-side conversation
        fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                thread_id: threadId
            })
        })
        .then(response => {
            if (!response.ok) {
                // Check if we got redirected due to session expiry
                if (response.url.includes('login')) {
                    window.location.href = '/login?session_expired=1';
                    throw new Error('Session expired');
                }
                return response.json();
            }
            return response.json();
        })
        .then(data => {
            console.log('Chat reset:', data);
        })
        .catch(error => {
            console.error('Error resetting chat:', error);
            if (!error.message.includes('Session expired')) {
                addMessage("Error connecting to the server.", false);
            }
        });
    }
    
    // Event listeners
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    if (resetButton) {
        resetButton.addEventListener('click', resetChat);
    }
    
    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Focus input field on load
        userInput.focus();
    }
    
    // Check connection on load
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            console.log('Backend health check:', data);
        })
        .catch(error => {
            console.error('Error connecting to backend:', error);
            if (chatContainer) {
                addMessage("Warning: Could not connect to backend API.", false);
            }
        });
});