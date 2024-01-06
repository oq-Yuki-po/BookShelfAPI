import datetime

import pytest
from sqlalchemy import select

from app.exceptions.exceptions import DuplicateBookIsbnException
from app.models import BookModel
from app.models.factories import BookModelFactory


class TestBookModel():

    def test__is_duplicated_is_true(self, db_session):
        """Test for _is_duplicated method of BookModel
        with duplicated isbn
        """
        # Prepare
        test_isbn = '9788576082675'
        book_model = BookModelFactory(isbn=test_isbn)
        db_session.commit()

        # Execute
        book = BookModel(title=book_model.title,
                         isbn=book_model.isbn,
                         cover_path=book_model.cover_path,
                         published_at=book_model.published_at)

        # Assert
        assert book._is_duplicated() is True

    def test__is_duplicated_is_false(self):
        """Test for _is_duplicated method of BookModel
        with non-duplicated isbn
        """
        # Prepare

        # Execute
        book = BookModel(title='test_title',
                         isbn='9788576082675',
                         cover_path='test_cover_path',
                         published_at='2020-01-01')

        # Assert
        assert book._is_duplicated() is False

    def test_save_google_books_api_successfully(self, db_session):
        """Test for save_google_books_api method of BookModel
        with successful case
        """
        # Prepare
        test_title = 'test_title'
        test_isbn = '9788576082675'
        test_cover_path = 'test_cover_path'
        test_published_at = '2020-01-01'

        # Execute
        book_model = BookModel(title=test_title,
                               isbn=test_isbn,
                               cover_path=test_cover_path,
                               published_at=test_published_at)
        saved_book_model = book_model.save_google_books_api()
        db_session.commit()

        # Assert
        assert isinstance(saved_book_model, BookModel)
        stmt = select(BookModel).where(BookModel.isbn == test_isbn)
        result = db_session.execute(stmt).scalars().first()
        assert result is not None
        assert result.title == test_title
        assert result.isbn == test_isbn
        assert result.cover_path == test_cover_path
        assert result.published_at == datetime.date.fromisoformat(test_published_at)

    def test_save_google_books_api_with_duplicated_isbn(self, db_session):
        """Test for save_google_books_api method of BookModel
        with duplicated isbn
        """
        # Prepare
        test_title = 'test_title'
        test_isbn = '9788576082675'
        test_cover_path = 'test_cover_path'
        test_published_at = '2020-01-01'
        BookModelFactory(title=test_title,
                         isbn=test_isbn,
                         cover_path=test_cover_path,
                         published_at=test_published_at)
        db_session.commit()

        # Execute
        book_model = BookModel(title=test_title,
                               isbn=test_isbn,
                               cover_path=test_cover_path,
                               published_at=test_published_at)

        # Assert
        with pytest.raises(DuplicateBookIsbnException):
            book_model.save_google_books_api()
