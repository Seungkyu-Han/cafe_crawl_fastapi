from fastapi import FastAPI, Query

import cafes.cafeDto
from cafes.cafeEnum import CafeType
from cafes.cafeService import retrieve_menu

app = FastAPI()

@app.get("/cafe")
async def crawl_cafe_menu_api(cafe_type: CafeType = Query()) -> cafes.cafeDto.CafeCrawlRes:

    return retrieve_menu(cafe_type=cafe_type)
