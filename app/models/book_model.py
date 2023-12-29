from sqlalchemy import Column, Date, Integer, String

from app.models.setting import BaseModel, Engine


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

    def __init__(self, title, isbn, cover_path, published_at, created_at=None, updated_at=None):
        self.title = title
        self.isbn = isbn
        self.cover_path = cover_path
        self.published_at = published_at
        self.created_at = created_at
        self.updated_at = updated_at


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=Engine)
