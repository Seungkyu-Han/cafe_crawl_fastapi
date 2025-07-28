from pydantic import BaseModel

from cafes.cafeEnum import Cafes

class CafeCrawlReq(BaseModel):
    cafeType: Cafes
    isCrawlImg: bool

class CafeCrawlRes(BaseModel):
    menus: list[tuple[str, str]]