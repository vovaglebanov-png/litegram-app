from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
messages = []

# Дизайн как в ТГ
HTML_UI = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LiteGram Online</title>
    <style>
        body { background-color: #1d1121; color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { background-color: #26182c; padding: 15px; text-align: center; color: #b279e6; font-weight: bold; border-bottom: 1px solid #3a2a41; }
        .chat { flex: 1; overflow-y: auto; padding: 15px; }
        .msg { background: #3a2a41; padding: 10px; border-radius: 12px; margin-bottom: 8px; max-width: 80%; width: fit-content; }
        .footer { background: #26182c; padding: 10px; display: flex; gap: 10px; }
        input { flex: 1; padding: 12px; border-radius: 20px; border: none; background: #1d1121; color: white; outline: none; }
        button { background: #b279e6; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">LiteGram Web</div>
    <div class="chat" id="chat">
        {% for m in msgs %}
            <div class="msg"><b>{{ m.user }}:</b> {{ m.text }}</div>
        {% endfor %}
    </div>
    <form class="footer" method="POST">
        <input type="text" name="user" placeholder="Имя" required style="width: 60px; flex: none;">
        <input type="text" name="text" placeholder="Сообщение..." required>
        <button type="submit">➤</button>
    </form>
    <script>document.getElementById('chat').scrollTop = 99999;</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user, text = request.form.get("user"), request.form.get("text")
        if user and text: messages.append({"user": user, "text": text})
    return render_template_string(HTML_UI, msgs=messages)

if __name__ == "__main__":
    # Порт для хостинга берется из настроек системы
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)