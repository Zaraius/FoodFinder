document.addEventListener("DOMContentLoaded", function () {
    const userInput = document.getElementById("user-input");
    const chatbox = document.getElementById("chatbox");
    const sendButton = document.getElementById("send");

    function addMessageToChatbox(message, isUser = false) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message");

        if (isUser) {
            messageElement.classList.add("user-message");
        } else {
            messageElement.classList.add("bot-message");
        }

        messageElement.innerHTML = message.replace(/\n/g, "<br>");
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function getBotResponse(userMessage) {
        fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ query: userMessage }),
        })
            .then((response) => response.json())
            .then((data) => {
                const botResponse = data.response || "Oops! No response.";
                setTimeout(() => addMessageToChatbox(botResponse, false), 1000);
            })
            .catch((error) => console.error("Error fetching response:", error));
    }

    sendButton.addEventListener("click", () => {
        const userMessage = userInput.value.trim();
        if (userMessage) {
            addMessageToChatbox(userMessage, true);
            userInput.value = "";
            getBotResponse(userMessage);
        }
    });

    addMessageToChatbox("What are you craving today?", false);
});
