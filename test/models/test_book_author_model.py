from sqlalchemy import select

from app.models import BookAuthorModel
from app.models.factories import AuthorModelFactory, BookAuthorModelFactory, BookModelFactory


class TestBookAuthorModel:

    def test_save(self, db_session):
        """Test for save method of BookAuthorModel
        """
        # Prepare
        book_model = BookModelFactory()
        author_model = AuthorModelFactory()
        db_session.commit()

        # Execute
        BookAuthorModel.save(book_id=book_model.id, author_id=author_model.id)
        db_session.commit()

        # Assert
        stmt = select(BookAuthorModel).where(BookAuthorModel.book_id == book_model.id)
        result = db_session.execute(stmt).scalars().first()
        assert result is not None
        assert result.book_id == book_model.id
