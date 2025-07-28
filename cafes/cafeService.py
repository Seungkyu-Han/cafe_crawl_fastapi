import cafes.cafeDto
import cafes.cafeEnum
from cafes.cafeDto import CafeCrawlRes
from cafes.cafeEnum import CafeType
import cafe_crawl.mmthcoffee
from http.client import HTTPException


def retrieve_menu(cafe_type: CafeType, is_crawl_img: bool) -> cafes.cafeDto.CafeCrawlRes:

    menus: list[tuple[str, str]]

    if cafe_type == CafeType.MAMMOTH:
        menus = cafe_crawl.mmthcoffee.crawl_mmth_menus()

    else:
        raise HTTPException()

    if not is_crawl_img:
        menus = [(name, "") for name, _ in menus]

    return CafeCrawlRes(menus=menus)