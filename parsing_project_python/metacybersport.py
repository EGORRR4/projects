from datetime import datetime

import requests
from bs4 import BeautifulSoup

import re

import pymysql


def get_initial_html(discipline):
    url_metacybersport = f"https://cybersport.metaratings.ru/news/{discipline}"
    response = requests.get(url_metacybersport)
    return BeautifulSoup(response.content, 'html.parser')


soup_csgo = get_initial_html('cs-go')
soup_dota = get_initial_html('dota-2')

connection = pymysql.connect(db='first_database', user='root',
                      host='localhost', password='***************')
cursor = connection.cursor()

def parsing_and_save_metacybersport(cs_or_dota_news):
    for title in cs_or_dota_news.find_all('a', class_="NewsItem_newsItem__qMbgT"):
        days_new = title.find('div', class_="Badge_badge__hWLtc Badge_badgeSuccess__nRAV2")
        badge = title.find('div', class_="Badge_badge__hWLtc Badge_badgePrimary__RVQYH")
        if (badge and badge.text == 'Эксклюзив' or days_new):
            date = title.find('ul', class_="NewsItem_newsItemList__8bOYE")
            date = datetime.strptime(' '.join([k.text for k in date.children]), '%d.%m.%Y %H:%M')
            preview = title.find('div', class_="NewsItem_newsItemTitle__V4Tgx newsItemTitle").text
            id_article = ''.join(re.findall(r'\b\w', preview))[:10]+''.join(str(date)[:10].split('-'))
            cursor.execute(f"SELECT id FROM articles WHERE id = '{id_article}'")
            if cursor.fetchone() is None:
                ref = 'https://cybersport.metaratings.ru' + title.get_attribute_list('href')[0]
                response_certain_art = requests.get(ref)
                soupchik = BeautifulSoup(response_certain_art.content, 'html.parser')
                article = soupchik.find('div', class_="workarea-text")
                parts_article = article.find_all('p')
                parts_text = []
                for p in parts_article:
                    parts_text.append(p.text)
                text = ''.join(parts_text)
                text = f"*{preview}*\n" + text
                if len(text) > 3000:
                    text = text[:2900]+"_...\n\nК сожалению, telegram не позволяет отправлять сообщения такой же величины как полная версия этой статьи(("\
                                    + f"Если вам интересна полная версия статьи, то смело переходите по ссылке на иcточник - {ref}_"
                else:
                    text = text + f"\n_Статья была взята с сайта metaratings.ru_\n __Ссылка на страницу статьи - {ref}_"
                cursor.execute(f"INSERT INTO articles(id, dt, kind_new,  reference, preview, importance) \
                                    VALUES ('{id_article}', '{date}', 'Cybersport', '{ref}', '{preview}', 'средней важности')")
                cursor.execute(f"INSERT INTO content_articles(id_article, text) \
                                    VALUES('{id_article}', '{text}')")
                connection.commit()

            else:
                pass

connection.close()

parsing_and_save_metacybersport(soup_csgo)
parsing_and_save_metacybersport(soup_dota)

