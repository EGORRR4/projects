from datetime import datetime

import requests
from bs4 import BeautifulSoup

from last_dates import dict_dates

import re

import pymysql




def get_initial_html(discipline):
    url_metacybersport = f"https://cybersport.metaratings.ru/news/{discipline}"
    response = requests.get(url_metacybersport)
    return BeautifulSoup(response.content, 'html.parser')


soup_csgo = get_initial_html('cs-go')
soup_dota = get_initial_html('dota-2')

def update_data(discipline):
    if datetime.weekday(datetime.now()) == 6:
        with open(f'MetaCybersport_{discipline}', 'r') as f:
            text = re.split(r'!!!Новая неделя, пора обновляться!!!', "".join(f.readlines()))
            del text[0]
        with open(f'MetaCybersport_{discipline}.txt', 'w') as f:
            f.write("".join(text))
            f.write("\n!!!Новая неделя, пора обновляться!!!\n")

update_data('dota-2')
update_data('cs-go')

def parsing_and_save_metacybersport(soup, discipline):
    last_datetime = dict_dates[f'lastdate_mcs_{discipline}.txt']
    i = 0
    for title in soup.find_all('a', class_="NewsItem_newsItem__qMbgT"):
        date = title.find('ul', class_="NewsItem_newsItemList__8bOYE")
        date = datetime.strptime(' '.join([k.text for k in date.children]), '%d.%m.%Y %H:%M')

        preview = title.find('div', class_="NewsItem_newsItemTitle__V4Tgx newsItemTitle")
        days_new = title.find('div', class_="Badge_badge__hWLtc Badge_badgeSuccess__nRAV2")
        badge = title.find('div', class_="Badge_badge__hWLtc Badge_badgePrimary__RVQYH")
        if (badge and badge.text == 'Эксклюзив' or days_new) and date > last_datetime:
            if i == 0:
                dict_dates[f'lastdate_mcs_{discipline}'] = date
                i += 1
            ref = 'https://cybersport.metaratings.ru' + title.get_attribute_list('href')[0]
            response_certain_art = requests.get(ref)
            soupchik = BeautifulSoup(response_certain_art.content, 'html.parser')
            article = soupchik.find('div', class_="workarea-text")
            parts_article = article.find_all('p')
            article = []
            for p in parts_article:
                article.append(p.text)
            with open(f'MetaCybersport_{discipline}.txt', 'a') as f:
                f.write(preview.text.upper())
                f.write('\n'.join(article))
                f.write('\n')
    if i == 1:
        with open('last_dates.py', 'w') as f:
            f.write('import datetime\n')
            f.write(f'dict_dates ={dict_dates}')


parsing_and_save_metacybersport(soup_csgo, 'cs-go')
parsing_and_save_metacybersport(soup_dota, 'dota-2')
