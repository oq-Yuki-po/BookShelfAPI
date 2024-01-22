from fastapi import APIRouter, Depends

from app.models import AuthorModel, BookAuthorModel, BookModel, session
from app.routers.setting import AppRoutePermissions, AppRoutes
from app.schemas.exceptions import (
    BookIsbnInvalidFormatExceptionOut,
    DuplicateBookISBNExceptionOut,
    GoogleBooksApiExceptionOut,
    NotEnoughPermissionsExceptionOut,
)
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
ROUTER_PERMISSIONS = AppRoutePermissions.Books


@router.post(BOOK_ROUTERS.POST_GOOGLE_BOOKS_URL,
             response_model=GoogleBooksApiSaveOut,
             responses={
                 400: {"model": BookIsbnInvalidFormatExceptionOut,
                       "description": "Book ISBN Invalid Format"},
                 403: {"model": NotEnoughPermissionsExceptionOut,
                       "description": "Not Enough Permissions"},
                 409: {"model": DuplicateBookISBNExceptionOut,
                       "description": "Duplicate Book ISBN"},
                 500: {"model": GoogleBooksApiExceptionOut,
                       "description": "Google Books API Error"}
             },
             status_code=200)
async def save_google_books(books_google_books_api_save_in: BooksGoogleBooksApiSaveIn,
                            current_user: TokenData = Depends(LoginService.verify_token))\
        -> GoogleBooksApiSaveOut:
    """
    Save book from Google Books API

    ```
    Parameters
    ----------
    books_google_books_api_save_in: BooksGoogleBooksApiSaveIn
        BooksGoogleBooksApiSaveIn schema
    current_user: TokenData
        TokenData schema

    Returns
    -------
    GoogleBooksApiSaveOut
        GoogleBooksApiSaveOut schema

    Raises
    ------
    BookIsbnInvalidFormatException
        if book isbn format is invalid
    NotEnoughPermissionsException
        if user does not have enough permissions
    DuplicateBookISBNException
        if book isbn already exists
    GoogleBooksApiException
        if google books api error occurred
    ```
    """
    # check permissions
    LoginService.verify_permission(required_permissions=ROUTER_PERMISSIONS.POST_GOOGLE_BOOKS,
                                   token=current_user)

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

    return GoogleBooksApiSaveOut(title=book_data.title,
                                 authors=book_data.authors,
                                 published_at=book_data.published_at,
                                 cover_image_base64=ImageBase64Service.encode(image_path=cover_image_path))
