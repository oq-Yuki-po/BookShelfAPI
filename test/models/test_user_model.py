import pytest
from sqlalchemy import select

from app.exceptions.exceptions import DuplicateUserException, InvalidUserEmailFormatException
from app.models import UserModel
from app.models.factories import UserModelFactory


class TestUserModel():

    def test__init_password(self):
        """Test __init__ method of UserModel
        check if password is hashed and salt is generated
        """
        # Prepare
        test_password = 'test_password'
        test_user_name = 'test_user_name'
        test_user_email = 'user_email_1@sample.com'

        # Execute
        user_model = UserModel(name=test_user_name,
                               email=test_user_email,
                               password=test_password)

        # Assert
        assert user_model.salt is not None
        assert user_model.name == test_user_name
        assert user_model.email == test_user_email
        assert len(user_model.password) == 60
        assert len(user_model.salt) == 29
        assert user_model.role == 'user'
        assert user_model.created_at is None
        assert user_model.updated_at is None

    def test__validate_email_is_valid(self):
        """Test _validate_email method of UserModel
        check if email is valid
        """
        # Prepare
        test_user_name = 'test_user_name'
        test_user_email = 'sample@sample.com'

        # Execute
        user_model = UserModel(name=test_user_name,
                               email=test_user_email,
                               password='test_password')

        # Assert
        assert user_model.email == test_user_email

    def test__validate_email_is_invalid(self):
        """Test _validate_email method of UserModel
        check if email is invalid
        """
        # Prepare
        test_user_name = 'test_user_name'
        test_user_email = 'sample@sample'

        # Execute
        with pytest.raises(InvalidUserEmailFormatException):
            UserModel(name=test_user_name,
                      email=test_user_email,
                      password='test_password')

    def test__hash_password(self):
        """Test _hash_password method of UserModel
        check if password is hashed
        """
        # Prepare
        test_password = 'test_password'
        test_user_name = 'test_user_name'
        test_user_email = 'sample@sample.com'

        # Execute
        user_model = UserModel(name=test_user_name,
                               email=test_user_email,
                               password=test_password)

        # Assert
        hashed_password = user_model._hash_password(test_password, user_model.salt)
        assert user_model.password == hashed_password

    def test__is_duplicate_is_duplicate(self, db_session):
        """Test _is_duplicate method of UserModel
        check if user is duplicate
        """
        # Prepare
        test_user_name = 'test_user_name'
        test_user_email = 'sample@sample.com'
        UserModelFactory(name=test_user_name,
                         email=test_user_email,
                         password='test_password')
        db_session.commit()

        user_model = UserModel(name=test_user_name,
                               email=test_user_email,
                               password='test_password')

        # Execute
        is_duplicate = user_model._is_duplicate(test_user_name, test_user_email)

        # Assert
        assert is_duplicate is True

    def test__is_duplicate_is_not_duplicate(self):
        """Test _is_duplicate method of UserModel
        check if user is not duplicate
        """
        # Prepare
        test_user_name = 'test_user_name'
        test_user_email = 'sample@sample.com'

        user_model = UserModel(name=test_user_name,
                               email=test_user_email,
                               password='test_password')

        # Execute
        is_duplicate = user_model._is_duplicate(test_user_name, test_user_email)

        # Assert
        assert is_duplicate is False

    def test_save_is_duplicate(self, db_session):
        """Test save method of UserModel
        check if user is duplicate
        """
        # Prepare
        test_user_name = 'test_user_name'
        test_user_email = 'sample@sample.com'
        test_password = 'test_password'
        UserModelFactory(name=test_user_name,
                         email=test_user_email,
                         password=test_password)
        db_session.commit()

        user_model = UserModel(name=test_user_name,
                               email=test_user_email,
                               password=test_password)

        # Execute
        with pytest.raises(DuplicateUserException):
            user_model.save()

    def test_save_is_not_duplicate(self, db_session):
        """Test save method of UserModel
        check if user is not duplicate
        """
        # Prepare
        test_user_name = 'test_user_name'
        test_user_email = 'sample@sample.com'
        test_password = 'test_password'
        user_model = UserModel(name=test_user_name,
                               email=test_user_email,
                               password=test_password)

        # Execute
        user_model.save()
        db_session.commit()

        # Assert
        stmt = select(UserModel).where(UserModel.name == test_user_name, UserModel.email == test_user_email)
        result = db_session.execute(stmt).scalars().one_or_none()
        assert result is not None
        assert user_model.id is not None
        assert user_model.name == test_user_name
        assert user_model.email == test_user_email
        assert user_model.password is not None
        assert user_model.salt is not None
        assert user_model.role == 'user'
        assert user_model.created_at is not None
        assert user_model.updated_at is not None
