import telebot
from telebot import types
from collections import deque
from dataclasses import dataclass
import os
from io import BytesIO
from sys import argv
from param import token, check_name
import pandas as pd

backup_id = 5677083753

try:
    df = pd.read_csv("data.csv", index_col=False)
    df.to_csv("data.csv", index=False)
except:
    df = pd.DataFrame([{"id": [823859678], "step": [0], "name": ["arduinoev3"], "first": ["🎩Игорь"], "last": ["ФБВоТ Повезло"], "premium": [True], "summa": [0], "email": ["v2072211@yandex.ru"]},
                    {"id": 5677083753, "step": 0, "name": "bssmipt_faq", "first": "Студсовет ФБВТ", "last": "Общий аккаунт", "premium": False, "summa": 0, "email": "@", }])

bot=telebot.TeleBot(token)

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
        logs(f"search {message.from_user.username} {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.is_premium}")
        df.loc[df[df.id == message.chat.id].index[0], "step"] = 0
        df.loc[df[df.id == message.chat.id].index[0], "summa"] = 0
        logs("good search")
    else:
        prem = True if message.from_user.is_premium == "True" else False
        df_for_add = pd.DataFrame([{"id": message.chat.id, "step": 0, "name": message.from_user.username, "first": message.from_user.first_name, "last": message.from_user.last_name, "premium": prem, "summa": 0, "email": None}])
        df = df._append(df_for_add, ignore_index = True)
        
    markup = types.ReplyKeyboardMarkup()
    test = types.KeyboardButton("Пройти тест")
    markup.add(test)

    bot.send_message(message.chat.id, f"""Привет!\n
Мы подготовили руководство и дневник финансовой грамотности для вас и вашего ребёнка.\n
Мы — команда Лектория <a href="https://publictalk.rbc.ru/?utm_source=tg_bot&utm_medium=welcome">«Дети в деле» РБК</a>, семейного лектория про осознанные стратегии финансового воспитания, финансовые навыки и предпринимательское мышление.\n
Чтобы получить руководство и дневник, пройдите короткий тест и узнайте ваш уровень финансовой грамотности""", 
                     disable_web_page_preview=True, reply_to_message_id=None, reply_markup=markup, parse_mode="HTML", disable_notification=None)

def write_question(message, q, ans):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[types.KeyboardButton(i) for i in ans])

    bot.send_message(message.chat.id, q, reply_markup=markup, parse_mode="HTML")

@bot.message_handler()
def start_message(message):
    global df
    if message.chat.id in list(df.id):
        match df[df.id == message.chat.id].step.item():
            case 0:
                write_question(message, """Как вам кажется, насколько хорошо развиты у вас и ваших детей гибкие навыки, которые нужны для финансовой грамотности? Попробуйте оценить некоторые из них:\n<b>1. Получается договариваться о размере карманных денег?</b>""", 
                           ["1. получается без проблем", 
                            "2. сначала конфликтуем, но договариваемся", 
                            "3. никогда не договоримся"])
                df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
            case 1:
                if message.text[0] in ["1", "2", "3"]:
                    df.loc[df[df.id == message.chat.id].index[0], "summa"] += 4 - int(message.text[0])
                    write_question(message, """<b>2. Получается достойно оценивать результат труда?</b>""", 
                            ["1. получается без проблем", 
                                "2. сначала конфликтуем, но договариваемся", 
                                "3. никогда не договоримся"])
                    df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                else:
                    bot.reply_to(message, f'Используй кнопки')
            case 2:
                if message.text[0] in ["1", "2", "3"]:
                    df.loc[df[df.id == message.chat.id].index[0], "summa"] += 4 - int(message.text[0])
                    write_question(message, """<b>3. Можете определить действия мошенников и не попасться на удочку?</b>""", 
                            ["1. получается без проблем",
                                "2. не всегда получается",
                                "3. никогда не получается"])
                    df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                else:
                    bot.reply_to(message, f'Используй кнопки')
            case 3:
                if message.text[0] in ["1", "2", "3"]:
                    df.loc[df[df.id == message.chat.id].index[0], "summa"] += 4 - int(message.text[0])
                    write_question(message, """<b>4. Умеете ставить и достигать финансовые цели?</b>""", 
                            ["1. получается без проблем", 
                                "2. сначала конфликтуем, но договариваемся", 
                                "3. никогда не договоримся"])
                    df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                else:
                    bot.reply_to(message, f'Используй кнопки')
            case 4:
                if message.text[0] in ["1", "2", "3"]:
                    df.loc[df[df.id == message.chat.id].index[0], "summa"] += 4 - int(message.text[0])
                    write_question(message, """<b>5. Получается планировать свое время и деньги на будущее?</b>""", 
                            ["1. получается без проблем", 
                                "2. сначала конфликтуем, но договариваемся", 
                                "3. никогда не договоримся"])
                    df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                else:
                    bot.reply_to(message, f'Используй кнопки')
            case 5:
                if message.text[0] in ["1", "2", "3"]:
                    df.loc[df[df.id == message.chat.id].index[0], "summa"] += 4 - int(message.text[0])
                    markup = types.InlineKeyboardMarkup()
                    url = types.InlineKeyboardButton("Группа", url='https://t.me/{check_name}')
                    markup.add(url)
            
                    bot.send_message(message.chat.id, """Готово!
Чтобы получить результаты и дневник финансовой грамотности:
1. Напишите ответным сообщением электронную почту, на неё отправим дневник и полезные материалы
2. Вступите в нашу группу """ + f"https://t.me/{check_name}", reply_markup=types.ReplyKeyboardRemove())
                    
                    df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                else:
                    bot.reply_to(message, f'Используй кнопки')
            case 6:
                if "@" in message.text:
                    markup = types.ReplyKeyboardMarkup()
                    inning = types.KeyboardButton("Вступил")
                    markup.add(inning)
                    bot.send_message(message.chat.id, "А теперь группа", reply_markup=markup)

                    backup()
                    s = df.loc[df[df.id == message.chat.id].index[0], "summa"]
                    logs(f"#2 {message.from_user.username} {message.text} {s}")

                    df.loc[df[df.id == message.chat.id].index[0], "step"] += 1
                else:
                    bot.send_message(message.chat.id, "Какая-то ошибка, напиши почту еще раз")
            case 7:
                try:
                    member = bot.get_chat_member("@" + check_name, message.chat.id)
                    if member.status == 'member' or member.status == 'creator':
                        markup = types.ReplyKeyboardMarkup()
                        test = types.KeyboardButton("/start")
                        markup.add(test)
                        bot.reply_to(message, 'Вы с нами, кидаю дневник и результаты', reply_markup=markup)

                        f = open("Финансовый дневник.pdf","rb")
                        bot.send_document(message.chat.id,f)

                        s = df.loc[df[df.id == message.chat.id].index[0], "summa"]
                        bot.send_message(message.chat.id, f"Ваш результат {s} баллов")
                        if df.loc[df[df.id == message.chat.id].index[0], "summa"] >= 15:
                            bot.send_message(message.chat.id, f"""Здорово! У вас неплохо получается договариваться и вы легко сможете внедрить полезные привычки и инструменты, о которых эксперты по бизнесу и финансовой грамотности расскажут 25 ноября в лекции <a href="https://publictalk.rbc.ru/?utm_source=tg_bot&utm_medium=result">«Дети в деле» от РБК</a>.\n
    Регистрируйтесь и ждём в гости родителей и их будущих предпринимателей!""", parse_mode="HTML")
                        elif 9 <= df.loc[df[df.id == message.chat.id].index[0], "summa"] <= 14:
                            bot.send_message(message.chat.id, f"""Неплохо! Вы делаете важные успехи, однако всегда есть к чему стремиться, приходите послушать опыт экспертов и других родителей, которые знают всё о финансовой грамотности и подростковом бизнесе.\n
    25 ноября ждём родителей и их будущих предпринимателей на лекции <a href="https://publictalk.rbc.ru/?utm_source=tg_bot&utm_medium=result">«Дети в деле» от РБК</a>.\n
    Регистрируйтесь и ждём в гости родителей и их будущих предпринимателей!""", parse_mode="HTML")
                        else:
                            bot.send_message(message.chat.id, f"""Вам есть к чему стремиться! В любом деле главное — начать. Вам обязательно стоит послушать опыт экспертов и других родителей, которые знают всё о финансовой грамотности и подростковом бизнесе. Обещаем, что к концу лекции вы уже почувствуете изменения.\n
    25 ноября ждём родителей и их будущих предпринимателей на лекции <a href="https://publictalk.rbc.ru/?utm_source=tg_bot&utm_medium=result">«Дети в деле» от РБК</a>.\n
    Регистрируйтесь и ждём в гости родителей и их будущих предпринимателей!""", parse_mode="HTML")
                        
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