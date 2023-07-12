import telebot
from telebot import types

import re

import pymysql

connection = pymysql.connect(db='first_database', user='root',
                      host='localhost', password='1212313111123')
cursor = connection.cursor()

kind_news = ['cybersport', 'art', 'schedule_matches']

bot  = telebot.TeleBot("6193778513:AAG2iZsKyaxabWQtdMqoS_AHfRu6EuXDX4o", parse_mode=None)

schedules = {}

def update_schedule(dicipline):
    with open(f'schedule_matches_{dicipline}.txt', 'r') as f:
        global schedules
        schedules[dicipline] = ''.join(f.readlines())

update_schedule('cs-go')
update_schedule('dota-2')

print(schedules)
def back_keyboard(deep_lvl):
    return types.InlineKeyboardButton(
                    text='⬅',
                    callback_data=f'back_{deep_lvl}')
def list_news():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text = i,
                    callback_data = i
                )
            ] for i in kind_news
        ]
    )

def list_previews_keyboard(deep_lvl):
    cursor.execute(f"SELECT id, preview, kind_new FROM articles WHERE kind_new = '{deep_lvl[14:]}'")
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text= i[1],
                    callback_data=f"{deep_lvl}"+i[0]
                )
            ]
            for i in cursor
        ]
    )

def list_dicipline_for_matches(deep_lvl):
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text= dicipline if schedules[dicipline] != '' else f'{dicipline}(нет матчей)',
                    callback_data=f"{deep_lvl}_{dicipline}"
                )
            ]
            for dicipline in list(schedules.keys())
        ]
    )

@bot.message_handler(commands=['start'])
def start_pos(message):
    bot.send_message(message.chat.id, text=f"Привет! Какие новости желаешь узнать?", reply_markup=list_news())

@bot.callback_query_handler(func=lambda call: call.data in kind_news or call.data == 'back_2')
def callback_worker(call):
    if call.data == "cybersport":  # call.data это callback_data, которую мы указали при объявлении кнопки
    # код сохранения данных, или их обработки
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Новости киберспорта:", reply_markup=list_previews_keyboard('list_articles_Cybersport').add(back_keyboard(2)))

    elif call.data == "schedule_matches":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Дисциплины:",
                              reply_markup=list_dicipline_for_matches('schedule').add(back_keyboard(2)))
    elif call.data == "art":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Artnews", reply_markup=list_previews_keyboard('list_articles_Artnews').add(back_keyboard(2)))
    elif call.data == "back_2":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Новости", reply_markup=list_news())

@bot.callback_query_handler(func=lambda call: ("list_articles" in call.data) or call.data in ['back_3_cs', 'back_3_art'])
def list_articles_cybersport(call):
    if call.data == "back_3_cs":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Новости киберспорта", reply_markup=list_previews_keyboard('list_articles_Cybersport').add(back_keyboard(2)))

    elif call.data == "back_3_art":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Новости искусства",
                              reply_markup=list_previews_keyboard('list_articles_Artnews').add(back_keyboard(2)))
    elif 'list_articles_Artnews' in call.data:
        cursor.execute(f"SELECT text FROM content_articles WHERE id_article = '{call.data[21:]}'")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=[i for i in cursor][0],
                              reply_markup=types.InlineKeyboardMarkup().add(back_keyboard('3_art')))
    else:
        cursor.execute(f"SELECT text FROM content_articles WHERE id_article = '{call.data[24:]}'")

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=[i for i in cursor][0],
                              reply_markup=types.InlineKeyboardMarkup().add(back_keyboard('3_cs')))

@bot.callback_query_handler(func=lambda call: ("schedule_" in call.data) or (call.data == 'back_3_schedule') )
def schedule_certain_discipline(call):
    if call.data == 'back_3_schedule':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Дисциплины:",
                              reply_markup=list_dicipline_for_matches('schedule').add(back_keyboard(2)))
    elif call.data == "schedule_dota-2":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"Расписание матчей dota 2 на сегодня:\n{schedules['dota-2']}",
                                reply_markup=types.InlineKeyboardMarkup().add(back_keyboard('3_schedule')))
    elif call.data == "schedule_cs-go":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"Расписание матчей cs-go на сегодня:\n{schedules['cs-go']}",
                                reply_markup=types.InlineKeyboardMarkup().add(back_keyboard('3_schedule')))

"""
    for i in art:
        if call.data == i:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f" Число: {call.data}", reply_markup=types.InlineKeyboardMarkup().add(back_keyboard('3_art')))

    for i in cs_news:
        if call.data == i:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f" Число: {call.data}", reply_markup=types.InlineKeyboardMarkup().add(back_keyboard('3_cs')))
    """


bot.infinity_polling()