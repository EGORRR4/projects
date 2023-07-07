import telebot
from telebot import types

import re


bot  = telebot.TeleBot("6193778513:AAG2iZsKyaxabWQtdMqoS_AHfRu6EuXDX4o", parse_mode=None)

mcs = ['1','2','3','4']
cs_d = ['5','6']
cs_news = mcs + cs_d
art=['7','8']
kind_news = ['cybersport', 'art']

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

def list_previews_keyboard(selected_news:list):
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text= preview,
                    callback_data=preview
                )
            ]
            for preview in selected_news
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
                              text=f"cybersport:", reply_markup=list_previews_keyboard(cs_news).add(back_keyboard(2)))
    elif call.data == "art":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Artnews{list_previews_keyboard(art).to_dict().items()}", reply_markup=list_previews_keyboard(art).add(back_keyboard(2)))
    elif call.data == "back_2":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Новости", reply_markup=list_news())

@bot.callback_query_handler(func=lambda call: (call.data in cs_news or art) or call.data in ['back_3_cs', 'back_3_art'])
def deep_lvl(call):
    if call.data == "back_3_cs":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Новости киберспорта", reply_markup=list_previews_keyboard(cs_news).add(back_keyboard(2)))
    elif call.data == "back_3_art":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Новости искусства",
                              reply_markup=list_previews_keyboard(art).add(back_keyboard(2)))
    for i in art:
        if call.data == i:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f" Число: {call.data}", reply_markup=types.InlineKeyboardMarkup().add(back_keyboard('3_art')))
    for i in cs_news:
        if call.data == i:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f" Число: {call.data}", reply_markup=types.InlineKeyboardMarkup().add(back_keyboard('3_cs')))


bot.infinity_polling()