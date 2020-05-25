from moviepy.editor import *
import json
from config import *

clips = []
names = []
date = []
LIST_SIZE = LAST_VIDEO - FIRST_VIDEO


def addText(clip, name, date):
    global LIST_SIZE
    txt_clip = (TextClip(f"{name}: {date}", fontsize=70, color='white', font="Amiri-bold")
                .set_position(('left', 'bottom'))
                .set_duration(int(SINGLE_VIDEO_LENGTH.seconds) - 2))
    clip = CompositeVideoClip([clip, txt_clip])
    LIST_SIZE -= 1
    return clip


def addVideos(clips):
    i = 0
    for clip in clips:
        clip = clip.resize((1920, 1080))
        clips[i] = addText(clip, names[i], date[i])
        i = i + 1

    clips.append(end_screen_clip())
    final = concatenate_videoclips(clips)

    final.write_videofile("../videos/final.mp4",
                          codec="libx264", threads=8, fps=30)


def createVideo():
    with open("output.json") as json_file:
        data = json.load(json_file)

        for game in data[FIRST_VIDEO:LAST_VIDEO]:
            if game['release_date'][0] == MONTH[TARGET_MONTH] or (not FILTER_BY_MONTH):
                print(game['filename'])
                clip = VideoFileClip(f"../videos/{game['filename']}.mp4")
                clip = clip.subclip(round(clip.duration * CUT_PERCENT),
                                    round(clip.duration * CUT_PERCENT) + int(SINGLE_VIDEO_LENGTH.seconds))
                clips.append(clip)
                names.append(game['name'])
                date.append(
                    f"{game['release_date'][1]} {game['release_date'][0]}")
    print(len(clips))
    addVideos(clips)
  


def end_screen_clip(size=(1920, 1080), duration=15, fps=30, color=(0, 0, 0)):
    return ColorClip(size, color, duration=duration)


if __name__ == "__main__":
    LIST_SIZE = LAST_VIDEO - FIRST_VIDEO
    createVideo()
