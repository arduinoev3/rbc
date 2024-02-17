import telebot
from telebot import types
from collections import deque
from dataclasses import dataclass
import os
from io import BytesIO
from sys import argv
from param import token, check_name
import pandas as pd
import time

backup_id = 5677083753

try:
    df = pd.read_csv("data.csv", index_col=False)
    df.to_csv("data.csv", index=False)
except:
    df = pd.DataFrame([{"id": 823859678, "step": 0, "name": "arduinoev3", "first": "🎩Игорь", "last": "ФБВоТ Повезло", "premium": True, "summa": 0, "email": "v2072211@yandex.ru"}])
bot = telebot.TeleBot(token)

def backup():
    global backup_id
    df.to_csv("data.csv", index=False)
    f = open("data.csv","rb")
    bot.send_document(backup_id, f)

def logs(s):
    print(s)
    bot.send_message(-1002079028053, s)

@bot.message_handler(commands=['start'])
def start_message(message):
    global df

    backup()
    logs(f"#1 {message.from_user.username} {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.is_premium}")

    if message.chat.id in list(df.id):
        df.loc[df[df.id == message.chat.id].index[0], "step"] = 0
    else:
        prem = True if message.from_user.is_premium == "True" else False
        df_for_add = pd.DataFrame([{"id": message.chat.id, "step": 0, "name": message.from_user.username, "first": message.from_user.first_name, "last": message.from_user.last_name, "premium": prem, "summa": 0, "email": None}])
        df = df._append(df_for_add, ignore_index = True)
    
    markup = types.ReplyKeyboardMarkup()
    inning = types.KeyboardButton("Вступил")
    markup.add(inning)

    bot.send_message(message.chat.id, f"""Добро пожаловать в бизнес-сообщество Предпринимательский Класс 2.0 от РБК.\n
<a href="https://t.me/biz_rbc_chat">Присоединяйся к остальным предпринимателям в Telegram-чате</a>:\n
- Получай ценные и практичные советы от опытных бизнесменов.
- Обсуждай стратегии, инсайты и делись опытом.
- Будь в кругу единомышленников и заводи полезные связи.\n
<b>Ссылка на вступление в сообщество:</b> <a href="https://t.me/biz_rbc_chat">https://t.me/biz_rbc_chat</a>""", 
                     disable_web_page_preview=True, parse_mode="HTML", reply_markup=markup)
    time.sleep(0.3)

def write_question(message, q, ans):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[types.KeyboardButton(i) for i in ans])

    bot.send_message(message.chat.id, q, reply_markup=markup, parse_mode="HTML")

@bot.message_handler()
def start_message(message):
    global df, N
    count = 0
    if message.text == "/jVGa4xX3":
        for i in range(1019 + 1, len(df)):
            if df.name[i] in {"katkolodeznikova", "tanya_markevich"}:
                continue
            try:
                bot.send_message(df.id[i], """""", parse_mode="HTML", disable_web_page_preview=True)
                count += 1
                logs(f"send {df.id[i]} {count}")
                time.sleep(0.2)
            except:
                pass
    elif message.chat.id in list(df.id):
        match df[df.id == message.chat.id].step.item():
            case 0:
                try:
                    
                    member = bot.get_chat_member("@" + check_name, message.chat.id)
                    if member.status == 'member' or member.status == 'creator':
                        bot.send_message(message.chat.id, """Приглашаем на встречу с предпринимателями 03.03 в формате Business Talk.\n
💡Опытные предприниматели поделятся своим опытом развития бизнеса и ответят на вопросы.\n
💰Используйте шанс прикоснуться к опыту единомышленников и получить ценные ответы на свои вопросы.\n
Для участия напиши ответным сообщением свой email.""", parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
                        df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                    else:
                        bot.reply_to(message, f'Вы не с нами, залетайте https://t.me/{check_name}')
                except Exception as e:
                    logs(str(e))
            case 1:
                if "@" in message.text:
                    bot.reply_to(message, f"Вы зарегистрированы на открытый диалог 3 марта! Добавьте 03.03 в календарь. Ждём вас в Центре Событий РБК!")
                    bot.send_message(message.chat.id, """30 марта мы организуем большую конференцию «Предпринимательский Клас 2.0». Следите за новостями в чате! 

️Опытные предприниматели поговорят про:

➖ Прогноз рынка на 2024 год: как себя чувствует рынок?
➖ Когда личный бренд помогает, а когда мешает бизнесу?
➖ Как выйти на Мосбиржу и привлечь миллиарды? 
➖ У тебя есть 1 млрд. Что дальше?
➖ Как реорганизовать брендинг под зумеров?
➖ Как выйти с русским продуктом на Amazon?
​​➖ Диверсификация активов: куда вкладывать деньги?
➖ Как находить инвестиции для бизнеса?
➖ Связь между бизнесом и образованием?
➖ Как заработать на Телеграме?

Построй свой эффективный бизнес — <a href="https://businessclass.rbc.ru/"><b>регистрируйся на большую конференцию предпринимателей!</b></a>

Следите за обновлениями программы в чате!""", parse_mode="HTML")
                    
                    df.loc[df[df.id == message.chat.id].index[0], "email"] = message.text
                    backup()

                    df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                else:
                    bot.send_message(message.chat.id, "Какая-то ошибка, напиши почту еще раз")
            case _:
                bot.send_message(message.chat.id, "Давай попробуем сначала /start")
    else:
        bot.send_message(message.chat.id, "Ты не в игре - жми /start")



bot.polling(none_stop=True)