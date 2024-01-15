from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import UserModel
from app.models.factories import UserModelFactory
from app.routers.setting import AppRoutes
from app.schemas.exceptions import (
    DuplicateUserExceptionOut,
    InvalidUserEmailFormatExceptionOut,
    VerificationTokenNotFoundExceptionOut,
)
from app.schemas.requests import UserSaveIn
from app.schemas.responses import UserSaveOut, UserVerifyOut

TEST_URL = f"{AppRoutes.Users.PREFIX}"


def test_save_new_user_success(app_client: TestClient, db_session: Session):
    """
    Test save new user
    """
    # Prepare
    test_user_name = "test_user"
    test_user_email = "sample@sample.com"
    test_user_password = "password"
    user_save_in = UserSaveIn(name=test_user_name, email=test_user_email, password=test_user_password)

    # Execute
    response = app_client.post(f"{TEST_URL}{AppRoutes.Users.POST_URL}",
                               json=user_save_in.model_dump())

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == UserSaveOut().model_dump()
    # Check database
    stmt = select(UserModel).where(UserModel.name == test_user_name)
    user_model = db_session.execute(stmt).scalars().one_or_none()
    assert user_model.name == test_user_name
    assert user_model.email == test_user_email
    assert user_model.password != test_user_password
    assert user_model.role == "user"
    assert user_model.is_verified is False
    assert user_model.verification_token is not None


def test_save_new_user_duplicate_email(app_client: TestClient, db_session: Session):
    """
    Test save new user with duplicate email
    """
    # Prepare
    duplicate_email = "sample@sample.com"
    UserModelFactory(email=duplicate_email)
    db_session.commit()

    test_user_name = "test_user"
    test_user_email = duplicate_email
    test_user_password = "password"
    user_save_in = UserSaveIn(name=test_user_name, email=test_user_email, password=test_user_password)

    # Execute
    response = app_client.post(f"{TEST_URL}{AppRoutes.Users.POST_URL}",
                               json=user_save_in.model_dump())

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == DuplicateUserExceptionOut().model_dump()


def test_save_new_user_invalid_email(app_client: TestClient):
    """
    Test save new user with invalid email
    """
    # Prepare
    test_user_name = "test_user"
    test_user_email = "sample"
    test_user_password = "password"
    user_save_in = UserSaveIn(name=test_user_name, email=test_user_email, password=test_user_password)

    # Execute
    response = app_client.post(f"{TEST_URL}{AppRoutes.Users.POST_URL}",
                               json=user_save_in.model_dump())

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == InvalidUserEmailFormatExceptionOut().model_dump()


def test_verify_user_success(app_client: TestClient, db_session: Session):
    """
    Test verify user
    """
    # Prepare
    user_model = UserModelFactory(is_verified=False)
    db_session.commit()
    user_id = user_model.id

    # Execute
    response = app_client.get(f"{TEST_URL}/token/{user_model.verification_token}")
    db_session.close()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == UserVerifyOut().model_dump()
    # Check database
    stmt = select(UserModel).where(UserModel.id == user_id)
    user_model = db_session.execute(stmt).scalars().one_or_none()
    assert user_model.is_verified is True
    assert user_model.verification_token is None


def test_verify_user_invalid_token(app_client: TestClient, db_session: Session):
    """
    Test verify user with invalid token
    """
    # Prepare
    user_model = UserModelFactory(is_verified=False)
    db_session.commit()
    user_id = user_model.id

    # Execute
    response = app_client.get(f"{TEST_URL}/token/invalid_token")
    db_session.close()

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == VerificationTokenNotFoundExceptionOut().model_dump()
    # Check database
    stmt = select(UserModel).where(UserModel.id == user_id)
    user_model = db_session.execute(stmt).scalars().one_or_none()
    assert user_model.is_verified is False
    assert user_model.verification_token is not None
