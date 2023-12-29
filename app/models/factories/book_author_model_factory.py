from datetime import datetime

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import BookAuthorModel, session
from app.models.factories import AuthorModelFactory, BookModelFactory


class BookAuthorModelFactory(SQLAlchemyModelFactory):
    class Meta:
        model = BookAuthorModel
        sqlalchemy_session = session

    book = factory.SubFactory(BookModelFactory)
    author = factory.SubFactory(AuthorModelFactory)
    created_at = datetime.now()
    updated_at = datetime.now()
