# schedule running code: 1 time at midnight
import bs4
import requests
from bs4 import BeautifulSoup
import re

def schedule_matches_cybersport(discipline):
    url_matches = f'https://www.cybersport.ru/matches/{discipline}?date=future'
    response = requests.get(url=url_matches)
    soup = BeautifulSoup(response.content, 'html.parser')
    growth_list_matches = [i for i in soup.find('div', class_="root_Ts3Rx").children]
    matches = []
    def delete_comments():
        nonlocal matches
        for i in range(len(growth_list_matches)):
            if type(growth_list_matches[i]) is bs4.Tag:
                matches.append(growth_list_matches[i])
    delete_comments()
    if len(matches) >= 2:
        with open(f'schedule_matches_{discipline}.txt', 'w') as f:
            f.write(f'{matches[0].text}')
            i = 1
            while matches[i].get_attribute_list('class')[0] != "dateHeader_ke3kU":
                name_team_1 = matches[i].find('div', class_="root_6Q2Jn participant_DJi5J participant1_xWFn2").text
                name_team_1 = ''.join(re.split(r'\s',name_team_1))
                name_team_2 = matches[i].find('div', class_="root_6Q2Jn participant_DJi5J participant2_P9p5D").text
                name_team_2 = ''.join(re.split(r'\s', name_team_2))
                match_time = matches[i].find('div', class_="date_Qyw+T").text
                match_time = ''.join(re.split(r'\s', match_time))
                # score_match = matches[i].find('div', class_="score_+pSbU").find_all('span', class_='') # for past
                f.write(f'\n{match_time}\n')
                f.write(f'{name_team_1} - {name_team_2}')
                i += 1
    else:
        pass
schedule_matches_cybersport('cs-go')
schedule_matches_cybersport('dota-2')