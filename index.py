from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
messages = []

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>LiteGram Web</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { background-color: #1d1121; color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        .header { background-color: #26182c; padding: 15px; text-align: center; font-weight: bold; font-size: 20px; color: #b279e6; border-bottom: 2px solid #3a2a41; }
        .chat-box { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .message { background-color: #3a2a41; padding: 10px 15px; border-radius: 15px; max-width: 85%; align-self: flex-start; word-wrap: break-word; }
        .footer { background-color: #26182c; padding: 10px; display: flex; gap: 8px; border-top: 2px solid #3a2a41; }
        input { background: #1d1121; border: 1px solid #4a3a51; color: white; padding: 10px; border-radius: 20px; outline: none; font-size: 16px; }
        .btn { background-color: #b279e6; border: none; color: white; padding: 10px 20px; border-radius: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">LiteGram Web</div>
    <div id="chat" class="chat-box"></div>
    <div class="footer">
        <input type="text" id="user" placeholder="Имя" style="width: 70px;">
        <input type="text" id="text" placeholder="Сообщение..." style="flex: 1;">
        <button onclick="sendMsg()" class="btn">➤</button>
    </div>

    <script>
        async function loadMsgs() {
            const res = await fetch('/get_messages');
            const data = await res.json();
            const chat = document.getElementById('chat');
            chat.innerHTML = data.map(m => `<div class="message"><b>${m.user}:</b>
${m.text}</div>`).join('');
            chat.scrollTop = chat.scrollHeight;
        }

        async function sendMsg() {
            const user = document.getElementById('user').value;
            const text = document.getElementById('text').value;
            if(!user || !text) return;
            await fetch('/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user, text})
            });
            document.getElementById('text').value = '';
            loadMsgs();
        }

        setInterval(loadMsgs, 2000); // Проверять новые сообщения каждые 2 секунды
        loadMsgs();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_UI)

@app.route("/get_messages")
def get_messages():
    return jsonify(messages)

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    if data.get("user") and data.get("text"):
        messages.append(data)
        if len(messages) > 50: messages.pop(0)
    return jsonify({"status": "ok"})
