from moviepy.editor import *
import json
clips = []
names = []


def addText(clip, name):
    txt_clip = (TextClip(name, fontsize=80, color='white')
                .set_position(('left', 'bottom'))
                .set_duration(8))
    clip = CompositeVideoClip([clip, txt_clip])
    return clip


def addVideos(clips):

    i = 0

    for clip in clips:
        clip = clip.resize((1920, 1080))
        clips[i] = addText(clip, names[i])

        i = i+1
    final = concatenate_videoclips([clip for clip in clips])

    # final = concatenate_videoclips([clips[0], clips[1]])

    final.write_videofile("../videos/final.mp4", codec="libx264")


def createVideo():
    with open("output.json") as json_file:
        data = json.load(json_file)
        i = 0
        for game in data[5:7]:
            clips.append(VideoFileClip(f"../videos/{game['filename']}"))
            clips[i] = clips[i].subclip(round(clips[i].duration * 0.35),
                                        round(clips[i].duration * 0.35)+10)
            i = i+1
            names.append(game['name'])

    addVideos(clips)


if __name__ == "__main__":

    with open("output.json") as json_file:
        data = json.load(json_file)
        i = 0
        for game in data[9:12]:
            clips.append(VideoFileClip(f"../videos/{game['filename']}"))
            clips[i] = clips[i].subclip(round(clips[i].duration * 0.35),
                                        round(clips[i].duration * 0.35)+10)
            i = i+1
            names.append(game['name'])

    addVideos(clips)
