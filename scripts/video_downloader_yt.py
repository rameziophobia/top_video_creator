from pytube import YouTube
from bs4 import BeautifulSoup
from list_scrapper import get_soup
import re
NAME = "frostpunk"
HREF_ID = "video-title"
IDENTFIER = "/watch"
BASE_URL = "https://www.youtube.com"


def downloadFile(name):
    url = getLink(name)
    yt = YouTube(url)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first()
    yt.download("../videos/", filename=name)


def getLink(name):
    url = f"https://www.youtube.com/results?search_query={name}+trailer"
    soup = get_soup(url)
    pattern = re.compile(f'.*{IDENTFIER}.*')
    videoInfo = soup.find(
        "a", href=pattern)
    videoUrl = BASE_URL+videoInfo["href"]
    print(videoUrl)
    return videoUrl


if __name__ == "__main__":
    getLink(NAME)
