from moviepy.editor import *
import json
from config import FIRST_VIDEO, LAST_VIDEO

clips = []
names = []
LIST_SIZE = LAST_VIDEO - FIRST_VIDEO + 1


def addText(clip, name):
    global LIST_SIZE
    txt_clip = (TextClip(f"{LIST_SIZE} : {name}", fontsize=70, color='white')
                .set_position(('left', 'bottom'))
                .set_duration(8))
    clip = CompositeVideoClip([clip, txt_clip])
    LIST_SIZE -= 1
    return clip


def addVideos(clips):

    i = 0

    for clip in clips:
        clip = clip.resize((1920, 1080))
        clips[i] = addText(clip, names[i])
        i = i+1

    final = concatenate_videoclips([clip for clip in clips])

    final.write_videofile("../videos/final.mp4", codec="libx264")


def createVideo():
    with open("output.json") as json_file:
        data = json.load(json_file)
        i = 0
        for game in data[FIRST_VIDEO:LAST_VIDEO]:
            clips.append(VideoFileClip(f"../videos/{game['filename']}.mp4"))
            clips[i] = clips[i].subclip(round(clips[i].duration * 0.35),
                                        round(clips[i].duration * 0.35)+10)
            i = i+1
            names.append(game['name'])

    addVideos(clips)


if __name__ == "__main__":
    LIST_SIZE = LAST_VIDEO - FIRST_VIDEO + 1
    createVideo()
