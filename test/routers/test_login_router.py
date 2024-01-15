from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.factories import UserModelFactory
from app.routers.setting import AppRoutes
from app.schemas.exceptions import (
    InvalidUserPasswordExceptionOut,
    UserIsNotVerifiedExceptionOut,
    UserNotFoundExceptionOut,
)
from app.schemas.requests import UserLoginIn
from app.schemas.responses import UserLoginOut

TEST_URL = f"{AppRoutes.Login.PREFIX}"


def test_login_success(app_client: TestClient, db_session: Session):
    """
    Test login
    """
    # Prepare
    test_user_password = "password"
    # create user with verified
    test_user_model = UserModelFactory(password=test_user_password,
                                       is_verified=True)
    db_session.commit()
    user_login_in = UserLoginIn(email=test_user_model.email, password=test_user_password)

    # Execute
    response = app_client.post(f"{TEST_URL}{AppRoutes.Login.POST_TOKEN_URL}",
                               json=user_login_in.model_dump())

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == UserLoginOut(access_token=response.json()["access_token"],
                                           type=response.json()["type"],
                                           user=test_user_model.role).model_dump()


def test_login_user_not_verified(app_client: TestClient, db_session: Session):
    """
    Test login with user not verified
    """
    # Prepare
    test_user_password = "password"
    # create user with not verified
    test_user_model = UserModelFactory(password=test_user_password,
                                       is_verified=False)
    db_session.commit()
    user_login_in = UserLoginIn(email=test_user_model.email, password=test_user_password)

    # Execute
    response = app_client.post(f"{TEST_URL}{AppRoutes.Login.POST_TOKEN_URL}",
                               json=user_login_in.model_dump())

    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == UserIsNotVerifiedExceptionOut().model_dump()


def test_login_invalid_password(app_client: TestClient, db_session: Session):
    """
    Test login with invalid password
    """
    # Prepare
    test_user_password = "password"
    test_user_model = UserModelFactory(password=test_user_password)
    db_session.commit()
    user_login_in = UserLoginIn(email=test_user_model.email, password="invalid_password")

    # Execute
    response = app_client.post(f"{TEST_URL}{AppRoutes.Login.POST_TOKEN_URL}",
                               json=user_login_in.model_dump())

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == InvalidUserPasswordExceptionOut().model_dump()


def test_login_user_not_found(app_client: TestClient):
    """
    Test login with user not found
    """
    # Prepare
    user_login_in = UserLoginIn(email="invalid_user", password="password")

    # Execute
    response = app_client.post(f"{TEST_URL}{AppRoutes.Login.POST_TOKEN_URL}",
                               json=user_login_in.model_dump())

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == UserNotFoundExceptionOut().model_dump()
