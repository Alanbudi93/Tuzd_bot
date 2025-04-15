import telebot
import os
from flask import Flask, request

API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, "Bot aktif di Railway pakai Webhook!")

@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def index():
    return "Bot is running on Railway!", 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'https://{os.environ["RAILWAY_DOMAIN"]}/{API_TOKEN}')
    app.run(host='0.0.0.0', port=8000)
