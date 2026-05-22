// Connect to server
const socket = io();

// Send message function
function sendMessage() {

    let input = document.getElementById("messageInput");

    let message = input.value;

    if (message.trim() !== "") {

        // Send message to server
        socket.send(message);

        // Clear input
        input.value = "";
    }
}

// Receive messages from server
socket.on('message', function(message) {

    let messagesDiv = document.getElementById("messages");

    let newMessage = document.createElement("div");

    newMessage.classList.add("message");

    newMessage.innerText = message;

    messagesDiv.appendChild(newMessage);

    // Auto scroll
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});