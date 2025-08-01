import requests
from bs4 import BeautifulSoup
from cafes.cafeDto import CafeCrawlRes, Menu, Category, MenuCategory

BASE_URL = 'https://mmthcoffee.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def crawl_mmth_menus() -> CafeCrawlRes:

    category_cur_order = 1

    data = requests.get(f'{BASE_URL}/sub/menu/list.html', headers = headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    menu_categories: list[MenuCategory] = []

    for cate_div in soup.select("div.cate"):
        category = cate_div.select_one("div.c_tit strong").text.strip()
        menus: list[Menu] = []

        menu_cur_order = 1

        for li in cate_div.select("ul.clear > li"):
            name_kr = li.select_one("div.txt_wrap strong").text.strip()
            name_en = li.select_one("div.txt_wrap p.eng").text.strip()
            img = li.select_one("div.img_wrap img")["src"]

            menus.append(Menu(nameKr=name_kr, nameEn=name_en, img=img, order=menu_cur_order))

            menu_cur_order += 1

        menu_categories.append(MenuCategory(category=Category(name = category, order = category_cur_order), menus=menus))
        category_cur_order += 1

    print(menu_categories)

    return CafeCrawlRes(menuCategories=menu_categories)