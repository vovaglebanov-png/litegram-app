from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
# Начальные чаты
chats_data = {"Общий чат": [], "Поддержка": []}

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>LiteGram Ultra</title>
    <style>
        :root { --bg: #0f0a15; --panel: #1e142a; --accent: #b279e6; --my-msg: linear-gradient(135deg, #8e2de2, #4a00e0); }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body, html { background: var(--bg); color: white; font-family: sans-serif; margin: 0; height: 100%; overflow: hidden; }
        #app { display: flex; flex-direction: column; height: 100vh; }

        .header { background: var(--panel); padding: 15px; border-bottom: 1px solid rgba(178,121,230,0.2); display: flex; align-items: center; justify-content: space-between; }
        
        .chat-list { flex: 1; overflow-y: auto; }
        .list-item { padding: 15px; border-bottom: 1px solid #26182c; display: flex; align-items: center; gap: 15px; }
        .avatar { width: 45px; height: 45px; background: var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }

        #chat-content { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .m { padding: 10px 15px; border-radius: 15px; max-width: 85%; align-self: flex-start; background: #26182c; word-wrap: break-word; }
        .m.me { align-self: flex-end; background: var(--my-msg); }
        .u { font-size: 11px; color: var(--accent); font-weight: bold; margin-bottom: 3px; display: block; }

        .footer { background: var(--panel); padding: 10px; display: flex; gap: 10px; border-top: 1px solid #3a2a41; }
        input { flex: 1; background: #0f0a15; border: 1px solid #3a2a41; color: white; padding: 12px; border-radius: 20px; outline: none; font-size: 16px; }
        
        /* КНОПКА ПЛЮС */
        .fab { position: fixed; bottom: 30px; right: 20px; width: 60px; height: 60px; background: var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 35px; box-shadow: 0 4px 20px rgba(0,0,0,0.6); z-index: 10; cursor: pointer; }

        /* МОДАЛЬНОЕ ОКНО */
        #modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: none; align-items: center; justify-content: center; z-index: 100; }
        .modal-content { background: var(--panel); padding: 25px; border-radius: 20px; width: 85%; text-align: center; border: 1px solid var(--accent); }
        
        .hidden { display: none !important; }
    </style>
</head>
<body>
    <div id="app">
        <!-- ГЛАВНЫЙ ЭКРАН -->
        <div id="main-screen" style="display: flex; flex-direction: column; height: 100%;">
            <div class="header"><b style="color:var(--accent); font-size: 20px;">LiteGram</b></div>
            <div class="chat-list" id="chat-list-ui"></div>
            <div class="fab" onclick="showModal()">+</div>
        </div>

        <!-- ОКНО ЧАТА -->
        <div id="chat-screen" class="hidden" style="flex-direction: column; height: 100%;">
            <div class="header">
                <span onclick="goBack()" style="font-size: 18px; color: var(--accent);">← Назад</span>
                <b id="chat-title"></b>
                <span></span>
            </div>
            <div id="chat-content"></div>
            <div class="footer">
                <input type="text" id="msg-input" placeholder="Сообщение..." autocomplete="off">
                <button onclick="send()" style="background:none; border:none; color:var(--accent); font-size:28px;">➤</button>
            </div>
        </div>
    </div>

    <!-- ОКНО СОЗДАНИЯ ЧАТА -->
    <div id="modal" onclick="hideModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()"


>
            <h3>Новый чат</h3>
            <input type="text" id="new-chat-name" placeholder="Имя друга..." style="width: 100%; margin-bottom: 15px;">
            <button onclick="confirmNewChat()" style="background:var(--accent); color:white; border:none; padding:12px 30px; border-radius:20px; width: 100%; font-weight:bold;">Создать</button>
        </div>
    </div>

    <script>
        let currentChat = "";
        let myName = localStorage.getItem('my_name') || "";

        if(!myName) {
            setTimeout(() => {
                const name = prompt("Введите ваше имя:");
                if(name) { myName = name; localStorage.setItem('my_name', name); }
                else { myName = "Гость"; }
            }, 500);
        }

        async function loadChatList() {
            const r = await fetch('/get_all_chats');
            const chats = await r.json();
            document.getElementById('chat-list-ui').innerHTML = chats.map(name => `
                <div class="list-item" onclick="openChat('${name}')">
                    <div class="avatar">${name[0].toUpperCase()}</div>
                    <b>${name}</b>
                </div>
            `).join('');
        }

        function showModal() { document.getElementById('modal').style.display = 'flex'; }
        function hideModal(e) { document.getElementById('modal').style.display = 'none'; }

        function confirmNewChat() {
            const name = document.getElementById('new-chat-name').value.trim();
            if(name) {
                hideModal();
                openChat(name);
                document.getElementById('new-chat-name').value = "";
            }
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
            if(!input.value || !currentChat) return;
            await fetch('/send_msg', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({chat: currentChat, u: myName, t: input.value})
            });
            input.value = "";
            loadMsgs();
        }

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
