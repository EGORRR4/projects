import re

import requests

from datetime import datetime

import pymysql


def fetch(url, params):
    headers = params["headers"]
    return requests.get(url, headers=headers).json()['events']


fetch_dota_news = fetch(
    "https://store.steampowered.com/events/ajaxgetpartnereventspageable/?clan_accountid=0&appid=570&offset=0&count=100&l=russian&origin=https:%2F%2Fwww.dota2.com",
    {
        "cache": "default",
        "credentials": "omit",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
        },
        "method": "GET",
        "mode": "cors",
        "redirect": "follow",
        "referrer": "https://www.dota2.com/",
        "referrerPolicy": "strict-origin-when-cross-origin"
    })

fetch_cs_news = fetch(
    "https://store.steampowered.com/events/ajaxgetpartnereventspageable/?clan_accountid=0&appid=730&offset=0&count=100&l=russian&origin=https:%2F%2Fwww.counter-strike.net",
    {
        "cache": "default",
        "credentials": "omit",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
        },
        "method": "GET",
        "mode": "cors",
        "redirect": "follow",
        "referrer": "https://www.counter-strike.net/",
        "referrerPolicy": "strict-origin-when-cross-origin"
    })

connection = pymysql.connect(db='first_database', user='root',
                             host='localhost', password='***************')
cursor = connection.cursor()


def convert_json_date(json_date):
    json_date = int(json_date)
    return datetime.fromtimestamp(json_date).strftime('%Y-%m-%d %I:%M:%S')


def get_news(cs_or_dota_news, site):
    for i in range(3):  # len(cs_or_dota_news)
        json_date = cs_or_dota_news[i]['announcement_body']['posttime']
        date = convert_json_date(json_date)
        preview = cs_or_dota_news[i]['event_name']
        id_article = ''.join(re.findall(r'\b\w', preview)) + date[:10]
        cursor.execute(f"SELECT id FROM articles WHERE id = '{id_article}'")
        if cursor.fetchone() is None:
            print('AAA')
            ref = f'https://www.{site}/newsentry/' + f"{cs_or_dota_news[i]['gid']}"
            cursor.execute(f"INSERT INTO articles(id, dt, kind_new, reference, preview, importance) \
                               VALUES ('{id_article}', '{date}', 'Cybersport', '{ref}', '{preview}', 'важно')")
            if cs_or_dota_news[i]['event_type'] == 12:
                text = f"Вышло обновление!!! С новыми изменениями в этом обновлени можно ознакомиться на [официальной странице]({ref})"
                cursor.execute(f"INSERT INTO content_articles(id_article, text) \
                                                    VALUES('{id_article}', '{text}')")

            else:
                text = ''.join(re.split(r'\[[^\]]+\]|\{[^\}]+\}/[^!]+\.png', cs_or_dota_news[i]['announcement_body']['body']))
                text = f"*{preview}*\n" + text
                if len(text) > 3000:
                    text = text[:2800] + "_...\n\nК сожалению, telegram не позволяет отправлять сообщения такой же величины как полная версия этой статьи(("\
                                       + f"Если вам интересна полная версия статьи, то смело переходите по ссылке на иcточник - {ref}_"
                else:
                    text = text + f"\n_Статья была взята с сайта www.{site}_\n _Ссылка на страницу статьи - {ref}_"
                cursor.execute(f"INSERT INTO content_articles(id_article, text) \
                                    VALUES('{id_article}', '{text}')")

            connection.commit()

        else:
            break

get_news(fetch_cs_news, 'counter-strike.net')
get_news(fetch_dota_news, 'dota2.com')
connection.close()
