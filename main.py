import json
import random

import moviepy.editor as mpe
#from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.io.VideoFileClip as tes

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.fx.resize import resize
import os
import collector

def renew_videos():
    with open("videos.json", "r") as json_file:
        data = json.load(json_file)
        for i in data["data"]:
            i["used"] = False

    with open("videos.json", "w") as json_f:
        json.dump(data, json_f, indent=2)


def clean_files(folder):
    for i in os.listdir(folder):
        if i[:5] != "final":
            try:
                os.remove(f'{folder}/{i}')
            except FileNotFoundError as e:
                print(e)

def combine_videos(length, height):
    with open("videos.json", "r") as json_file:
        data = json.load(json_file)
        video_list = []
        clips = []
        count = 0
        temp_length = length
        while temp_length > 0:
            temp = random.choice(data["data"])
            if not temp["used"]:
                count +=1
                print(data["data"].index(temp))
                data["data"][data["data"].index(temp)]["used"] = True
                temp_clip = mpe.VideoFileClip(temp["video_title"])

                temp_clip = temp_clip.resize(height=height)
                print(F"*****NO MODIFICATION. DIMENSIONS {temp_clip.w}x{temp_clip.h}*****")
                if (temp_clip.w % 2) != 0:
                    test = temp_clip.w + 1
                    print(test)
                    test2 = int(temp_clip.w) + 1
                    print(test2)
                    temp_clip = temp_clip.resize((test2, temp_clip.h))
                    print(f"*****CLIP RESIZED. NEW DIMENSIONS {temp_clip.w}x{temp_clip.h}*****")
                else:
                    print(f"*****UNMODIFIED. DIMENSIONS {temp_clip.w}x{temp_clip.h}*****")
                print(temp_clip.w)
                clips.append(temp_clip)
                video_list.append(temp["video_title"])
                temp_length -= temp["duration"]
            else:
                print("USED")
        print(video_list)
        print(length-temp_length)
        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(f"Final Video{data['videos']}.mp4", threads=8)
        data['videos'] += 1
    with open("videos.json", "w") as json_f:
        json.dump(data, json_f, indent=2)



collector.get_reddit_videos("dankvideos", 40,"meme storage")
#clean_files("meme storage")
#renew_videos()

combine_videos(600, 1200)