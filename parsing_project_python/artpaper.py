import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from dict_for_theartnewspaper import last_dict_articles  # local module
import pymysql

connection = pymysql.connect(db='first_database', user='root',
                      host='localhost', password='1212313111123')
cursor = connection.cursor()


def get_initial_html():
    url = "https://www.theartnewspaper.ru/sections/news/"
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


articles = get_initial_html().find_all('div', class_="postPreviewsV2Root js-fix-post-previews")


def parsing_theatrnewspaper():
    articles = get_initial_html().find_all('div', class_="postPreviewsV2Root js-fix-post-previews")
    old_articles = False
    for i in articles:
        if not old_articles:
            for k in i.find_all('a'):
                preview = k.get_attribute_list('title')[0]
                ref = 'https://www.theartnewspaper.ru' + k.get_attribute_list('href')[0]
                date = ''.join(re.split('\.', k.find('div', class_="postPreviewsItemDate").text)[::-1])
                id_article = ''.join(re.findall(r'\b\w', preview))+date
                cursor.execute(f"SELECT id FROM articles WHERE  id = '{id_article}'")
                if cursor.fetchone() is None:
                    certain_art = requests.get(ref)
                    soup_certain_art = BeautifulSoup(certain_art.content, 'html.parser')

                    k = 1
                    content_article = []
                    while soup_certain_art.find('div', class_=f"postTextRoot postTextRoot-{k}"):
                        content_article.append(
                            soup_certain_art.find('div', class_=f"postTextRoot postTextRoot-{k}").text)
                        k += 2
                    text = ''.join(content_article)
                    if len(text) > 3000:
                        text = text[:2900] + f"...К сожалению, telegram не позволяет отправлять сообщения такой же величины как полная версия этой статьи(( \
                                           Если вам интересна полная версия статьи, то смело переходите по ссылке на иточник - {ref}"
                    cursor.execute(f"INSERT INTO articles(id, dt, kind_new, reference, preview, importance) \
                                        VALUES ('{id_article}', '{date}', 'Artnews', '{ref}', '{preview}', 'средней важности')")
                    cursor.execute(f"INSERT INTO content_articles(id_article, text) \
                                        VALUES('{id_article}', '{text}')")
                    connection.commit()
                else:
                    old_articles = True
                    break
        else:
            break

    connection.close()
parsing_theatrnewspaper()
