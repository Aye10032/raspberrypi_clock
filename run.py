import logging
import sys
import time

import requests
import schedule
from PIL import Image, ImageDraw, ImageFont
from ST7789 import ST7789

# General
SPI_PORT = 0
SPI_CS = 0
SPI_DC = 25
BACKLIGHT = 18
SPI_RST = 27

# Screen dimensions
WIDTH = 240
HEIGHT = 240

buffer = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(buffer)

draw.rectangle((0, 0, 50, 50), (255, 0, 0))
draw.rectangle((320 - 50, 0, 320, 50), (0, 255, 0))
draw.rectangle((0, 240 - 50, 50, 240), (0, 0, 255))
draw.rectangle((320 - 50, 240 - 50, 320, 240), (255, 255, 0))

disp = ST7789(
    port=SPI_PORT,
    cs=SPI_CS,
    dc=SPI_DC,
    backlight=BACKLIGHT,
    rst=SPI_RST,
    width=WIDTH,
    height=HEIGHT,
    rotation=0,
    spi_speed_hz=60 * 1000 * 1000,
    invert=True
)

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height

weather_text = '--'
weather_icon = '/home/pi/clock/icons/999-fill.png'
humidity = '--'
temperature = '--'
weather_color = '#F6F7F9'


def update_weather():
    global humidity, temperature, weather_text, weather_icon, weather_color
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

        if weather_code == 154:
            weather_code = 104

        if weather_code < 150:
            weather_color = '#FEB41E'
        elif weather_code >= 150 & weather_code < 500:
            weather_color = '#6569FD'
        else:
            weather_color = '#F6F7F9'

        weather_icon = '/home/pi/clock/icons/' + str(weather_code) + '-fill.png'
        print('update success')
    except:
        weather_text = '--'
        weather_icon = '/home/pi/clock/icons/999-fill.png'
        weather_color = '#F6F7F9'
        humidity = '--'
        temperature = '--'


def mainrun():
    try:
        Font3 = ImageFont.truetype("/home/pi/clock/Font/Font00.ttf", 40)
        Font2_5 = ImageFont.truetype("/home/pi/clock/Font/Font00.ttf", 28)
        Font1 = ImageFont.truetype("/home/pi/clock/Font/Font00.ttf", 26)
        Font1_5 = ImageFont.truetype("/home/pi/clock/Font/Font00.ttf", 22)
        Font0_8 = ImageFont.truetype("/home/pi/clock/Font/Font02.ttf", 18)

        schedule.every(10).minutes.do(update_weather)

        while True:
            image = Image.open('/home/pi/clock/bg.jpg')
            draw = ImageDraw.Draw(image)

            schedule.run_pending()

            time_text = time.strftime("%I:%M:%S", time.localtime())
            p_text = time.strftime('%p', time.localtime())
            month_text = time.strftime('%m月%d日', time.localtime())
            w_day = time.localtime().tm_wday
            if w_day == 0:
                month_text += ' 周一'
            elif w_day == 1:
                month_text += ' 周二'
            elif w_day == 2:
                month_text += ' 周三'
            elif w_day == 3:
                month_text += ' 周四'
            elif w_day == 4:
                month_text += ' 周五'
            elif w_day == 5:
                month_text += ' 周六'
            elif w_day == 6:
                month_text += ' 周日'

            draw.text((30, 28), month_text, fill='WHITE', font=Font2_5)

            draw.text((30, 92), time_text, fill="WHITE", font=Font3)

            if p_text == 'AM':
                draw.text((190, 92), p_text, fill='#F7834F', font=Font0_8)
            elif p_text == 'PM':
                draw.text((190, 120), p_text, fill='#4FC3F7', font=Font0_8)

            draw.bitmap((28, 176), Image.open(weather_icon), fill=weather_color)
            draw.text((70, 174), weather_text, fill='WHITE', font=Font1)
            draw.text((165, 162), humidity, fill='WHITE', font=Font1_5)
            draw.text((165, 194), temperature, fill='WHITE', font=Font1_5)

            # image1 = image1.rotate(180)
            img_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
            disp.display(img_flip)
            time.sleep(1)

    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        disp.reset()
        logging.info("quit:")
        exit()


if __name__ == '__main__':
    time.sleep(1)
    update_weather()
    mainrun()
