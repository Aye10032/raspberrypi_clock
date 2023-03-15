import time

import PIL.ImageShow
from PIL import Image, ImageDraw, ImageFont

humidity = '13℃'
temperature = '45%'

image1 = Image.open('bg.jpg')
draw = ImageDraw.Draw(image1)

# logging.info("draw text")
Font3 = ImageFont.truetype("Font00.ttf", 40)
Font1 = ImageFont.truetype("Font00.ttf", 26)
Font1_5 = ImageFont.truetype("Font00.ttf", 22)
Font2_5 = ImageFont.truetype("Font00.ttf", 28)
Font0_8 = ImageFont.truetype("Font02.ttf", 18)

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

draw.text((70, 174), '小雨', fill='WHITE', font=Font1)
draw.text((165, 162), humidity, fill='WHITE', font=Font1_5)
draw.text((165, 194), temperature, fill='WHITE', font=Font1_5)

draw.bitmap((28, 176), Image.open('icons/101-fill.png'), fill='#8184FC')

PIL.ImageShow.show(image1)
