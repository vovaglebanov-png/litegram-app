from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
# Теперь храним сообщения для каждого чата отдельно
chats_data = {
    "Общий чат": [],
    "Поддержка": [{"u": "Бот", "t": "Привет! Чем помочь?"}]
}

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>LiteGram MultiChat</title>
    <style>
        :root { --bg: #0f0a15; --panel: #1e142a; --accent: #b279e6; --my-msg: linear-gradient(135deg, #8e2de2, #4a00e0); }
        body { background: var(--bg); color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        .header { background: var(--panel); padding: 15px; text-align: center; border-bottom: 1px solid rgba(178,121,230,0.2); display: flex; justify-content: space-between; align-items: center; }
        .header b { color: var(--accent); font-size: 18px; }
        
        #main-screen, #chat-screen { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
        .list-item { padding: 15px; border-bottom: 1px solid #26182c; display: flex; align-items: center; gap: 15px; cursor: pointer; }
        .avatar { width: 45px; height: 45px; background: #3a2a41; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: var(--accent); }
        
        #chat-content { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .m { padding: 10px 15px; border-radius: 15px; max-width: 80%; align-self: flex-start; background: #26182c; position: relative; }
        .m.me { align-self: flex-end; background: var(--my-msg); }
        .u { font-size: 10px; color: var(--accent); margin-bottom: 4px; display: block; }
        .me .u { color: #eee; }

        .footer { background: var(--panel); padding: 10px; display: flex; gap: 10px; align-items: center; }
        input { flex: 1; background: #0f0a15; border: 1px solid #3a2a41; color: white; padding: 12px; border-radius: 20px; outline: none; }
        .btn-send { background: var(--accent); border: none; width: 40px; height: 40px; border-radius: 50%; color: white; font-weight: bold; }
        
        .hidden { display: none !important; }
    </style>
</head>
<body>
    <!-- ЭКРАН СПИСКА ЧАТОВ -->
    <div id="main-screen">
        <div class="header"><b>LiteGram</b> <span>🔍</span></div>
        <div style="padding: 10px; color: grey; font-size: 12px;">ВАШИ ЧАТЫ</div>
        <div id="chat-list">
            <div class="list-item" onclick="openChat('Общий чат')">
                <div class="avatar">ОЧ</div>
                <div><b>Общий чат</b>
<small style="color:grey">Напишите что-нибудь...</small></div>
            </div>
            <div class="list-item" onclick="openChat('Поддержка')">
                <div class="avatar">П</div>
                <div><b>Поддержка</b>
<small style="color:grey">Бот: Привет! Чем помочь?</small></div>
            </div>
        </div>
    </div>

    <!-- ЭКРАН ПЕРЕПИСКИ -->
    <div id="chat-screen" class="hidden">
        <div class="header">
            <span onclick="goBack()" style="cursor:pointer">←</span>
            <b id="chat-title">Чат</b>
            <span>⋮</span>
        </div>
        <div id="chat-content"></div>
        <div class="footer">
            <input type="text" id="msg-input" placeholder="Сообщение...">
            <button class="btn-send" onclick="send()">➤</button>
        </div>
    </div>

    <script>
        let currentChat = "";
        let myName = localStorage.getItem('my_name') || prompt("Введите ваше имя:") || "Гость";
        localStorage.setItem('my_name', myName);

        function openChat(name) {
            currentChat = name;
            document.getElementById('chat-title').innerText = name;
            document.getElementById('main-screen').classList.add


('hidden');
            document.getElementById('chat-screen').classList.remove('hidden');
            loadMsgs();
        }

        function goBack() {
            document.getElementById('main-screen').classList.remove('hidden');
            document.getElementById('chat-screen').classList.add('hidden');
            currentChat = "";
        }

        async function loadMsgs() {
            if(!currentChat) return;
            const r = await fetch(`/get_msgs?chat=${currentChat}`);
            const d = await r.json();
            const cont = document.getElementById('chat-content');
            cont.innerHTML = d.map(m => {
                const isMe = m.u === myName ? 'me' : '';
                return `<div class="m ${isMe}"><span class="u">${m.u}</span>${m.t}</div>`;
            }).join('');
            cont.scrollTop = cont.scrollHeight;
        }

        async function send() {
            const input = document.getElementById('msg-input');
            if(!input.value || !currentChat) return;
            await fetch('/send_msg', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({chat: currentChat, u: myName, t: input.value})
            });
            input.value = "";
            loadMsgs();
        }

        setInterval(loadMsgs, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/get_msgs')
def get_msgs():
    chat = request.args.get('chat')
    return jsonify(chats_data.get(chat, []))

@app.route('/send_msg', methods=['POST'])
def send_msg():
    data = request.json
    chat = data.get('chat')
    if chat in chats_data:
        chats_data[chat].append({"u": data['u'], "t": data['t']})
    return jsonify(ok=True)
