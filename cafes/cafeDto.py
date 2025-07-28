from pydantic import BaseModel

from cafes.cafeEnum import CafeType

class CafeCrawlReq(BaseModel):
    cafeType: CafeType
    isCrawlImg: bool

class CafeCrawlRes(BaseModel):
    menus: list[tuple[str, str]]