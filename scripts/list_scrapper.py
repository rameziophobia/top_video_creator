from bs4 import BeautifulSoup
from requests import get
import json

# from moviepy.editor import *
#
# video = VideoFileClip("../videos/Persona5.mp4").subclip(50,60)
# txt_clip = (TextClip("My Holidays 2013", fontsize=70, color='white')
#             .set_position('center')
#             .set_duration(10))
# result = CompositeVideoClip([video, txt_clip]) # Overlay text on video
# result.write_videofile("../videos/myHolidays_edited.mp4",fps=25) # Many options...

test_url = "https://www.metacritic.com/browse/games/score/metascore/all/ps4/filtered"
BASE_URL = "https://www.metacritic.com"
HREF_CLASS = "basic_stat product_title"
REQUEST_HEADER = {'User-Agent': 'Mozilla/5.0'}


def main():
    soup = get_soup(test_url)
    games_info = []
    game_divs = soup.find_all('div', class_=HREF_CLASS)
    game_divs = game_divs[:-8]

    position = 0
    for div in game_divs:
        game = get_game_info(div, position)
        games_info.append(game)
        print(f"finished {game['name']} -rating fetch-")

    for game in games_info:
        add_game_video(game)

    print('all done')
    write_json(games_info)


def get_game_info(div, position):
    game = {}
    href_parent = div.find('a')
    if href_parent:
        game['url'] = BASE_URL + href_parent['href']
        game['name'] = href_parent.text.strip()
        game['position'] = position
        position += 1
    rating1_div = div.next_sibling.next_sibling
    game['rating'] = rating1_div.find('div').text
    rating2_div = rating1_div.next_sibling.next_sibling
    game['user_rating'] = rating2_div.text.strip().split()[1]
    return game


def add_game_video(game):
    soup = get_soup(game['url'])
    video_wrapper_div = soup.find('div', id='videoContainer_wrapper')
    if video_wrapper_div:
        game['video_url'] = video_wrapper_div.attrs['data-mcvideourl']
        game['video_found'] = True
    else:
        game['video_found'] = False
    print(f"finished {game['name']}  -video fetch-")


def get_soup(store_site):
    page = get(store_site, headers=REQUEST_HEADER)
    soup = BeautifulSoup(page.content, features="html.parser")
    return soup


def write_json(my_dict):
    with open('output.json', 'w+') as handle:
        json.dump(my_dict, handle, indent=4)


if __name__ == "__main__":
    main()
