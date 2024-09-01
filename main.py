import os
from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("مرحبا"), KeyboardButton("كيف حالك؟"))
    bot.reply_to(message, "أهلا بك! كيف يمكنني مساعدتك؟", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "مرحبا":
        bot.reply_to(message, "مرحبا بك! كيف يمكنني مساعدتك اليوم؟")
    elif message.text == "كيف حالك؟":
        bot.reply_to(message, "أنا بخير، شكراً لسؤالك! كيف يمكنني مساعدتك؟")
    else:
        bot.reply_to(message, "عذراً، لم أفهم طلبك. هل يمكنك توضيحه؟")

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your-app-name.vercel.app/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
