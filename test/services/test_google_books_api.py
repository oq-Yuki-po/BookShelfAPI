import os

import pytest
from fastapi import status
from requests.exceptions import HTTPError, RequestException

from app.exceptions.exceptions import GoogleBooksApiException
from app.exceptions.message import ExceptionMessage
from app.schemas.api import GoogleBookSchema
from app.services.google_books_api_service import GoogleBooksApiService


class TestGoogleBooksApiService:

    def test_get_book_by_isbn(self):
        """Test for fetch_book_data method of GoogleBooksApiService
        """

        # Prepare
        isbn = '9784048930598'

        # Execute
        google_books_api_service = GoogleBooksApiService()
        book = google_books_api_service.fetch_book_data(isbn)

        # Assert
        assert book.title == 'Clean Code'
        assert book.authors == ['ロバート・C. マーチン']
        assert book.published_at == '2017-12-01'
        assert book.cover_url == 'http://books.google.com/books/content?id=bk4atAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'

    def test_get_book_by_isbn_with_invalid_response(self, mocker):
        """Test for fetch_book_data method of GoogleBooksApiService
        with invalid response
        """

        # Prepare
        isbn = '9784048930599'
        mocker.patch('app.services.google_books_api_service.requests.get')
        requests_get_mock = mocker.patch('app.services.google_books_api_service.requests.get')
        requests_get_mock.return_value.json.return_value = {'items': []}

        # Execute
        google_books_api_service = GoogleBooksApiService()
        with pytest.raises(GoogleBooksApiException) as exc_info:
            _ = google_books_api_service.fetch_book_data(isbn)

        # Assert
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc_info.value.message == ExceptionMessage.GOOGLE_BOOKS_API_INVALID_RESPONSE

    def test_get_book_by_isbn_with_http_error(self, mocker):
        """Test for fetch_book_data method of GoogleBooksApiService
        with HTTP error
        """

        # Prepare
        isbn = '9784048930599'
        mocker.patch('app.services.google_books_api_service.requests.get')
        requests_get_mock = mocker.patch('app.services.google_books_api_service.requests.get')
        requests_get_mock.side_effect = HTTPError()

        # Execute
        google_books_api_service = GoogleBooksApiService()
        with pytest.raises(GoogleBooksApiException) as exc_info:
            _ = google_books_api_service.fetch_book_data(isbn)

        # Assert
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc_info.value.message == ExceptionMessage.GOOGLE_BOOKS_API_HTTP_ERROR

    def test_get_book_by_isbn_with_unexpected_error(self, mocker):
        """Test for fetch_book_data method of GoogleBooksApiService
        with unexpected error
        """

        # Prepare
        isbn = '9784048930599'
        mocker.patch('app.services.google_books_api_service.requests.get')
        requests_get_mock = mocker.patch('app.services.google_books_api_service.requests.get')
        requests_get_mock.side_effect = Exception()

        # Execute
        google_books_api_service = GoogleBooksApiService()
        with pytest.raises(GoogleBooksApiException) as exc_info:
            _ = google_books_api_service.fetch_book_data(isbn)

        # Assert
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc_info.value.message == ExceptionMessage.GOOGLE_BOOKS_API_UNEXPECTED_ERROR

    def test_save_cover_image(self):
        """Test for save_cover_image method of GoogleBooksApiService
        """

        # Prepare
        isbn = '9784048930598'
        google_book_schema = GoogleBookSchema(title='Clean Code',
                                              authors=['ロバート・C. マーチン'],
                                              published_at='2017-12-01',
                                              cover_url='http://books.google.com/books/content?id=bk4atAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api')

        # Execute
        google_books_api_service = GoogleBooksApiService()
        cover_image_path = google_books_api_service.save_cover_image(google_book_schema, isbn)

        # Assert
        assert cover_image_path == 'app/static/images/9784048930598.jpg'

        # Clean up
        os.remove(cover_image_path)

    def test_save_cover_image_with_request_exception(self, mocker):
        """Test for save_cover_image method of GoogleBooksApiService
        with request exception
        """

        # Prepare
        isbn = '9784048930598'
        google_book_schema = GoogleBookSchema(title='Clean Code',
                                              authors=['ロバート・C. マーチン'],
                                              published_at='2017-12-01',
                                              cover_url='')
        mocker.patch('app.services.google_books_api_service.requests.get')
        requests_get_mock = mocker.patch('app.services.google_books_api_service.requests.get')
        requests_get_mock.side_effect = RequestException()

        # Execute
        google_books_api_service = GoogleBooksApiService()
        with pytest.raises(GoogleBooksApiException) as exc_info:
            _ = google_books_api_service.save_cover_image(google_book_schema, isbn)

        # Assert
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc_info.value.message == ExceptionMessage.GOOGLE_BOOKS_API_IMAGE_DOWNLOAD_ERROR

    def test_save_cover_image_with_file_not_found(self, mocker):
        """Test for save_cover_image method of GoogleBooksApiService
        with file not found
        """

        # Prepare
        isbn = '9784048930598'
        google_book_schema = GoogleBookSchema(title='Clean Code',
                                              authors=['ロバート・C. マーチン'],
                                              published_at='2017-12-01',
                                              cover_url='')
        mocker.patch('app.services.google_books_api_service.requests.get')
        requests_get_mock = mocker.patch('app.services.google_books_api_service.requests.get')
        requests_get_mock.return_value.content = b'sfas'

        # Execute
        google_books_api_service = GoogleBooksApiService()
        with pytest.raises(GoogleBooksApiException) as exc_info:
            _ = google_books_api_service.save_cover_image(google_book_schema, isbn)

        # Assert
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc_info.value.message == ExceptionMessage.GOOGLE_BOOKS_API_IMAGE_DOWNLOAD_ERROR
