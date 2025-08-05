from fastapi import FastAPI

from cafe import cafe_controller

app = FastAPI()

app.include_router(cafe_controller.router)
