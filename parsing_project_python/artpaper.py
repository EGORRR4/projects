import requests

from bs4 import BeautifulSoup

import re

import pymysql

connection = pymysql.connect(db='first_database', user='root',
                      host='localhost', password='***************')
cursor = connection.cursor()

def get_initial_html():
    url = "https://www.theartnewspaper.ru/sections/news/"
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


articles = get_initial_html().find_all('div', class_="postPreviewsV2Root js-fix-post-previews")


def parsing_theatrnewspaper():
    articles = get_initial_html().find_all('div', class_="postPreviewsV2Root js-fix-post-previews")
    old_articles = False
    ww = 0
    for i in articles:
        if ww < 10:
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
                    text = f"*{preview}*\n" + ''.join(content_article)
                    if len(text) > 3000:
                        text = text[:2900] + "...\n\n_К сожалению, telegram не позволяет отправлять сообщения такой же величины как полная версия этой статьи((" \
                                        + f"Если вам интересна полная версия статьи, то смело переходите по ссылке на источник - {ref}_"
                    else:
                        text = text + f"\n_Статья была взята с сайта www.theartnewspaper.com_\n _Ссылка на страницу статьи - {ref}_"
                    cursor.execute(f"INSERT INTO articles(id, dt, kind_new, reference, preview, importance) \
                                        VALUES ('{id_article}', '{date}', 'Artnews', '{ref}', '{preview}', 'средней важности')")
                    cursor.execute(f"INSERT INTO content_articles(id_article, text) \
                                        VALUES('{id_article}', '{text}')")
                    connection.commit()
                    ww += 1
                else:
                    old_articles = True
                    connection.close()
                    break
        else:
            break

parsing_theatrnewspaper()
