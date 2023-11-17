import telebot
from telebot import types
from collections import deque
from dataclasses import dataclass
import os
from io import BytesIO

if os.environ.get('API_KEY'):
    token = os.environ.get('API_KEY')
else:
    token="6851790018:AAFmSMFLj0VQr5xLkxSWk_lC45Fb7__RL48"
if os.environ.get('CHECK_NAME'):
    check_name = os.environ.get('CHECK_NAME')
else:
    check_name = "test_talks_group"
admins = ["arduinoev3", "derskov"]

@dataclass
class User:
    id: int
    step: int
    name: str
    first: str
    last: str
    phone: str

m = dict()

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    global m
    m[message.from_user.username] = User(id=message.chat.id, step=0, name=message.from_user.username, first=message.from_user.first_name, last=message.from_user.last_name, phone=None)
    bot.send_message(message.chat.id, f"Привет! Мы проводим https://publictalk.rbc.ru")

@bot.message_handler(commands=['get'])
def start_message(message):
    global m, admins
    if message.from_user.username in admins:
        bot.send_message(message.chat.id, "\n".join([m[it].__repr__() for it in m]))

@bot.message_handler()
def start_message(message):
    global m, check_name
    if message.from_user.username in m:
        if m[message.from_user.username].step == 0:
            m[message.from_user.username].phone = message.text
            m[message.from_user.username].step = 1
            bot.send_message(m[message.from_user.username].id, f"Если хочешь получить в подарок финансовый дневник, то присоединяйся https://t.me/{check_name}")
        else:
            user_id = message.chat.id
            try:
                member = bot.get_chat_member("@" + check_name, user_id)
                if member.status == 'member' or member.status == 'creator':
                    m[message.from_user.username].step = 2
                    bot.reply_to(message, 'Вы с нами, кидаю дневник')

                    f = open("Финансовый дневник.pdf","rb")
                    bot.send_document(message.chat.id,f)
                else:
                    bot.reply_to(message, f'Вы не с нами, залетайте https://t.me/{check_name}')
            except Exception as e:
                bot.send_message(m["arduinoev3"].id, str(e))
    else:
        bot.send_message(message.chat.id, "Тебя не в игре - введи /start")



bot.infinity_polling()