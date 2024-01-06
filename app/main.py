from fastapi import FastAPI

from app.routers import book_router, login_router, user_router

app = FastAPI(title="FastAPI Template")

app.include_router(user_router)
app.include_router(login_router)
app.include_router(book_router)
