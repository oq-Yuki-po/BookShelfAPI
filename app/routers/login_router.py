from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import handle_errors
from app.exceptions.exceptions import InvalidUserPasswordException
from app.models import UserModel
from app.routers.setting import AppRoutes
from app.schemas.exceptions import InvalidUserPasswordExceptionOut, UserNotFoundExceptionOut
from app.schemas.responses import UserLoginOut
from app.services.login_service import LoginService

router = APIRouter(
    prefix=AppRoutes.Login.PREFIX,
    tags=[AppRoutes.Login.TAG]
)


@router.post(AppRoutes.Login.POST_TOKEN_URL,
             response_model=UserLoginOut,
             responses={
                 404: {"model": UserNotFoundExceptionOut,
                       "description": "User Not Found"},
                 400: {"model": InvalidUserPasswordExceptionOut,
                       "description": "Invalid Password"}
             },
             status_code=status.HTTP_200_OK)
@handle_errors
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> UserLoginOut:
    """
    Login user

    ```
    Parameters
    ----------
    user_login_in: UserLoginIn
        UserLoginIn schema

    Returns
    -------
    UserLoginOut
        UserLoginOut schema

    Raises
    ------
    UserNotFoundException
        if user is not found
    InvalidUserPasswordException
        if user password is invalid
    ```
    """
    # user authentication
    is_valid = UserModel.authenticate(password=form_data.password,
                                      email=form_data.username)
    if not is_valid:
        raise InvalidUserPasswordException()

    # fetch user
    user = UserModel.fetch_user_by_email(form_data.username)

    # generate token
    access_token_expires = timedelta(minutes=30)
    access_token = LoginService.create_access_token(data={"sub": user.name, "role": user.role},
                                                    expires_delta=access_token_expires)
    return UserLoginOut(access_token=access_token, type="bearer", role=user.role)
