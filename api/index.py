import fire
import os
from glob import glob
result = [y for x in os.walk(".") for y in glob(os.path.join(x[0], '*.*'))]
paths = []
for i in result:
    if ".png" in i or ".mp4" in i or i in ".jpg":
        paths.append(i)
t = int(input("Что хотите исследовать? \n1. Камера\n2. Картинка или видео\nВвод: "))
video_file = 0

if(t==2):
    video_file = ""
    for i in range(len(paths)):
        print(i+1,">",paths[i])
    p = int(input("Введите номер каталога: "))
    video_file = paths[p-1]

p = int(input("Включить видео?\n0 - нет\n1 - да\nВвод: "))

item = fire.Fire(video_file)
item.add([18, 50, 50],[35, 255, 255] )
# item.open()

for isFind in item.find( True if p==1 else False):
    if(isFind):
        print("Пожар обнаружен")