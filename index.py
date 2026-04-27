from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# В реальности сообщения на Vercel без БД живут недолго. 
# Но мы оптимизировали код для лучшей стабильности.
messages = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { background: #1d1121; color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        #chat { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .m { background: #3a2a41; padding: 12px; border-radius: 12px; max-width: 85%; align-self: flex-start; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .f { background: #26182c; padding: 15px; display: flex; gap: 8px; border-top: 1px solid #3a2a41; }
        input { background: #1d1121; border: 1px solid #4a3a51; color: white; padding: 12px; border-radius: 20px; font-size: 16px; outline: none; }
        button { background: #b279e6; color: white; border: none; padding: 10px 20px; border-radius: 20px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div style="background:#26182c; padding:15px; text-align:center; color:#b279e6; font-weight:bold; font-size:18px;">LiteGram Web</div>
    <div id="chat"></div>
    <div class="f">
        <input type="text" id="u" placeholder="Имя" style="width: 70px;">
        <input type="text" id="t" placeholder="Сообщение..." style="flex: 1;">
        <button onclick="send()">➤</button>
    </div>
    <script>
        // Сохраняем имя в памяти телефона, чтобы не вводить каждый раз
        if(localStorage.getItem('my_name')) {
            document.getElementById('u').value = localStorage.getItem('my_name');
        }

        async function load() {
            try {
                const r = await fetch('/msgs');
                const d = await r.json();
                const chat = document.getElementById('chat');
                chat.innerHTML = d.map(m => `<div class="m"><b>${m.u}:</b>
${m.t}</div>`).join('');
                chat.scrollTop = chat.scrollHeight;
            } catch(e) { console.log("Ошибка загрузки"); }
        }

        async function send() {
            const u = document.getElementById('u').value;
            const t = document.getElementById('t').value;
            if(!u || !t) return;
            
            localStorage.setItem('my_name', u); // Запоминаем имя

            await fetch('/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({u, t})
            });
            document.getElementById('t').value = '';
            load();
        }
        setInterval(load, 3000);
        load();
    </script>
</body>
</html>
"""

@app.route('/')
def i(): return render_template_string(HTML)

@app.route('/msgs')
def g(): return jsonify(messages)

@app.route('/send', methods=['POST'])
def s():
    data = request.json
    if data: 
        messages.append(data)
        # Ограничиваем список, чтобы сервер не падал
        if len(messages) > 100: messages.pop(0)
    return jsonify(ok=True)
