from PIL import Image
from PIL.ExifTags import TAGS
import glob
import os

f = open('output.txt', 'w')

pictures = r"E:\polska"
DateTimeOriginal = 36867
one_behind = 0
burst = 0

for filepath in glob.glob(pictures+"/*"):
        print(filepath)
        dto_str = Image.open(filepath)._getexif()[DateTimeOriginal]
        time_str = dto_str[11:19]
        hour = int(time_str[:1])
        minute = int(time_str[3:5])
        second = int(time_str[6:8])
        sec = ((((hour * 60) + minute) * 60) + second)

        if ((sec - one_behind) < 3):
                f.write(prev_file[10:] + '\n')
                burst = 1
        else:
                if burst == 1:
                        try:
                                f.write(prev_file)
                        except:
                                print("I TRIED")
                burst = 0
                f.write('\n')


        prev_file = filepath
        one_behind = sec


        print(dto_str)
        print(time_str)
        print('Hour: '+dto_str[11:13]+' Minute: '+str(minute)+' Second: '+str(second)+' Total Secs: '+str(sec))

        