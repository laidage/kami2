# 40 * 30
#40 * 40
#18   29
# 72 * 116
# 720 * 1160

from PIL import Image
import os
from closed_color import min_color_diff

def get_img_rgb(file_path):
    im = Image.open(file_path)
    im = im.convert('RGB')
    im.getdata()
    pixes = im.load()
    return pixes


def make_hidden_config(config_file, img_file):
    color_nums, min_steps = 0, 0
    color_rgbs = []
    with open('hidden_config/' + config_file, 'r') as f:
        lines = f.readlines()
        color_nums, min_steps = int(lines[0]), int(lines[1])
        for i in range(color_nums):
            color_rgbs.append(eval(lines[i+2]))

    pixes = get_img_rgb('hidden_img/' + img_file)
    with open('hidden_config/' + config_file, 'w') as f:
        f.write(str(color_nums) + '\n' )
        f.write(str(min_steps) + '\n')
        for i in range(color_nums):
            f.write(str(color_rgbs[i]) + '\n')

        for i in range(116):
            y = 5 + i * 10
            row = []
            for j in range(72):
                x = 5 + j * 10
                color = pixes[x, y]
                row.append(min_color_diff(color, color_rgbs)[1])
            if i == 115:
                f.write(str(row))
            else:
                f.write(str(row) + '\n')

if __name__ == '__main__':
    make_hidden_config('1', '1.png')