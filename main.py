from fastapi import FastAPI

import cafes.cafeDto
from cafes.cafeService import retrieve_menu

app = FastAPI()

@app.post("/cafe")
async def crawl_cafe_menu_api(cafe_crawl_req: cafes.cafeDto.CafeCrawlReq) -> cafes.cafeDto.CafeCrawlRes:

    return retrieve_menu(cafe_type=cafe_crawl_req.cafeType, is_crawl_img=cafe_crawl_req.isCrawlImg)
