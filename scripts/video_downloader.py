import requests

test_url = "https://static-gamespotvideo.cbsistatic.com/vr/2016/12/03/Trailer_Persona5_ThePhantomThieves_20161203_4000.mp4"


def downloadfile(name, url):
    name = "../videos/" + name + ".mp4"
    r = requests.get(url)
    print("****Connected****")
    f = open(name, 'wb')
    print("Downloading.....")
    for chunk in r.iter_content(chunk_size=255):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
    print("Done")
    f.close()


downloadfile("Persona5", test_url)

