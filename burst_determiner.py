from PIL import Image
from PIL.ExifTags import TAGS
import glob
import json
import os

f = open('output.txt', 'w')     #        Open 'coutput.txt' in write mode. Creates a file if does not exist

pictures = r"D:\Polska_Pics"    #        Filepath for picture directory
DateTimeOriginal = 36867        #        Tag ID for exif original date and time
one_behind = 0                  #       
is_burst = 0                    #        Used to determine if a burst was triggered, with two images being within >5 seconds< MAKE VAR
burst_num = 0                   #        The total number of bursts triggered
pic_q = {}                      #        Picture dictionary which contains picture name and exif date and time data
pic_l = []                      #        Sorted list of picture filepaths by numbers
prev_sec = -1                   #        The previous pictures time (in total seconds) in the loop
num = ""                        #        Used in custom_sort for a key to sort with, only contains numbers
time_diff = 0                   #        The difference between the current image and the previous image

#       A function that takes a picture filepath and returns the seconds counted up from the time. MUST ADD DATE DATA SOMEHOW
def getsecs(fp):
        dto_str = Image.open(fp)._getexif()[DateTimeOriginal]
        time_str = dto_str[11:19]
        hour = int(time_str[:2])
        minute = int(time_str[3:5])
        second = int(time_str[6:8])
        sec_baby = ((((hour * 60) + minute) * 60) + second)
        #print(dto_str)
        return sec_baby

#       Takes every file in the directory and adds it to a list because glob randomly picks files
for path in glob.glob(pictures+'/*'):
        pic_l.append(path)

#       A key for sorting, it takes the string being sorted and returns only the numbers in that string
def custom_sort(p):
        num = ''
        num.join([n for n in p if n.isdigit()])
        return num

#       Sorts the globby list into a fresh custom_sort list
pic_l.sort(key=custom_sort)

#       Initiate some lists
container = []                  #       Used to build up the list of bursts
burst_list = []                 #       Stores each list of bursts when stop is triggered
highest_burst = 0               #       Used to store the highest burst length

#       Checks if the list already contains the file trying to be written
def check(f):
        if container.count(f) == 0:
                return True     #       Not written, permitted
        else:
                return False    #       Already written, not permitted

#       Loops the sorted list of filepaths
for filepath in pic_l:
        files_list = filepath.split("\\")       #       Creates a list of directories and elements the filepath contains
        pic = files_list[(len(files_list) - 1)] #       Stores the picture name (the last element of the list) as pic
        sec = getsecs(filepath)                 #       Calls getsecs and gets the time for each picture

        #       Check condition, if its the first loop store the values and continue to the next value
        if prev_sec == -1:
                prev_sec = sec
                prev_pic = pic
                continue

        pic_q[pic] = sec                        #       Stores picture name and seconds to a dictionary
        time_diff = (sec - prev_sec)            #       Calculates the difference in time between the current picture and the previous one

        #       If the time difference is less than 5 >and the time difference is greater than 0< hack to fix not counting days
        #       Burst condition is detected
        if time_diff < 5 and time_diff > 0:
                #       If the burst condition was already triggered before
                if is_burst == 1:
                        if check(pic):
                                container.append(pic)
                                print('*')
                #       If the burst condition was not already triggered
                if is_burst == 0:
                        if check(prev_pic):
                                container.append(prev_pic)
                                print('*')
                        if check(pic):
                                container.append(pic)
                                print('*')
                        is_burst = 1
                        burst_num = burst_num + 1
        
        #       If the time difference is greater than or equal to 5
        if time_diff >= 5:
                #       If the burst condition was already triggered before
                if is_burst == 1:
                        burst_list.append(str(container))
                        c_len = len(container)
                        print(c_len)
                        f.write(str(container) + '\n')
                        if c_len > highest_burst:
                                highest_burst = c_len
                        container.clear()
                        is_burst = 0
                        print('.')
                #       If the burst condition was not already triggered
                if is_burst == 0:
                        print('.')
        prev_sec = sec
        prev_pic = pic

for burst in burst_list:
        print(str(burst) + "\n")

print(burst_num)

"""
                if ((time_diff < 3)) and (is_burst == 0):
                        if check(prev_pic):
                                container.append(prev_pic)
                        if check(pic):
                                container.append(pic)
                        is_burst = 1

                if ((time_diff < 3)) and (is_burst == 1):
                        if check(pic):
                                container.append(pic)

                if ((time_diff >= 3)) and (is_burst == 1):
                        burst_list.append(container)
                        container.clear()
                        is_burst = 0

                if ((time_diff >= 3)) and (is_burst == 0):
                        3
                prev_sec = sec
                prev_pic = pic
"""



"""
for filepath in pic_l:
        def rotate():
                prev_sec = sec
                prev_pic = pic

        files_list = filepath.split("\\")
        pic = files_list[(len(files_list) - 1)]
        sec = getsecs(filepath)

        pic_q[pic] = sec

        time_diff = sec - prev_sec

        if prev_sec == -1:
                        prev_sec = sec
                        prev_pic = pic
        else:
                if ((time_diff < 3)) and (is_burst == 0):
                        f.write(prev_pic)
                        f.write(pic)
                        is_burst = 1
                        print('/ \ ')
                        print(' |  ' + prev_pic)
                        print(' |  ' + pic)
                        prev_sec = sec
                        prev_pic = pic
                        continue

                if ((time_diff < 3)) and (is_burst == 1):
                        f.write(pic)
                        print(' |  ' + pic)
                        prev_sec = sec
                        prev_pic = pic
                        continue

                if ((time_diff >= 3)) and (is_burst == 1):
                        is_burst = 0
                        f.write('\n')
                        print('\ /')
                        prev_sec = sec
                        prev_pic = pic
                        continue

                if ((time_diff >= 3)) and (is_burst == 0):
                        #print('    ' + pic)
                        prev_sec = sec
                        prev_pic = pic
                        continue

"""