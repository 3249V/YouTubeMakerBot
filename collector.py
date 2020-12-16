import json
import time
import urllib
import traceback
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import praw


def get_reddit_videos(subreddit, count, folder):
    r = praw.Reddit(client_id="Oez4fMric1z1uQ", client_secret="3-IOEjlgneiGBeNT02yeZ3TDLL1asw", user_agent="idk")
    counter = 0
    sub = r.subreddit(subreddit).hot(limit=count*10)
    temp_dict = []
    titles=[]
    times=[]
    with open("videos.json", "r") as json_file:
        data = json.load(json_file)
        existing_titles = data["titles"]
    print(existing_titles)
    if folder != "":
        folder = folder + "/"
    for post in sub:
        if counter > (count-1):
            break
        if post.is_video and not post.over_18 and not post.title in existing_titles:
            vid_link = post.media['reddit_video']['fallback_url']
            audio_link = f'{vid_link.split("_")[0]}_audio.mp4'
            #print(audio_link)
            #print(vid_link)
            print(f'{folder}{post.title}.mp4')
            try:
                beginning = time.perf_counter()

                title = post.title.replace(":", "_colon_")
                title = title.replace("?", "")
                urllib.request.urlretrieve(vid_link, f'{folder}{title}.mp4')
                urllib.request.urlretrieve(audio_link, f'{folder}{title}.mp3')
                vid = VideoFileClip(f'{folder}{title}.mp4')
                audio = AudioFileClip(f'{folder}{title}.mp3')
                combined_vid = vid.set_audio(audio)
                combined_vid.write_videofile(f'{folder}final {title}.mp4')
                temp_dict.append({"video_title": f'{folder}final {title}.mp4',
                                  "duration": post.media['reddit_video']["duration"],
                                 "used": False, "url": post.url, "source": "reddit", "score": post.score, "tags": []})
                counter +=1
                print(f"-----DOWNLOADED VIDEO {counter} OF {count}-----")
                times.append(time.perf_counter()-beginning)
                titles.append(post.title)
            except:
                print("Exception at download")
                traceback.print_exc()

    with open("videos.json", "r") as json_file:
        data = json.load(json_file)
        video_list = []
        for i in data["data"]:
            video_list.append(i["video_title"])
        for i in temp_dict:
            if not i["video_title"] in video_list:
                data["data"].insert(0,i)
                data["total_duration"] += i["duration"]
                data["usable_duration"] += i["duration"]
        data["time_downloading"] += sum(times)
        data["downloads"] += len(times)
        data["average_download_time"] = data["time_downloading"] / data["downloads"]
        for i in titles:
            data["titles"].append(i)
        print(temp_dict)
    with open("videos.json", "w") as json_f:
        json.dump(data, json_f, indent=2)

#get_reddit_videos("dankvideos", 100,"meme storage")