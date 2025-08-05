from fastapi import APIRouter, Depends, Query

from cafe.cafe_dto import CafeCrawlRes
from cafe.cafe_enum import CafeType
from cafe.cafe_service import CafeService, get_cafe_service

router = APIRouter()



@router.get("/cafe", response_model=CafeCrawlRes)
async def crawl_cafe_menu_api(cafe_type: CafeType = Query(), cafe_service: CafeService = Depends(get_cafe_service)) -> CafeCrawlRes:

    return cafe_service.retrieve_menu(cafe_type=cafe_type)
