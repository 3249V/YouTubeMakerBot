import praw
import urllib
import moviepy.editor as mpe
import json
import random
#dankvideos, memevideos
r = praw.Reddit(client_id="Oez4fMric1z1uQ", client_secret="3-IOEjlgneiGBeNT02yeZ3TDLL1asw", user_agent="idk")


def get_videos(subreddit, count, folder):

    sub = r.subreddit(subreddit).hot(limit=count)
    temp_dict = []
    if folder != "":
        folder = folder + "/"
    for post in sub:
        if post.is_video:
            #print(post.media['reddit_video'])
            vid_link = post.media['reddit_video']['fallback_url']
            audio_link = f'{vid_link.split("_")[0]}_audio.mp4'
            #print(audio_link)
            #print(vid_link)

            print(f'{folder}{post.title}.mp4')
            try:
                urllib.request.urlretrieve(vid_link, f'{folder}{post.title}.mp4')
                urllib.request.urlretrieve(audio_link, f'{folder}{post.title}.mp3')
                vid = mpe.VideoFileClip(f'{folder}{post.title}.mp4')
                audio = mpe.AudioFileClip(f'{folder}{post.title}.mp3')
                combined_vid = vid.set_audio(audio)
                combined_vid.write_videofile(f'{folder}final {post.title}.mp4')
                temp_dict.append({"video_title": f'{folder}final {post.title}.mp4',
                                  "duration": post.media['reddit_video']["duration"],
                                 "used": False})
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

    with open("videos.json", "w") as json_f:
        json.dump(data, json_f, indent=2)

def combine_videos(length):
    with open("videos.json", "r") as json_file:
        data = json.load(json_file)
        video_list = []
        clips = []
        temp_length = length
        while temp_length > 0:
            temp = random.choice(data["data"])
            if not temp["used"]:
                print(data["data"].index(temp))
                data["data"][data["data"].index(temp)]["used"] = True
                clips.append(mpe.VideoFileClip(temp["video_title"]))
                video_list.append(temp["video_title"])
                temp_length -= temp["duration"]
            else:
                print("USED")
        print(video_list)
        print(length-temp_length)
        final_video = mpe.concatenate_videoclips(clips, method='compose')
        final_video.write_videofile(f"Final Video{data['videos']}.mp4")
        data['videos'] += 1
    with open("videos.json", "w") as json_f:
        json.dump(data, json_f, indent=2)


get_videos("dankvideos", 100,"meme storage")
combine_videos(120)