from PIL import Image
import os

def get_files(path):
    files = []
    for file in os.listdir(path):
        if not os.path.isfile(file):
            files.append(file)
    return files

def resize_img(file):
    dir = "level_image/"
    index = file.split("_")[0]
    im = Image.open(dir + file)
    im = im.crop((0, 0, 720, 1160))
    im = im.resize((99, 160))
    im.save("level_img/"+ index + ".png")

if __name__ == "__main__":
    files = get_files("level_image/")
    for file in files:
        resize_img(file)