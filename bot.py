import telebot
from telebot import types
from collections import deque
from dataclasses import dataclass
token="6851790018:AAFmSMFLj0VQr5xLkxSWk_lC45Fb7__RL48"
chanel_name = "test_talks_chanel"
admins = ["arduinoev3", "derskov"]

@dataclass
class User:
    id: int
    step: int = 0
    name: str
    first: str
    last: str
    phone: str

m = dict()

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    global m
    m[message.from_user.username] = User(id=message.chat.id, name=message.from_user.username, first=message.from_user.first_name, last=message.from_user.last_name, phone=None)
    bot.send_message(message.chat.id, f"Привет! Напиши, пожалуйста, свой номер телефона")

@bot.message_handler(commands=['get'])
def start_message(message):
    global m, admins
    if message.from_user.username in admins:
        bot.send_message(message.chat.id, "\n".join([m[it].__repr__() for it in m]))

@bot.message_handler(commands=['check_subscription'])
def check_subscription(message):
    global chanel_name
    user_id = message.chat.id
 
    try:
        member = bot.get_chat_member("@" + chanel_name, user_id)
        if member.status == 'member' or member.status == 'creator':
            bot.reply_to(message, 'Вы подписаны на канал')
        else:
            bot.reply_to(message, 'Вы не подписаны на канал')
    except Exception as e:
        bot.reply_to(message, str(e))

@bot.message_handler()
def start_message(message):
    global m
    if message.from_user.username in m:
        if m[message.from_user.username].step == 0:
            m[message.from_user.username].phone = message.text
            m[message.from_user.username].step = 1
            bot.send_message(m[message.from_user.username].id, "Еще раз приветсвую - зацени https://publictalk.rbc.ru. (Если хочешь получить в подарок финансовый дневник, то подписывайся на канал)")
        else:
            pass
    else:
        bot.send_message(message.chat.id, "Тебя не в игре - введи /start")



bot.infinity_polling()