import json
from urllib import request
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def parse_menu():
    office_code = 'R10' # 경북교육청
    school_code = '8750555' # 경산과학고등학교

    now = datetime.now()
    if now.hour < 8:
        now = now - timedelta(days=1)

    today = now.strftime('%Y%m%d')
    tomorrow = (now + timedelta(days=1)).strftime('%Y%m%d')

    today_url = \
        f'https://open.neis.go.kr/hub/mealServiceDietInfo?ATPT_OFCDC_SC_CODE={office_code}&SD_SCHUL_CODE={school_code}&MLSV_YMD={today}'

    tomorrow_url = \
        f'https://open.neis.go.kr/hub/mealServiceDietInfo?ATPT_OFCDC_SC_CODE={office_code}&SD_SCHUL_CODE={school_code}&MLSV_YMD={tomorrow}'

    def dish_name(raw: str) -> str:
        return raw.replace(' ', '').split('(')[0].rstrip('s').replace('`', '')

    targets = [request.urlopen(url) for url in [today_url, tomorrow_url]]
    raw = [BeautifulSoup(target, 'html.parser', from_encoding='utf-8').select('row') for target in targets]

    menus = [today, tomorrow]

    ## TODO: 시간대 중 일부가 누락된 경우
    # today
    if raw[0]:
        for meal in raw[0]:
            meal = meal.select_one('ddish_nm').string
            print(meal)
            menus.append(list(map(dish_name, meal.split('<br/>'))) if meal else [None])
    else:
            [menus.append([None]) for _ in range(3)]

    # tomorrow
    if raw[1]:
        for meal in raw[1]:
            meal = meal.select_one('ddish_nm').string
            print(meal)
            menus.append(list(map(dish_name, meal.split('<br/>'))) if meal else [None])
    else:
            [menus.append([None]) for _ in range(3)]

    with open('./saved/menus.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(menus, ensure_ascii=False))
