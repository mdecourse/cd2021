# pip install moviepy
import os
from moviepy.editor import VideoFileClip

# Converts into more readable format
def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return hours, mins, seconds
    
for dname, dirs, files in os.walk("2021-03_2a_stage1"):
    for fname in files:
        vName = os.path.join(dname, fname)
        clip = VideoFileClip(vName)
        hours, mins, secs = convert(clip.duration)
        print(fname + "組:", str(int(mins)) + "分", str(int(secs)) + "秒")