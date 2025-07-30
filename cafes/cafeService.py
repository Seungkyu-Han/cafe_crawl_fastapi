import cafes.cafeDto
import cafes.cafeEnum
from cafes.cafeDto import CafeCrawlRes
from cafes.cafeEnum import CafeType
from cafes.cafe_crawl.mmthcoffee import crawl_mmth_menus
from http.client import HTTPException


def retrieve_menu(cafe_type: CafeType) -> cafes.cafeDto.CafeCrawlRes:

    result: CafeCrawlRes

    if cafe_type == CafeType.MAMMOTH:
        result = crawl_mmth_menus()

    else:
        raise HTTPException()

    return result