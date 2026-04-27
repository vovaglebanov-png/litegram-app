from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
chats_data = {
    "Общий чат": [],
    "Поддержка": [{"u": "Бот", "t": "Нажми '+', чтобы создать чат!"}]
}

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>LiteGram Final</title>
    <style>
        :root { --bg: #0f0a15; --panel: #1e142a; --accent: #b279e6; --my-msg: linear-gradient(135deg, #8e2de2, #4a00e0); }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        body, html { 
            background: var(--bg); color: white; font-family: sans-serif; 
            margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden;
        }

        #app { display: flex; flex-direction: column; height: 100vh; height: -webkit-fill-available; }

        .header { background: var(--panel); padding: 15px; border-bottom: 1px solid rgba(178,121,230,0.2); display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
        
        .chat-list { flex: 1; overflow-y: auto; }
        .list-item { padding: 15px; border-bottom: 1px solid #26182c; display: flex; align-items: center; gap: 15px; }
        .avatar { width: 45px; height: 45px; background: var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }

        #chat-content { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .m { padding: 10px 15px; border-radius: 15px; max-width: 85%; align-self: flex-start; background: #26182c; word-wrap: break-word; line-height: 1.4; }
        .m.me { align-self: flex-end; background: var(--my-msg); }
        .u { font-size: 11px; color: var(--accent); font-weight: bold; margin-bottom: 3px; display: block; }

        .footer { background: var(--panel); padding: 10px; border-top: 1px solid #3a2a41; display: flex; gap: 10px; align-items: center; flex-shrink: 0; }
        input { flex: 1; background: #0f0a15; border: 1px solid #3a2a41; color: white; padding: 12px; border-radius: 20px; outline: none; font-size: 16px; }
        .send-btn { background: none; border: none; color: var(--accent); font-size: 28px; cursor: pointer; padding: 0 5px; }

        .fab { position: fixed; bottom: 80px; right: 20px; width: 56px; height: 56px; background: var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .hidden { display: none !important; }
    </style>
</head>
<body>
    <div id="app">
        <!-- СПИСОК ЧАТОВ -->
        <div id="main-screen" style="display: flex; flex-direction: column; height: 100%;">
            <div class="header"><b style="color:var(--accent); font-size: 20px;">LiteGram</b></div>
            <div class="chat-list" id="chat-list-ui"></div>
            <div class="fab" onclick="createNewChat()">+</div>
        </div>

        <!-- ОКНО ЧАТА -->
        <div id="chat-screen" class="hidden" style="flex-direction: column; height: 100%;">
            <div class="header">
                <span onclick="goBack()" style="font-size: 18px; color: var(--accent); cursor:pointer;">← Назад</span>
                <b id="chat-title"></b>
                <span></span>
            </div>
            <div id="chat-content"></div>
            <div class="footer">
                <input type="text" id="msg-input" placeholder="Сообщение..." autocomplete="off">
                <button class="send-btn" id="final-send-btn" onclick="send()">➤</button>
            </div>
        </div>
    </div>

    <script>
        let currentChat = "";
        let myName = localStorage.getItem('my_name') || prompt("Имя:") || "User";
        localStorage.setItem('my_name', myName);

        async function loadChatList() {
            con


st r = await fetch('/get_all_chats');
            const chats = await r.json();
            document.getElementById('chat-list-ui').innerHTML = chats.map(name => `
                <div class="list-item" onclick="openChat('${name}')">
                    <div class="avatar">${name[0].toUpperCase()}</div>
                    <b>${name}</b>
                </div>
            `).join('');
        }

        function createNewChat() {
            const name = prompt("Имя друга:");
            if(name) openChat(name);
        }

        function openChat(name) {
            currentChat = name;
            document.getElementById('chat-title').innerText = name;
            document.getElementById('main-screen').style.display = 'none';
            document.getElementById('chat-screen').style.display = 'flex';
            loadMsgs();
        }

        function goBack() {
            document.getElementById('main-screen').style.display = 'flex';
            document.getElementById('chat-screen').style.display = 'none';
            currentChat = "";
            loadChatList();
        }

        async function loadMsgs() {
            if(!currentChat) return;
            const r = await fetch('/get_msgs?chat=' + encodeURIComponent(currentChat));
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
            const text = input.value.trim();
            if(!text || !currentChat) return;
            
            await fetch('/send_msg', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({chat: currentChat, u: myName, t: text})
            });
            input.value = "";
            loadMsgs();
        }

        // Позволяет отправлять по кнопке Enter на клавиатуре
        document.getElementById('msg-input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') send();
        });

        setInterval(() => { currentChat ? loadMsgs() : loadChatList(); }, 2000);
        loadChatList();
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/get_all_chats')
def get_all_chats(): return jsonify(list(chats_data.keys()))

@app.route('/get_msgs')
def get_msgs():
    chat = request.args.get('chat')
    if chat not in chats_data: chats_data[chat] = []
    return jsonify(chats_data[chat])

@app.route('/send_msg', methods=['POST'])
def send_msg():
    data = request.json
    chat = data.get('chat')
    if chat not in chats_data: chats_data[chat] = []
    chats_data[chat].append({"u": data['u'], "t": data['t']})
    return jsonify(ok=True)
