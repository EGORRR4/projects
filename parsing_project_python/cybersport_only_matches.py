# schedule running code: 1 time at midnight
import requests
from bs4 import BeautifulSoup

def schedule_matches_cybersport(discipline):
    url_matches = f'https://www.cybersport.ru/matches/{discipline}?date=future'
    response = requests.get(url=url_matches)
    soup = BeautifulSoup(response.content, 'html.parser')
    growth_list_matches = [i for i in soup.find('div', class_="root_Ts3Rx").children]
    b = []
    def delete_comments():
        nonlocal b
        for i in range(len(growth_list_matches)):
            if type(growth_list_matches[i]) == type(growth_list_matches[0]):
                b.append(growth_list_matches[i])
    delete_comments()
    print(len(b))
    with open(f'schedule_matches_{discipline}.txt', 'a') as f:
        f.write(f'\n{b[0].text}')
        i = 1
        while b[i].get_attribute_list('class')[0] != "dateHeader_ke3kU":
            name_team_1 = b[i].find('div', class_="root_6Q2Jn participant_DJi5J participant1_xWFn2")
            name_team_2 = b[i].find('div', class_="root_6Q2Jn participant_DJi5J participant2_P9p5D")
            match_time = b[i].find('div', class_="date_Qyw+T")
            # score_match = b[i].find('div', class_="score_+pSbU").find_all('span', class_='') # for past
            f.write(f'{match_time.text}\n')
            f.write(f'{name_team_1.text} - {name_team_2.text}')
            i += 1
schedule_matches_cybersport('cs-go')
schedule_matches_cybersport('dota-2')