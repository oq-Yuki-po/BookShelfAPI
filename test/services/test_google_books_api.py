import pytest
from fastapi import status
from requests.exceptions import HTTPError

from app.exceptions.exceptions import GoogleBooksApiException
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
        assert exc_info.value.message == 'Invalid response received from the API'

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
        assert exc_info.value.message == 'HTTP error occurred'

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
        assert exc_info.value.message == 'Unexpected error occurred'
