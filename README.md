<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lobby</title>
    <style>
        body {
            font-family: serif;
            background-color: #222;
            margin: 0;
            padding: 0;
        }

        .background-video {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }

        .chat-container {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            width: 100%;
            height: 100%;
            font-size: 20px;
            color: #fff;
        }

        .chat-header {
            background-color: rgb(130, 34, 34);
            padding: 10px;
            text-align: center;
            color: #fff;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1;
        }

        .chat-messages {
            flex: 1;
            min-height: 33rem;
            overflow-y: auto;
            position: relative;
            top: 2rem;
            padding: 10px;
            bottom: 1.5rem;
            padding-top: 5rem;
            /* Ensures no overlap with the header */
            padding-bottom: 4rem;
            /* Prevents overlap with the input */
            background-color: rgba(0, 0, 0, 0.8);
        }

        .chat-message {
            margin-bottom: 10px;
            font-size: 1.2rem;
            font-family: serif;
        }

        .sent {
            text-align: left;
        }

        .received {
            text-align: right;
        }

        .chat-input {
            position: fixed;
            bottom: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background-color: #111010;
            z-index: 1;
        }

        .chat-input input {
            flex: 1;
            width: 60rem;
            height: 2.5rem;
            border-radius: 10px;
            padding: 5px 10px;
            font-family: serif;
            border: 2px solid white;
            font-size: 1rem;
            color: #fff;
            background-color: rgba(0, 0, 0, 0.7);
        }

        .chat-input button {
            width: 5rem;
            height: 3rem;
            border-radius: 10px;
            color: white;
            font-size: 1.2rem;
            font-family: serif;
            background-color: rgb(147, 43, 43);
            border: none;
            cursor: pointer;
        }

        .chat-input button:hover {
            background-color: rgb(95, 27, 27);
        }

        @media screen and (max-width: 768px) {
            .chat-input input {
                font-size: 0.9rem;
            }

            .chat-input button {
                font-size: 0.9rem;
            }
        }
    </style>
</head>

<body>
    <video class="background-video" muted loop autoplay playsinline>
        <source src="/static/ALGOVisualizer.mp4" type="video/mp4">
    </video>

    <div class="chat-container">
        <div class="chat-header">
            <h1>Welcome to room {{room_name}}!</h1>
            <h2 id="member-count"></h2>
        </div>

        <div class="chat-messages" id="messages">
            <!-- Chat messages will appear here dynamically -->
        </div>

    </div>
    <footer>
        <div class="chat-input">
            <form id="form">
                <input type="text" id="textinput" name="message" placeholder="Type your message..." autocomplete="off">
                <button type="submit">Send</button>
            </form>
        </div>
    </footer>
    <script type="text/javascript">
        const user_name = "{{user_name}}";
        const lobbycode = "{{lobbycode}}";

        // WebSocket setup
        const url = `ws://${window.location.host}/ws/socket-server/${lobbycode}/`;
        const chatSocket = new WebSocket(url);

        const messagesContainer = document.getElementById('messages');
        const memberCountDisplay = document.getElementById('member-count');
        const form = document.getElementById('form');

        // Scroll to the bottom of the chat
        function scrollToBottom() {
            setTimeout(() => {
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }, 0); // Delay to ensure DOM updates are complete
        }

        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);

            if (data.type === 'member_count') {
                memberCountDisplay.textContent = `Members: ${data.member}`;
                return;
            }

            if (data.type === 'chat') {
                const messageClass = data.user_name === user_name ? 'received' : 'sent';
                const userDisplay = data.user_name === user_name ? 'You' : data.user_name;

                const messageElement = `
                    <div class="chat-message ${messageClass}">
                        <p><strong>${userDisplay}:</strong> ${data.message}</p>
                    </div>
                `;

                messagesContainer.insertAdjacentHTML('beforeend', messageElement);
                scrollToBottom();
            }
        };

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const input = e.target.message.value.trim();
            if (input === '') return;

            chatSocket.send(JSON.stringify({
                message: input,
                user_name: user_name
            }));

            form.reset();
        });

        // Ensure the chat is scrolled to the bottom on load
        scrollToBottom();
    </script>
</body>

</html>
