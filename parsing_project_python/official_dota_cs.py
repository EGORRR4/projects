import re

import requests

from last_dates import dict_dates

from datetime import datetime


def fetch(url, params):
    headers = params["headers"]
    return requests.get(url, headers=headers).json()['events'][0:10] # уверен что сайт не будет выпускать больше 10 статей в день

dota_news = fetch("https://store.steampowered.com/events/ajaxgetpartnereventspageable/?clan_accountid=0&appid=570&offset=0&count=100&l=russian&origin=https:%2F%2Fwww.dota2.com", {
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

cs_news = fetch("https://store.steampowered.com/events/ajaxgetpartnereventspageable/?clan_accountid=0&appid=730&offset=0&count=100&l=russian&origin=https:%2F%2Fwww.counter-strike.net", {
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

last_posttime_dota = dict_dates['posttime_dota']
last_posttime_csgo = dict_dates['posttime_csgo']

def update_data(discipline):
    if datetime.weekday(datetime.now()) == 6:
        with open(f'MetaCybersport_{discipline}', 'r') as f:
            text = re.split(r'!!!Новая неделя, пора обновляться!!!', "".join(f.readlines()))
            del text[0]
        with open(f'MetaCybersport_{discipline}', 'w') as f:
            f.write("".join(text))
            f.write("\n!!!Новая неделя, пора обновляться!!!\n")

update_data('dota2')
update_data('csgo')

def new_articles(news, last_posttime):
    current_posttime = [news[i]['announcement_body']['posttime'] for i in range(10)]
    if current_posttime[0] == last_posttime:
        return []
    count_new_news = 0
    while last_posttime < current_posttime[count_new_news]:
        count_new_news += 1
    return news[:count_new_news]

today_dota2 = new_articles(dota_news, last_posttime_dota)
today_csgo = new_articles(cs_news, last_posttime_csgo)

def parsing_and_save_today_news(today_news, discipline):
    if len(today_news) == 0:
        return
    else:
        last_posttime =  today_news[0]['announcement_body']['posttime']
        with open(f'news_{discipline}.txt', 'a+') as f:
            for i in range(len(today_news)):
                f.write(''.join(re.split(r'\[\w*[^url=]\w*\d*\]', today_news[i]['announcement_body']['body'])))
                f.write('\n')
                
        dict_dates[f'posttime_{discipline}'] = last_posttime
        with open('last_dates.py' 'w') as f:
            f.write(f'dict_dates ={dict_dates}')
                
parsing_and_save_today_news(today_dota2, 'dota2')
parsing_and_save_today_news(today_csgo, 'csgo')