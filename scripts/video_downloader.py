import requests
import json
test_url = "https://static-gamespotvideo.cbsistatic.com/vr/2016/12/03/Trailer_Persona5_ThePhantomThieves_20161203_4000.mp4"


def downloadfile(name, url):
    name = "../videos/" + name
    print(name)
    r = requests.get(url)
    print("****Connected****")
    f = open(name, 'wb')
    print("Downloading.....")
    for chunk in r.iter_content(chunk_size=255):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
    print("Done")
    f.close()


with open("output.json") as json_file:
    data = json.load(json_file)
    for game in data[5: 8]:
        if game['video_found']:
            print(f"downloading {game['name']} {game['video_url']}")
            downloadfile(game['filename'], game['video_url'])
            print(f"finished {game['name']}")
