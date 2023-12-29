from datetime import timedelta

from fastapi import APIRouter, status

from app import handle_errors
from app.exceptions.exceptions import InvalidUserPasswordException
from app.models import UserModel, session
from app.routers.setting import AppRoutes
from app.schemas.requests import UserLoginIn, UserSaveIn
from app.schemas.responses import UserLoginOut, UserSaveOut
from app.services.login_service import LoginService

router = APIRouter(
    prefix=AppRoutes.Users.PREFIX,
    tags=[AppRoutes.Users.TAG]
)


@router.post(AppRoutes.Users.POST_URL,
             response_model=UserSaveOut,
             status_code=status.HTTP_201_CREATED)
@handle_errors
async def save_new_user(user_save_in: UserSaveIn) -> UserSaveOut:
    """
    Save new user to database

    ```
    Parameters
    ----------
    user_save_in: UserSaveIn
        UserSaveIn schema

    Returns
    -------
    UserSaveOut
        UserSaveOut schema

    Raises
    ------
    DuplicateUserException
        if user name and email is duplicate
    InvalidUserEmailFormatException
        if user email is invalid
    ```
    """
    user_model = UserModel(name=user_save_in.name,
                           password=user_save_in.password,
                           email=user_save_in.email)
    user_model.save()
    session.commit()

    return UserSaveOut()


@router.post(AppRoutes.Users.POST_TOKEN_URL,
             response_model=UserLoginOut,
             status_code=status.HTTP_200_OK)
@handle_errors
async def login(user_login_in: UserLoginIn) -> UserLoginOut:
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
    is_valid = UserModel.authenticate(password=user_login_in.password,
                                      email=user_login_in.email)
    if not is_valid:
        raise InvalidUserPasswordException()

    # fetch user
    user = UserModel.fetch_user_by_email(user_login_in.email)

    # generate token
    access_token_expires = timedelta(minutes=30)
    access_token = LoginService.create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )

    return UserLoginOut(access_token=access_token, token_type="bearer", role=user.role)
