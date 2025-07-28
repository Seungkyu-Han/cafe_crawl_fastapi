from fastapi import FastAPI

import cafes.cafeDto

app = FastAPI()

@app.post("/cafe")
async def crawl_cafe_menu(cafe_crawl_req: cafes.cafeDto.CafeCrawlReq) -> cafes.cafeDto.CafeCrawlRes:
    print(cafe_crawl_req)
    return None
