import pytest

from app.exceptions.exceptions import BookIsbnInvalidFormatException
from app.exceptions.message import ExceptionMessage
from app.schemas.requests import BooksGoogleBooksApiSaveIn
from app.schemas.requests.books import isbn10_to_isbn13


def test_isbn10_to_isbn13():
    # Prepare
    isbn10 = "8533302250"
    isbn13 = "9788533302259"

    # Execute
    result = isbn10_to_isbn13(isbn10=isbn10)

    # Assert
    assert result == isbn13


def test_isbn_format_validation():
    # Prepare
    isbn = "978-85-333-0225-0"

    # Execute
    result = BooksGoogleBooksApiSaveIn(isbn=isbn)

    # Assert
    assert result.isbn == isbn.replace('-', '')


def test_isbn_format_validation_with_10_digits():
    # Prepare
    isbn = "85-333-0225-0"
    isbn_13 = "9788533302259"

    # Execute
    result = BooksGoogleBooksApiSaveIn(isbn=isbn)

    # Assert
    assert result.isbn == isbn_13


def test_isbn_format_validation_with_invalid_isbn():
    # Prepare
    isbn = "978-85-333-0225s"

    # Execute
    with pytest.raises(BookIsbnInvalidFormatException) as exc_info:
        BooksGoogleBooksApiSaveIn(isbn=isbn)

    # Assert
    assert exc_info.value.message == ExceptionMessage.BOOK_ISBN_FORMAT


def test_isbn_format_validation_with_invalid_isbn_length():
    # Prepare
    isbn = "978-85-333-0225"

    # Execute
    with pytest.raises(BookIsbnInvalidFormatException) as exc_info:
        BooksGoogleBooksApiSaveIn(isbn=isbn)

    # Assert
    assert exc_info.value.message == ExceptionMessage.BOOK_ISBN_DIGITS
