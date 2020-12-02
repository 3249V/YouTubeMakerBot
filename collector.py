import praw
import urllib
import moviepy.editor as mpe
import json
from pytube import YouTube
#dankvideos, memevideos


def get_reddit_videos(subreddit, count, folder):
    r = praw.Reddit(client_id="Oez4fMric1z1uQ", client_secret="3-IOEjlgneiGBeNT02yeZ3TDLL1asw", user_agent="idk")
    counter = 0
    sub = r.subreddit(subreddit).hot(limit=count)
    temp_dict = []
    if folder != "":
        folder = folder + "/"
    for post in sub:
        if post.is_video and not post.over_18:
            #print(post.media['reddit_video'])
            vid_link = post.media['reddit_video']['fallback_url']
            audio_link = f'{vid_link.split("_")[0]}_audio.mp4'
            #print(audio_link)
            #print(vid_link)

            print(f'{folder}{post.title}.mp4')
            try:
                if ":" in post.title:
                    title = post.title.replace(":", "(colon)")
                else:
                    title = post.title
                urllib.request.urlretrieve(vid_link, f'{folder}{title}.mp4')
                urllib.request.urlretrieve(audio_link, f'{folder}{title}.mp3')
                vid = mpe.VideoFileClip(f'{folder}{title}.mp4')
                audio = mpe.AudioFileClip(f'{folder}{title}.mp3')
                combined_vid = vid.set_audio(audio)
                combined_vid.write_videofile(f'{folder}final {title}.mp4')
                temp_dict.append({"video_title": f'{folder}final {title}.mp4',
                                  "duration": post.media['reddit_video']["duration"],
                                 "used": False, "url": post.url, "source": "reddit", "score": post.score, "tags": []})
                counter +=1
                print(f"-----DOWNLOADED VIDEO {counter} OF {count}-----")
            except:
                print("Exception at download")

    with open("videos.json", "r") as json_file:
        data = json.load(json_file)
        video_list = []
        for i in data["data"]:
            video_list.append(i["video_title"])
        for i in temp_dict:
            #print(i["video_title"] in video_list)
            if not i["video_title"] in video_list:
                data["data"].insert(0,i)
                data["total_duration"] += i["duration"]
                data["usable_duration"] += i["duration"]

    with open("videos.json", "w") as json_f:
        json.dump(data, json_f, indent=2)

