from flask import Flask, render_template_string, request

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
        .header { background-color: #26182c; padding: 20px; text-align: center; font-weight: bold; font-size: 22px; color: #b279e6; border-bottom: 2px solid #3a2a41; }
        .chat-box { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; }
        .message { background-color: #3a2a41; padding: 12px; border-radius: 15px; margin-bottom: 10px; max-width: 85%; align-self: flex-start; line-height: 1.4; }
        .footer { background-color: #26182c; padding: 15px; display: flex; gap: 10px; border-top: 2px solid #3a2a41; }
        input { background: #1d1121; border: 1px solid #4a3a51; color: white; padding: 12px; border-radius: 25px; outline: none; font-size: 16px; }
        .btn { background-color: #b279e6; border: none; color: white; padding: 12px 25px; border-radius: 25px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">LiteGram Web</div>
    <div class="chat-box" id="chat">
        {% for msg in msgs %}
            <div class="message"><b>{{ msg.user }}:</b>
{{ msg.text }}</div>
        {% endfor %}
    </div>
    <form class="footer" method="POST">
        <input type="text" name="user" placeholder="Имя" required style="width: 70px;">
        <input type="text" name="text" placeholder="Сообщение..." required style="flex: 1;">
        <button type="submit" class="btn">➤</button>
    </form>
    <script>
        var chat = document.getElementById('chat');
        chat.scrollTop = chat.scrollHeight;
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user = request.form.get("user")
        text = request.form.get("text")
        if user and text:
            messages.append({"user": user, "text": text})
            if len(messages) > 50: messages.pop(0) # Храним только последние 50
    return render_template_string(HTML_UI, msgs=messages)

# Важно для Vercel
app.debug = False
