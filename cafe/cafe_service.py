from fastapi import Depends

from cafe.cafe_crawl.cafe_crawler import CafeCrawler
from cafe.cafe_crawl.compose_coffee import ComposeCafeCrawler
from cafe.cafe_crawl.mgc_coffee import MgcCafeCrawler
from cafe.cafe_crawl.mmth_coffee import MmthCafeCrawler
from cafe.cafe_crawl.the_venti_coffee import TheVentiCafeCrawler
from cafe.cafe_dto import CafeCrawlRes
from cafe.cafe_enum import CafeType

def get_cafe_crawler() -> dict[CafeType, CafeCrawler]:
    return {
        CafeType.MGC: MgcCafeCrawler(),
        CafeType.MAMMOTH: MmthCafeCrawler(),
        CafeType.COMPOSE: ComposeCafeCrawler(),
        CafeType.THE_VENTI: TheVentiCafeCrawler()
    }

class CafeService:
    def __init__(self, crawlers: dict[CafeType, CafeCrawler]= Depends(get_cafe_crawler)):
        self.crawlers = crawlers

    def retrieve_menu(self, cafe_type: CafeType) -> CafeCrawlRes:
        return self.crawlers[cafe_type].crawl_menu()

def get_cafe_service(crawlers: dict[CafeType, CafeCrawler] = Depends(get_cafe_crawler)) -> CafeService:
    return CafeService(crawlers)