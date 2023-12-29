from fastapi import FastAPI

from app.routers import user_router

app = FastAPI(title="FastAPI Template")

app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
