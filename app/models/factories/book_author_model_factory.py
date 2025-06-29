from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory
from factory.declarations import SubFactory

from app.models import BookAuthorModel, session
from app.models.factories import AuthorModelFactory, BookModelFactory


class BookAuthorModelFactory(SQLAlchemyModelFactory):
    class Meta:
        model = BookAuthorModel
        sqlalchemy_session = session

    book = SubFactory(BookModelFactory)
    author = SubFactory(AuthorModelFactory)
    created_at = datetime.now()
    updated_at = datetime.now()
