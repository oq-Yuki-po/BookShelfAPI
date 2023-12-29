from app.services.google_books_api_service import GoogleBooksApiService


class TestGoogleBooksApiService:

    def test_get_book_by_isbn(self):

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
