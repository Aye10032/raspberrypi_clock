import os

import cairosvg

icon_path = 'icons'

icons = os.listdir(icon_path)

for icon in icons:
    if icon.__contains__('.svg'):
        svg_path = os.path.join(icon_path, icon)
        print(svg_path)
        png_path = os.path.join(icon_path, icon).replace('.svg', '.png')
        print(png_path)
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=35, output_height=35, unsafe=True)
