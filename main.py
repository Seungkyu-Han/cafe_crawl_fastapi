from fastapi import FastAPI

app = FastAPI()

@app.post("/cafe")
async def crawl_cafe_menu(name: str):
    return {"message": f"Hello {name}"}
