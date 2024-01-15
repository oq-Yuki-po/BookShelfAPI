from datetime import datetime

from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from app.models import UserModel, session


class UserModelFactory(SQLAlchemyModelFactory):
    class Meta:

        model = UserModel
        sqlalchemy_session = session

    name = Sequence(lambda n: f'user_name_{n}')
    email = Sequence(lambda n: f'user_email_{n}@sample.com')
    password = Sequence(lambda n: f'user_password_{n}')
    role = "user"
    is_verified = True
    verification_token = Sequence(lambda n: f'user_verification_token_{n}')
    created_at = datetime.now()
    updated_at = datetime.now()
