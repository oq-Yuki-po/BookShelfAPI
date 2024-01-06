from fastapi import APIRouter, Depends

from app.exceptions.exceptions import NotEnoughPermissionsException
from app.models import AuthorModel, BookAuthorModel, BookModel, session
from app.routers.setting import AppRoutePermissions, AppRoutes
from app.schemas.requests import BooksGoogleBooksApiSaveIn
from app.schemas.responses import GoogleBooksApiSaveOut
from app.services.google_books_api_service import GoogleBooksApiService
from app.services.image_service import ImageBase64Service
from app.services.login_service import LoginService, TokenData

router = APIRouter(
    prefix=AppRoutes.Books.PREFIX,
    tags=[AppRoutes.Books.TAG]
)
BOOK_ROUTERS = AppRoutes.Books
BOOK_ROUTER_PERMISSIONS = AppRoutePermissions.Books


@router.post(BOOK_ROUTERS.POST_GOOGLE_BOOKS_URL,
             response_model=GoogleBooksApiSaveOut,
             status_code=200)
async def save_google_books(books_google_books_api_save_in: BooksGoogleBooksApiSaveIn,
                            current_user: TokenData = Depends(LoginService.verify_token)) -> GoogleBooksApiSaveOut:

    # check user permissions
    if current_user.role not in BOOK_ROUTER_PERMISSIONS.PostGoogleBooks.PERMISSIONS:
        raise NotEnoughPermissionsException()

    # fetch book data from google books api
    book_data = GoogleBooksApiService.fetch_book_data(isbn=books_google_books_api_save_in.isbn)

    # save author
    for author in book_data.authors:
        AuthorModel.save(name=author)

    # save cover image
    cover_image_path = GoogleBooksApiService.save_cover_image(google_book_schema=book_data,
                                                              isbn=books_google_books_api_save_in.isbn)
    # save book
    book_model = BookModel(title=book_data.title,
                           isbn=books_google_books_api_save_in.isbn,
                           cover_path=cover_image_path,
                           published_at=book_data.published_at)
    new_book_model = book_model.save_google_books_api()

    # save book author
    author_models = AuthorModel.fetch_by_names(names=book_data.authors)

    for author_model in author_models:
        BookAuthorModel.save(book_id=new_book_model.id, author_id=author_model.id)

    session.commit()

    return GoogleBooksApiSaveOut(message='book saved successfully',
                                 title=book_data.title,
                                 authors=book_data.authors,
                                 published_at=book_data.published_at,
                                 cover_image_base64=ImageBase64Service.encode(image_path=cover_image_path))
