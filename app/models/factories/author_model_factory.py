from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory
from factory.declarations import Sequence

from app.models import AuthorModel, session


class AuthorModelFactory(SQLAlchemyModelFactory):
    class Meta:

        model = AuthorModel
        sqlalchemy_session = session

    name = Sequence(lambda n: f'author_name_{n}')
    created_at = datetime.now()
    updated_at = datetime.now()
