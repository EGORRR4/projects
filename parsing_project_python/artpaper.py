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
    dict_articles = last_dict_articles
    last_date = list(dict_articles.keys())[-1]
    len_prev_list_refs = len(dict_articles[last_date])
    for i in articles:
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
                cursor.execute(f"INSERT INTO articles(id, dt, reference, preview, importance) \
                                        VALUES ('{id_article}', '{date}', '{ref}', '{preview}', 'средней важности')")
                cursor.execute(f"INSERT INTO content_articles(id_article, text) \
                                        VALUES('{id_article}', '{text}')")
                connection.commit()
            else:
                pass
    connection.close()

"""
    min_date = list(dict_articles.keys())[0]
    now = datetime.weekday(datetime.now())

    if now == 6 and len(dict_articles) > 7:
        while datetime.weekday(str(min_date), '%Y%m%d') <= 6:
            del dict_articles[min_date]
            min_date = list(dict_articles.keys())[0]
    global list_articles_newartpaper
    global list_previews_articels_newartpaper
    list_articles_newartpaper = []
    list_previews_articels_newartpaper = []
    for key_date, list_refs in dict_articles.items():
        if int(key_date) > int(last_date):
            for ref in list_refs:
                certain_art = requests.get(ref)
                soup_certain_art = BeautifulSoup(certain_art.content, 'html.parser')

                k = 1
                content_article = []
                title = soup_certain_art.find('h1', class_="postTitleRoot js-fix-hanging").text
                while soup_certain_art.find('div', class_=f"postTextRoot postTextRoot-{k}"):
                    content_article.append(soup_certain_art.find('div', class_=f"postTextRoot postTextRoot-{k}").text)
                    k += 2
                with open('theartnewspaperru', 'a+') as f:
                    f.write(f'{title.upper()}\n')
                    for p in content_article:
                        f.write(f'{p}')
                    f.write('\n')
                list_articles_newartpaper.append("".join(content_article))
                list_previews_articels_newartpaper.append(title)
        elif int(key_date) == int(last_date) and len(list_refs) < len_prev_list_refs:
            cnt_new_artcles = len_prev_list_refs - list_refs
            while cnt_new_artcles <= 0:
                certain_art = requests.get(list_refs[-cnt_new_artcles])
                soup_certain_art = BeautifulSoup(certain_art.content, 'html.parser')

                k = 1
                content_article = []
                title = soup_certain_art.find('h1', class_="postTitleRoot js-fix-hanging").text
                while soup_certain_art.find('div', class_=f"postTextRoot postTextRoot-{k}"):
                    content_article.append(soup_certain_art.find('div', class_=f"postTextRoot postTextRoot-{k}").text)
                    k += 2
                with open('theartnewspaperru', 'a+') as f:
                    f.write(f'{title.upper()}\n')
                    for p in content_article:
                        f.write(f'{p}')
                    f.write('\n')
                cnt_new_artcles -= 1
                list_articles_newartpaper.append("".join(content_article))
                list_previews_articels_newartpaper.append(title)
    with open('dict_for_theartnewspaper.py', 'w') as f:
        f.write(f'last_dict_articles = {dict_articles}')

"""
parsing_theatrnewspaper()
