import pytest
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import AppRoles
from app.exceptions.exceptions import InvalidCredentialsException
from app.services.login_service import LoginService, TokenData


class TestLoginService():

    def test_create_access_token(self):
        """
        Test create access token
        """
        # Prepare
        test_user_name = "test_user_name"
        test_role = AppRoles.USER
        test_data = {"sub": test_user_name, "role": test_role}

        # Execute
        response = LoginService.create_access_token(test_data)

        # Assert
        assert isinstance(response, str)

    def test_verify_token(self):
        """
        Test verify token
        """
        # Prepare
        test_user_name = "test_user_name"
        test_role = AppRoles.USER
        test_data = {"sub": test_user_name, "role": test_role}
        test_access_token = LoginService.create_access_token(test_data)
        test_token = HTTPAuthorizationCredentials(scheme="Bearer", credentials=test_access_token)

        # Execute
        response = LoginService.verify_token(test_token)

        # Assert
        assert isinstance(response, TokenData)
        assert response.user_name == test_user_name
        assert response.role == test_role

    def test_verify_token_invalid_token(self):
        """
        Test verify token with invalid token
        """
        # Prepare
        test_access_token = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")

        # Execute
        with pytest.raises(InvalidCredentialsException):
            LoginService.verify_token(test_access_token)
