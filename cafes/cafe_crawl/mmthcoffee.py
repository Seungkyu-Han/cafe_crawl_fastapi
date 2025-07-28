import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = 'https://mmthcoffee.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def crawl_mmth_menus() -> list[tuple[str, str]]:

    data = requests.get(f'{BASE_URL}/sub/menu/list.html', headers = headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    items = soup.select('ul.clear > li')

    menu_list: list[tuple[str, str]] = []

    for item in items:
        name_kr_tag: Tag = item.select_one('strong')
        img_tag: Tag = item.select_one('img')

        if not (name_kr_tag and img_tag):
            continue

        name_kr = name_kr_tag.get_text(strip = True)
        img_src = img_tag['src']

        menu_list.append((name_kr, img_src))

    return menu_list