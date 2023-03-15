import requests
import json

import schedule


def update_weather():
    try:
        print('update start')
        url = "https://devapi.qweather.com/v7/weather/now?key=fd34706246e44dbdbbe3bb33af2b6a64&location=101190603"
        headers = {
            'Content-Type': 'application/json'
        }

        r = requests.request("GET", url, headers=headers)
        humidity = r.json()['now']['humidity'] + '%'
        temperature = r.json()['now']['temp'] + '℃'
        weather_code = int(str(r.json()['now']['icon']))
        weather_text = r.json()['now']['text']

        print('1')

        if weather_code == 154:
            weather_code = 104
            print('replace')

        if weather_code < 150:
            weather_color = '#FEB41E'
        elif weather_code >= 150 & weather_code < 500:
            weather_color = '#6569FD'
        else:
            weather_color = '#F6F7F9'

        print(weather_color)
        weather_icon = '/home/pi/clock/icons/' + str(weather_code) + '-fill.png'
        print('update success')
    except:
        humidity = '--'
        temperature = '--'


# schedule.every(10).minutes.do(update_weather)
update_weather()
