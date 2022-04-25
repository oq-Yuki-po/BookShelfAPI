from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.author_model import AuthorModel
from app.models.setting import BaseModel, Engine


class BookModel(BaseModel):
    """
    BookModel
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    author_id = Column(Integer, ForeignKey('authors.id'))
    isbn = Column(String(13))
    cover_path = Column(String(256))

    authors = relationship(AuthorModel, backref="books")

    def __init__(self, title, isbn, cover_path, author_id):
        self.title = title
        self.isbn = isbn
        self.cover_path = cover_path
        self.author_id = author_id


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=Engine)
