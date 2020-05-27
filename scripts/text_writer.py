from config import *
import json
from datetime import timedelta


def write_text_file():
    START_TIME = timedelta(seconds=0)
    with open("output.json") as json_file:
        data = json.load(json_file)
        text_file = open("text.txt", "w")
        text = ""
        for game in data[FIRST_VIDEO:LAST_VIDEO]:
            if game['release_date'][0] == MONTH[TARGET_MONTH] or (not FILTER_BY_MONTH):
                text += f"{game['release_date'][1]} {game['release_date'][0]} -- {game['name']}: {START_TIME}\n"
                START_TIME += timedelta(seconds=int(game['clip_duration']))
        text_file.write(text)
        text_file.close()


if __name__ == "__main__":
    write_text_file()

