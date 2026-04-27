from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
# База данных сообщений в памяти сервера
db = {"777": [{"u": "Система", "t": "Добро пожаловать в LiteGram!"}]}

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>LiteGram Online</title>
    <style>
        :root { --bg: #0f0a15; --panel: #1e142a; --accent: #b279e6; }
        body { background: var(--bg); color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        .header { background: var(--panel); padding: 15px; text-align: center; border-bottom: 1px solid var(--accent); font-weight: bold; color: var(--accent); }
        
        #login-screen { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 15px; }
        #chat-screen { flex: 1; display: none; flex-direction: column; overflow: hidden; }
        
        input { background: #1e142a; border: 1px solid #b279e6; color: white; padding: 12px; border-radius: 12px; width: 80%; max-width: 300px; outline: none; font-size: 16px; }
        button { background: var(--accent); border: none; color: white; padding: 12px 25px; border-radius: 12px; font-weight: bold; cursor: pointer; }

        #messages { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .msg { background: #1e142a; padding: 10px 15px; border-radius: 15px; max-width: 85%; align-self: flex-start; border: 1px solid #3a2a41; }
        .me { align-self: flex-end; background: var(--accent); border: none; }
        
        .footer { background: #1e142a; padding: 10px; display: flex; gap: 10px; border-top: 1px solid #3a2a41; }
        .footer input { flex: 1; }
    </style>
</head>
<body>
    <div class="header">LITEGRAM</div>

    <div id="login-screen">
        <input type="text" id="username" placeholder="Ваше имя">
        <input type="text" id="roomid" placeholder="Номер комнаты (напр. 777)">
        <button onclick="enterChat()">Войти в чат</button>
    </div>

    <div id="chat-screen">
        <div id="messages"></div>
        <div class="footer">
            <input type="text" id="msg-input" placeholder="Сообщение..." onkeypress="if(event.key=='Enter')send()">
            <button onclick="send()">➤</button>
        </div>
    </div>

    <script>
        let currentUser = localStorage.getItem('u') || "";
        let currentRoom = "";

        if(currentUser) document.getElementById('username').value = currentUser;

        function enterChat() {
            currentUser = document.getElementById('username').value;
            currentRoom = document.getElementById('roomid').value;
            if (currentUser && currentRoom) {
                localStorage.setItem('u', currentUser);
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('chat-screen').style.display = 'flex';
                setInterval(load, 2000);
                load();
            }
        }

        async function load() {
            const r = await fetch('/get?r=' + encodeURIComponent(currentRoom));
            const data = await r.json();
            const div = document.getElementById('messages');
            div.innerHTML = data.map(m => `
                <div class="msg ${m.u === currentUser ? 'me' : ''}">
                    <small style="font-size:10px; opacity:0.7">${m.u}</small>
${m.t}
                </div>
            `).join('');
            div.scrollTop = div.scrollHeight;
        }

        async function send() {
            const inp = document.getElementById('msg-input');
            const text = inp.value;
            if (!text) return;
            inp.value = "";
            await fetch('/send', {
                method: 'POST',
                headers: {'Conten


t-Type': 'application/json'},
                body: JSON.stringify({ r: currentRoom, u: currentUser, t: text })
            });
            load();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/get')
def get_messages():
    r = request.args.get('r')
    return jsonify(db.get(r, []))

@app.route('/send', methods=['POST'])
def send():
    d = request.json
    r = d.get('r')
    if r not in db: db[r] = []
    db[r].append({"u": d['u'], "t": d['t']})
    if len(db[r]) > 50: db[r].pop(0)
    return jsonify({"ok": True})
