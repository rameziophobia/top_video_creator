from moviepy.editor import *

clips = []
names = ["1", "2", "3"]


def addText(clip, name):
    txt_clip = (TextClip(name, fontsize=50, color='white')
                .set_position(('left', 'bottom'))
                .set_duration(2))
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


if __name__ == "__main__":
    clip1 = VideoFileClip("../videos/Persona5.mp4")
    clip2 = VideoFileClip("../videos/BloodBorne.mp4")
    clip3 = VideoFileClip("../videos/BloodBorne.mp4")
    clip1 = clip1.subclip(60, 62)
    clip2 = clip2.subclip(60, 62)
    clip3 = clip3.subclip(40, 50)
    clips.append(clip1)
    clips.append(clip2)
    clips.append(clip3)
    addVideos(clips)
