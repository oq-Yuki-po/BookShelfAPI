from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Date, Integer, String, select

from app.exceptions.exceptions import DuplicateBookIsbnException
from app.models.setting import BaseModel, Engine, session


class BookModel(BaseModel):
    """
    BookModel

    Attributes
    ----------
    id : int
        book id
    title : str
        book title
    isbn : str
        book isbn
    cover_path : str
        book cover path
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    isbn = Column(String(13))
    published_at = Column(Date, nullable=False)
    cover_path = Column(String(256))

    def __init__(self,
                 title,
                 isbn,
                 cover_path,
                 published_at,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        self.title = title
        self.isbn = isbn
        self.cover_path = cover_path
        self.published_at = published_at
        self.created_at = created_at
        self.updated_at = updated_at

    def _is_duplicated(self) -> bool:
        """
        Check if book's isbn is duplicated

        Returns
        -------
        bool
            True if book's isbn is duplicated
        """
        stmt = select(BookModel).where(BookModel.isbn == self.isbn)
        result = session.execute(stmt).scalars().one_or_none()
        if result is None:
            return False
        else:
            return True

    def save_google_books_api(self) -> BookModel:
        """Save book from Google Books API

        Returns
        -------
        BookModel
            BookModel object

        Raises
        ------
        DuplicateBookIsbnException
            If book's isbn is duplicated
        """
        if self._is_duplicated():
            raise DuplicateBookIsbnException()
        else:
            session.add(self)
            session.flush()
            return self


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=Engine)
