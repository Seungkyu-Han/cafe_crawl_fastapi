import requests
from bs4 import BeautifulSoup, ResultSet
from cafe.cafe_dto import CafeCrawlRes, Menu, Category, MenuCategory
from cafe.cafe_crawl.cafe_crawler import CafeCrawler


class ComposeCafeCrawler(CafeCrawler):

    BASE_URL = 'https://composecoffee.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    def category_link_mapper(self, link: str) -> list[tuple[str, str]]:

        res = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        result: list[tuple[str, str]] = []

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith("http") and "/menu/category/" in href:
                name = a_tag.get_text(strip=True)
                result.append((name, href))

        seen = set()
        unique_result = []
        for name, href in result:
            if href not in seen:
                seen.add(href)
                unique_result.append((name, href))

        return unique_result

    def get_last_page(self, soup: BeautifulSoup) -> int:

        page_numbers = []
        for link in soup.select(".page-link"):
            if link.text.strip().isdigit():
                page_numbers.append(int(link.text.strip()))
        return max(page_numbers) if page_numbers else 1


    def crawl_menu(self) -> CafeCrawlRes:

        category_link_map: list[tuple[str, str]] = self.category_link_mapper(f'{self.BASE_URL}/menu')
        menu_categories: list[MenuCategory] = []
        category_sort_order = 1


        for category_name, category_url in category_link_map:
            menu_sort_order = 1
            menus: list[Menu] = []
            res = requests.get(category_url, headers=self.headers)
            soup = BeautifulSoup(res.text, "html.parser")

            category_last_page = self.get_last_page(soup)

            for page in range(1, category_last_page + 1):
                url = f"{category_url}?page={page}"
                pres = requests.get(url, headers=self.headers)
                psoup = BeautifulSoup(pres.text, "html.parser")

                items = psoup.select(".itemBox")
                for item in items:
                    title_tag = item.select_one("h4.title") or item.select_one("h3.undertitle")
                    img_tag = item.select_one("img")

                    name_kr = title_tag.get_text(strip=True) if title_tag else None
                    img = img_tag["src"] if img_tag else None
                    if img and not img.startswith("http"):
                        img = self.BASE_URL.rstrip("/") + img

                    menus.append(Menu(nameKr=name_kr, nameEn='', img=img, order=menu_sort_order))

                    menu_sort_order += 1

            menu_categories.append(MenuCategory(category=Category(name=category_name, order=category_sort_order), menus=menus))
            category_sort_order += 1

        return CafeCrawlRes(menuCategories=menu_categories)
