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

    bot.send_message(message.chat.id, f"""Привет!\n
Мы — команда Конференции <a href="https://businessclass.rbc.ru">Предпринимательский класс 2.0</a>, площадкb, где опытные предприниматели делятся реальными кейсами, стратегиями и инсайтами, а участники задают им вопросы, обсуждают проблемы и вызовы в своем бизнесе.\n
Хотим пригласить тебя на БЕСПЛАТНОЕ мероприятие Business Talk - это открытый диалог с предпринимателями на тему “Строим планы на год: как разработать систему и когда отходить от плана?”. Обсудим:\n
1) Как правильно планировать?
2) Как предпринимателю работать с сезонностью?
3) Постановка целей и задач на год. На что рассчитывать в 2024 году?
4) Предиктивная модель бизнеса: как внедрить ее в жизнь?
5) Реактивная модель: как и когда нужно отходить от плана в бизнесе?

Для присоединения в наш чат введи почту;""", 
                     disable_web_page_preview=True, parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
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
                if "@" in message.text:
                    bot.send_message(message.chat.id, f"А теперь телефон")
                    
                    df.loc[df[df.id == message.chat.id].index[0], "email"] = message.text
                    backup()

                    df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                else:
                    bot.send_message(message.chat.id, "Какая-то ошибка, напиши почту еще раз")
            case 1:
                num = list(filter(lambda x: x in set(map(str, range(0, 10))), message.text))
                number = "".join(num)
                if 10 <= len(number) <= 11:
                    markup = types.ReplyKeyboardMarkup()
                    inning = types.KeyboardButton("Вступил")
                    markup.add(inning)
                    bot.send_message(message.chat.id, f"И теперь группа https://t.me/{check_name}", reply_markup=markup)
                    
                    df.loc[df[df.id == message.chat.id].index[0], "summa"] = int(number)
                    backup()

                    df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                else:
                    bot.send_message(message.chat.id, "Какая-то ошибка, напиши почту еще раз")
            case 2:
                try:
                    member = bot.get_chat_member("@" + check_name, message.chat.id)
                    if member.status == 'member' or member.status == 'creator':

                        bot.reply_to(message, """Круто! Еще раз напомню о мероприятии <a href="https://businessclass.rbc.ru">Предпринимательский класс 2.0</a>""", parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())

                        df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                    else:
                        bot.reply_to(message, f'Вы не с нами, залетайте https://t.me/{check_name}')
                except Exception as e:
                    logs(str(e))
            case _:
                bot.send_message(message.chat.id, "Давай попробуем сначала /start")
    else:
        bot.send_message(message.chat.id, "Ты не в игре - жми /start")



bot.polling(none_stop=True)