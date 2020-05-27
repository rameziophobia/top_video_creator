from bs4 import BeautifulSoup
from requests import get
import json
import re
from config import *

test_url = "https://www.metacritic.com/browse/games/release-date/coming-soon/xboxone/date"
BASE_URL = "https://www.metacritic.com"
HREF_CLASS = "basic_stat product_title"
TABLE_CLASS = "clamp-list condensed"
REQUEST_HEADER = {'User-Agent': 'Mozilla/5.0'}


def scrap_compact():
    soup = get_soup(test_url)
    games_info = []
    game_divs = soup.find_all('div', class_=HREF_CLASS)
    game_divs = game_divs[:-8]

    position = 0
    for div in game_divs:
        game = get_game_info(div)
        if(game['release_date'][0] != "Jun"):
            continue
        game['position'] = position
        position += 1
        games_info.append(game)
        print(f"finished {game['name']} -rating fetch-")

    for game in games_info:
        add_game_video(game)

    print('all done')
    write_json(games_info)


def scrap_cards():
    games_info = []
    for page in range(CARDS_START_PAGE, CARDS_TARGET_PAGE + 1):
        curr_page = f"{CARDS_URL_START}&page={page}"
        soup = get_soup(curr_page)

        tables = soup.find_all('table', class_=TABLE_CLASS)
        for table in tables:
            entries = table.find_all('tr')
            games_info.extend([process_table_entry(entry) for entry in entries])

        print(f'page {page}')

    games_info = list({each['name']: each for each in games_info}.values())
    # todo the above code gets the unique games but loses platform info

    for index, game in enumerate(games_info):
        game['position'] = index
        add_game_video(game)
    write_json(games_info)


def process_table_entry(entry):
    game = dict()
    game['rating'] = entry.select_one('td a div').text
    title_div = entry.find('a', class_='title')
    game['url'] = BASE_URL + title_div['href']
    game['name'] = title_div.find('h3').text
    game['filename'] = "".join(
            x for x in game['name'] if (x.isalnum() or x == " "))
    platform_div = entry.find('div', class_='platform')

    game['platform'] = platform_div.find('span', class_='data').text.strip()
    game['release_date'] = platform_div.next_sibling.next_sibling.text.split()
    game['release_date'][1] = game['release_date'][1][:-1]
    print(f"finished {game['name']} -rating fetch-")
    return game


def get_game_info(div):
    game = {}
    href_parent = div.find('a')
    if href_parent:
        game['url'] = BASE_URL + href_parent['href']
        game['name'] = href_parent.text.strip()
        game['filename'] = "".join(
            x for x in game['name'] if (x.isalnum() or x == " "))
    rating1_div = div.next_sibling.next_sibling
    game['rating'] = rating1_div.find('div').text
    rating2_div = rating1_div.next_sibling.next_sibling
    game['user_rating'] = rating2_div.text.strip().split()[1]
    rating2_div = rating1_div.next_sibling.next_sibling
    game['release_date'] = rating2_div.text.strip().split()[-2:]
    return game


def add_game_video(game):
    soup = get_soup(game['url'])
    video_wrapper_div = soup.find('div', id='videoContainer_wrapper')
    if video_wrapper_div:
        game['video_url'] = video_wrapper_div.attrs['data-mcvideourl']
        game['video_url'].replace(r'/gsc', '')
        game['video_found'] = True
    else:
        game['video_found'] = False

    playlist_pattern = re.compile(
        r'MetaC\.Video\.addToPlaylist.', re.MULTILINE | re.DOTALL)
    playlist_div = soup.find("script", text=playlist_pattern)
    if playlist_div:
        vid_url_pattern = re.compile(r'https.*\.mp4')
        playlist_videos = re.findall(vid_url_pattern, playlist_div.string)
        game['playlist_videos'] = playlist_videos
        game['playlist_found'] = True
    else:
        game['playlist_found'] = False
    print(f"finished {game['name']}  -video fetch-")


def get_soup(store_site):
    page = get(store_site, headers=REQUEST_HEADER)
    soup = BeautifulSoup(page.content, features="html.parser")
    return soup


def write_json(games_list):
    with open('output1.json', 'w+') as handle:
        # reverse list for countdown
        # games_list = list(reversed(games_list))
        json.dump(games_list, handle, indent=4)


if __name__ == "__main__":
    scrap_cards()
