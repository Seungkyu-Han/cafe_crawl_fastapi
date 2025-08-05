from pydantic import BaseModel

from cafe.cafe_enum import CafeType

class CafeCrawlReq(BaseModel):
    cafeType: CafeType

class Category(BaseModel):
    name: str
    order: int

class Menu(BaseModel):
    nameKr: str
    nameEn: str
    img: str
    order: int

class MenuCategory(BaseModel):
    category: Category
    menus: list[Menu]

class CafeCrawlRes(BaseModel):
    menuCategories: list[MenuCategory]
