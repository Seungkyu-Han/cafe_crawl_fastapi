from pydantic import BaseModel

from cafes.cafeEnum import CafeType

class CafeCrawlReq(BaseModel):
    cafeType: CafeType

class Menu(BaseModel):
    nameKr: str
    nameEn: str
    img: str
    order: int

class MenuCategory(BaseModel):
    category: str
    menus: list[Menu]

class CafeCrawlRes(BaseModel):
    menuCategories: list[MenuCategory]
