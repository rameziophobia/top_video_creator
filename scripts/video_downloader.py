import requests
import json
import os
from config import FIRST_VIDEO, LAST_VIDEO
from video_downloader_yt import downloadFile

test_url = "https://static-gamespotvideo.cbsistatic.com/vr/2016/12/03/Trailer_Persona5_ThePhantomThieves_20161203_4000.mp4"

THRESHOLD = 300


def download_video(name, url, playlist_urls):
    size_header = requests.get(url, stream=True).headers['Content-length']
    size = int(size_header) // 1024 // 1024
    print(f"SIZE OF VIDEO ID {size} MB")

    for u in playlist_urls:
        if size and size < THRESHOLD and playlist_urls:
            break
        size_header = requests.get(u, stream=True).headers['Content-length']
        size = int(size_header) // 1024 // 1024
        print(size)
        url = u

    if size and size <= THRESHOLD:
        response = requests.get(url)
        name = "../videos/" + name
        print(name)
        write_file(name, response)

    else:
        downloadFile(name)


def write_file(name, response):
    with open(name + ".mp4", 'wb') as f:
        print("Downloading.....")
        for chunk in response.iter_content(chunk_size=255):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
        print("Done")


def download_videos():
    with open("output.json") as json_file:
        data = json.load(json_file)
        for game in data[FIRST_VIDEO:LAST_VIDEO]:
            if os.path.exists(r'../videos/' + game['filename'] + '.mp4') exists():
                continue
            if game['video_found'] or game["playlist_found"]:
                print(f"downloading {game['name']} {game['video_url']}")
                playlist_vids = game.get('playlist_videos', [])
                download_video(game['filename'],
                               game['video_url'], playlist_vids)
                print(f"finished {game['name']}")
            else:
                downloadFile(game['filename'])
