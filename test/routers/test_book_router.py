import datetime
import os
from typing import List

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AuthorModel, BookAuthorModel, BookModel
from app.routers.setting import AppRoutePermissions, AppRoutes
from app.schemas.api import GoogleBookSchema
from app.schemas.requests import BooksGoogleBooksApiSaveIn
from app.schemas.responses import GoogleBooksApiSaveOut

TEST_URL = f"{AppRoutes.Books.PREFIX}"
TEST_PERMISSIONS = AppRoutePermissions.Books


def test_save_google_books_success(app_client: TestClient,
                                   db_session: Session,
                                   mocker,
                                   override_verify_token_dependency,
                                   encode_image_base64):
    """
    Test save google books
    """
    # Prepare
    with override_verify_token_dependency("admin"):

        test_isbn = "9784774193684"
        books_google_books_api_save_in = BooksGoogleBooksApiSaveIn(isbn=test_isbn)
        # Mock
        mocker.patch('app.services.google_books_api_service.GoogleBooksApiService.fetch_book_data',
                     return_value=GoogleBookSchema(title="test_title",
                                                   authors=["test_author 1", "test_author 2"],
                                                   published_at="2021-01-01",
                                                   cover_url="https://via.placeholder.com/150"))
        # Execute
        response = app_client.post(f"{TEST_URL}{AppRoutes.Books.POST_GOOGLE_BOOKS_URL}",
                                   json=books_google_books_api_save_in.model_dump())

    # Assert
    # Check response
    assert response.status_code == status.HTTP_200_OK
    encoded_cover_image = encode_image_base64(f"app/static/images/{test_isbn}.jpg")
    assert response.json() == GoogleBooksApiSaveOut(message='book saved successfully',
                                                    title="test_title",
                                                    authors=["test_author 1", "test_author 2"],
                                                    published_at="2021-01-01",
                                                    cover_image_base64=encoded_cover_image).model_dump()

    # Check database
    stmt = select(BookModel).where(BookModel.isbn == test_isbn)
    book_model: BookModel = db_session.execute(stmt).scalars().first()
    stmt = select(AuthorModel).where(AuthorModel.name.in_(["test_author 1", "test_author 2"]))
    author_models: List[AuthorModel] = db_session.execute(stmt).scalars().all()
    stmt = select(BookAuthorModel).where(BookAuthorModel.book_id == book_model.id)
    book_author_models: List[BookAuthorModel] = db_session.execute(stmt).scalars().all()

    assert book_model.title == "test_title"
    assert book_model.isbn == test_isbn
    assert book_model.published_at == datetime.date(2021, 1, 1)
    assert book_model.cover_path == f"app/static/images/{test_isbn}.jpg"
    assert len(author_models) == 2
    for author_model in author_models:
        assert author_model.name in ["test_author 1", "test_author 2"]
    assert len(book_author_models) == 2
    for book_author_model in book_author_models:
        assert book_author_model.book_id == book_model.id
        assert book_author_model.author_id in [author_model.id for author_model in author_models]
    # Check cover image file
    assert os.path.exists(f"app/static/images/{test_isbn}.jpg")

    # Clean up
    os.remove(f"app/static/images/{test_isbn}.jpg")
