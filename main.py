import telebot
import os
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running via webhook!", 200

@app.route(f"/{TOKEN}", methods=['POST'])
def receive_update():
    json_data = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "ok", 200

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, "Bot aktif dan jalan lancar pakai webhook!")

if __name__ == "__main__":
    DOMAIN = os.getenv("RAILWAY_DOMAIN")  # contoh: alert-presence.up.railway.app
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{DOMAIN}/{TOKEN}")
    app.run(host="0.0.0.0", port=8000)
