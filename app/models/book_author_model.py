from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models import AuthorModel, BookModel, session
from app.models.setting import BaseModel, Engine


class BookAuthorModel(BaseModel):
    """
    BookAuthorModel

    This model is for many-to-many relationship between books and authors.

    Attributes
    ----------
    book_id : int
        book id is foreign key from books table
    author_id : int
        author id is foreign key from authors table
    """

    __tablename__ = 'book_authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(BookModel.id))
    author_id = Column(Integer, ForeignKey(AuthorModel.id))

    book = relationship("BookModel", backref="book_authors")
    author = relationship("AuthorModel", backref="book_authors")

    def __init__(self, book_id=None, author_id=None, created_at=None, updated_at=None, book=None, author=None):
        if book is None:
            self.book_id = book_id
        else:
            self.book = book
        if author is None:
            self.author_id = author_id
        else:
            self.author = author
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def save(cls, book_id, author_id):
        """
        Save book author

        Parameters
        ----------
        book_id : int
            book id
        author_id : int
            author id

        Returns
        -------
        bool
            True if saved successfully
        """
        book_author = cls(book_id=book_id, author_id=author_id)
        session.add(book_author)
        session.flush()


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=Engine)
