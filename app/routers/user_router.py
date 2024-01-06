from fastapi import APIRouter, Depends, status

from app import handle_errors
from app.exceptions.exceptions import NotEnoughPermissionsException
from app.models import UserModel, session
from app.routers.setting import AppRoutePermissions, AppRoutes
from app.schemas.exceptions import (
    DuplicateUserExceptionOut,
    InvalidUserEmailFormatExceptionOut,
    NotEnoughPermissionsExceptionOut,
)
from app.schemas.requests import UserSaveIn
from app.schemas.responses import UserGetMeOut, UserSaveOut
from app.services.login_service import LoginService

router = APIRouter(
    prefix=AppRoutes.Users.PREFIX,
    tags=[AppRoutes.Users.TAG]
)
USER_ROUTER = AppRoutes.Users
USER_ROUTER_PERMISSIONS = AppRoutePermissions.Users


@router.post(USER_ROUTER.POST_TOKEN_URL,
             response_model=UserSaveOut,
             responses={
                 409: {"model": DuplicateUserExceptionOut,
                       "description": "Duplicate User"},
                 400: {"model": InvalidUserEmailFormatExceptionOut,
                       "description": "Invalid Email Format"}
             },
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
        if user email is duplicate
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


@router.get(USER_ROUTER.GET_ME_URL,
            response_model=UserGetMeOut,
            responses={
                404: {"model": NotEnoughPermissionsExceptionOut,
                      "description": "Not Enough Permissions"}
            },
            status_code=status.HTTP_200_OK)
@handle_errors
async def get_current_user(current_user: str = Depends(LoginService.verify_token)) -> UserGetMeOut:
    """
    Get current user

    ```
    Parameters
    ----------
    current_user: str
        current user

    Returns
    -------
    UserGetMeOut
        UserGetMeOut schema

    Raises
    ------
    NotEnoughPermissionsException
        if user role is not admin or user
    ```
    """
    if current_user.role not in USER_ROUTER_PERMISSIONS.GetMe.PERMISSIONS:
        raise NotEnoughPermissionsException()
    return UserGetMeOut(user_name=current_user.user_name, role=current_user.role)
