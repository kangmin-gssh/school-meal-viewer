import sys
import json
import subprocess
from datetime import datetime, timedelta

if __name__ == '__main__':
    now = datetime.now()
    if now.hour < 6:
        now = now - timedelta(days=1)

    today = now.strftime('%Y%m%d')
    tomorrow = (now + timedelta(days=1)).strftime('%Y%m%d')

    print(today, tomorrow)

    # json 양식: date, date, [menus] * 6
    with open('./saved/menus.json', 'r') as file:
        try:
            data = json.loads(file.read())
        except:
            data = [None]
        print(data)

    if today == data[0]:
        pass
    else:
        subprocess.run([sys.executable, './parse.py'])

    subprocess.run([sys.executable, './app.py'])
