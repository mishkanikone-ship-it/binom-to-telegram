import os
import telebot
from flask import Flask, request, abort

# Получаем настройки из переменных окружения (без хардкода токенов)
TOKEN = os.environ.get("TG_BOT_TOKEN")
CHAT_ID = os.environ.get("TG_CHAT_ID")
SECRET = os.environ.get("BINOM_SECRET", "my_super_secret")

if not TOKEN or not CHAT_ID:
    raise SystemExit("Set TG_BOT_TOKEN and TG_CHAT_ID in environment variables")

bot = telebot.TeleBot(TOKEN)
app = Flask(name)

@app.route('/', methods=['GET'])
def home():
    return "Binom → Telegram is running.", 200

@app.route('/lead', methods=['POST'])
def receive_lead():
    # необязательная проверка секретного параметра в URL: /lead?secret=...
    secret = request.args.get("secret", "")
    if secret != SECRET:
        abort(403)

    # Binom может слать form-data или json
    data = request.form.to_dict() or request.get_json(silent=True) or {}
    if not data:
        return "no data", 400

    # Формируем текст сообщения
    lines = ["📥 Новый лид из Binom"]
    for k, v in data.items():
        lines.append(f"{k}: {v}")
    msg = "\n".join(lines)

    # Отправляем в Telegram
    bot.send_message(CHAT_ID, msg)
    return "ok", 200

if name == "main":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
