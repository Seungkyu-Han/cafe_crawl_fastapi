import requests
from bs4 import BeautifulSoup, ResultSet
from cafe.cafe_dto import CafeCrawlRes, Menu, Category, MenuCategory
from cafe.cafe_crawl.cafe_crawler import CafeCrawler


class MgcCafeCrawler(CafeCrawler):

    BASE_URL = 'https://www.mega-mgccoffee.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    def make_menu_url(self, category: int, page: int) -> str:
        return f'{self.BASE_URL}/menu/menu.php?page={page}&category={category}&menu_category1=1&menu_category2=1'

    def get_category_value(self) -> list[tuple[int, str]]:
        res = requests.get(f'{self.BASE_URL}/menu/?menu_category1=1&menu_category2=1', headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")
        checkboxes = soup.select("div.checkbox_wrap.list_checkbox")

        result: list[tuple[int, str]] = []

        for checkbox in checkboxes:
            input_tag = checkbox.find("input", {"type": "checkbox"})
            value: int = int(input_tag.get("value"))

            label_text = checkbox.find("div", class_="checkbox_text").get_text(strip=True)

            result.append((value, label_text))

        return result

    def crawl_menu(self) -> CafeCrawlRes:
        menu_categories: list[MenuCategory] = []
        category_value_map: list[tuple[int, str]] = self.get_category_value()

        for category_value, category_name in category_value_map:
            menu_cur_order = 1
            menus: list[Menu] = []
            for cur_page in range(1, 100):
                res = requests.get(self.make_menu_url(category=category_value, page=cur_page), headers=self.headers)

                soup = BeautifulSoup(res.text, "html.parser")

                items: ResultSet = soup.select('.cont_gallery_list_box')

                if len(items) == 0:
                    break

                for item in items:
                    name_kr = item.select_one('.cont_text_title b').get_text(strip=True)
                    name_en = item.select_one('.cont_text_info .text1').get_text(strip=True)
                    img = item.select_one('img')['src']

                    menus.append(Menu(nameKr=name_kr, nameEn=name_en, img=img, order=menu_cur_order))

                    menu_cur_order += 1

            menu_categories.append(
                MenuCategory(category=Category(name=category_name, order=category_value), menus=menus))

        return CafeCrawlRes(menuCategories=menu_categories)
