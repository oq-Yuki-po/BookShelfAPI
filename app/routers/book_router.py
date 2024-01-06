from fastapi import APIRouter

from app.routers.setting import AppRoutes

router = APIRouter(
    prefix=AppRoutes.Books.PREFIX,
    tags=[AppRoutes.Books.TAG]
)
