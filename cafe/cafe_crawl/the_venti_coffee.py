import requests
from bs4 import BeautifulSoup, ResultSet
from cafe.cafe_dto import CafeCrawlRes, Menu, Category, MenuCategory
from cafe.cafe_crawl.cafe_crawler import CafeCrawler


class TheVentiCafeCrawler(CafeCrawler):

    BASE_URL = 'https://www.theventi.co.kr'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    def category_link_mapper(self, link: str) -> list[tuple[str, str]]:

        res = requests.get(link, headers=self.headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html.parser")

        result: list[tuple[str, str]] = []

        for a_tag in soup.select("ul.tab.box li a"):
            name = a_tag.get_text(strip=True)
            href = a_tag.get("href")

            result.append((name, f'{link}{href}'))

        return result


    def crawl_menu(self) -> CafeCrawlRes:

        category_link_map: list[tuple[str, str]] = self.category_link_mapper(f'{self.BASE_URL}/new2022/menu/all.html')

        category_sort_order = 1
        menu_sort_order = 1
        menu_categories: list[MenuCategory] = []

        for category_name, category_url in category_link_map:
            res = requests.get(category_url, headers=self.headers)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, "html.parser")

            menus: list[Menu] = []

            for item in soup.select("li.item"):
                img_tag = item.select_one(".img_bx img")
                img = img_tag.get('src')

                name_tag = item.select_one(".txt_bx p.tit")
                name = name_tag.get_text(strip=True) if name_tag else None

                menus.append(Menu(nameKr=name, nameEn='', img=img, order=menu_sort_order))
                menu_sort_order += 1

            menu_categories.append(MenuCategory(category=Category(name=category_name, order=category_sort_order), menus=menus))
            category_sort_order += 1
        return CafeCrawlRes(menuCategories=menu_categories)
