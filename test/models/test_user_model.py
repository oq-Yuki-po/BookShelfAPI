import pytest
from fastapi import status
from sqlalchemy import select

from app.exceptions.exceptions import DuplicateUserException, InvalidUserEmailFormatException, UserNotFoundException
from app.exceptions.message import ExceptionMessage
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
        assert user_model.name == test_user_name
        assert user_model.email == test_user_email
        assert len(user_model.password) == 60
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
        with pytest.raises(InvalidUserEmailFormatException) as exc_info:
            UserModel(name=test_user_name,
                      email=test_user_email,
                      password='test_password')

        # Assert
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.message == ExceptionMessage.INVALID_USER_EMAIL_FORMAT

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
        is_duplicate = user_model._is_duplicate(test_user_email)

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
        is_duplicate = user_model._is_duplicate(test_user_email)

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
        with pytest.raises(DuplicateUserException) as exc_info:
            user_model.save()

        # Assert
        assert exc_info.value.status_code == status.HTTP_409_CONFLICT
        assert exc_info.value.message == ExceptionMessage.DUPLICATE_USER

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

    def test_authenticate_is_valid(self, db_session):
        """Test authenticate method of UserModel
        check if user is valid
        """
        # Prepare
        test_user_name = 'test_user_name'
        test_user_email = 'sample@sample.com'
        test_password = 'test_password'
        UserModelFactory(name=test_user_name,
                         email=test_user_email,
                         password=test_password)
        db_session.commit()

        # Execute
        is_valid = UserModel.authenticate(test_password, test_user_email)

        # Assert
        assert is_valid is True

    def test_authenticate_is_invalid(self, db_session):
        """Test authenticate method of UserModel
        check if user is invalid
        """
        # Prepare
        test_user_name = 'test_user_name'
        test_user_email = 'sample@sample.com'
        test_password = 'test_password'
        invalid_password = 'invalid_password'
        UserModelFactory(name=test_user_name,
                         email=test_user_email,
                         password=test_password)
        db_session.commit()

        # Execute
        is_valid = UserModel.authenticate(invalid_password, test_user_email)

        # Assert
        assert is_valid is False

    def test_authenticate_user_not_found(self):
        """Test authenticate method of UserModel
        check if user is not found
        """
        # Prepare
        test_user_email = 'test_user_email'
        test_password = 'test_password'

        # Execute
        with pytest.raises(UserNotFoundException) as exc_info:
            UserModel.authenticate(test_password, test_user_email)

        # Assert
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.message == ExceptionMessage.USER_NOT_FOUND

    def test_fetch_user(self, db_session):
        """Test fetch_user method of UserModel
        check if user is found
        """
        # Prepare
        test_user_model = UserModelFactory()
        db_session.commit()

        # Execute
        user = UserModel.fetch_user_by_email(test_user_model.email)

        # Assert
        assert user is not None
        assert user.id == test_user_model.id
        assert user.name == test_user_model.name
        assert user.email == test_user_model.email
        assert user.role == test_user_model.role

    def test_fetch_user_user_not_found(self):
        """Test fetch_user method of UserModel
        check if user is not found
        """
        # Prepare
        test_user_email = 'test_user_email'

        # Execute
        with pytest.raises(UserNotFoundException) as exc_info:
            UserModel.fetch_user_by_email(test_user_email)

        # Assert
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.message == ExceptionMessage.USER_NOT_FOUND
