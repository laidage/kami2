# 40 * 30
#40 * 40
#18   29
# 72 * 116
# 720 * 1160

from PIL import Image
from closed_color import min_color_diff
from collections import Counter

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

        # for i in range(116):
        #     y = 5 + i * 10
        #     row = []
        #     for j in range(72):
        #         x = 5 + j * 10
        #         color = pixes[x, y]
        #         row.append(min_color_diff(color, color_rgbs)[1])
        #     if i == 115:
        #         f.write(str(row))
        #     else: 
        #         f.write(str(row) + '\n')

        for i in range(116):
            row = []
            for j in range(72):
                colors = []
                for m in range(10):
                    y = m + i * 10
                    for n in range(10):
                        x = n + j * 10
                        color = pixes[x, y]
                        colors.append(min_color_diff(color, color_rgbs)[1])
                color_count = Counter(colors)
                cc = color_count.most_common(1)[0][0]
                row.append(cc)
            if i == 115:
                f.write(str(row))
            else: 
                f.write(str(row) + '\n')

if __name__ == '__main__':
    for i in range(1, 6):
        make_hidden_config(str(i), str(i) + '.png')