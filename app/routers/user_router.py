from fastapi import APIRouter, Depends, status

from app import handle_errors
from app.exceptions.exceptions import NotEnoughPermissionsException, VerificationTokenNotFoundException
from app.models import UserModel, session
from app.routers.setting import AppRoutePermissions, AppRoutes
from app.schemas.exceptions import (
    DuplicateUserExceptionOut,
    InvalidUserEmailFormatExceptionOut,
    NotEnoughPermissionsExceptionOut,
    VerificationTokenNotFoundExceptionOut,
)
from app.schemas.requests import UserSaveIn
from app.schemas.responses import UserGetMeOut, UserSaveOut, UserVerifyOut
from app.services.login_service import LoginService
from app.services.mail_service import MailService

router = APIRouter(
    prefix=AppRoutes.Users.PREFIX,
    tags=[AppRoutes.Users.TAG]
)
USER_ROUTER = AppRoutes.Users
USER_ROUTER_PERMISSIONS = AppRoutePermissions.Users


@router.post(USER_ROUTER.POST_URL,
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

    verification_token = user_model.verification_token

    # send email
    mail_service = MailService()

    # send email to user
    mail_service.send_email(receiver_email=user_model.email,
                            subject="Welcome to Book Shelf App",
                            body=f"Hi {user_model.name},\n\n"
                                 f"Welcome to Book Shelf App.\n\n"
                                 f"Please click the link below to verify your account.\n\n"
                                 f"http://localhost:8000/users/token/{verification_token}"
                            )

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


@router.get(USER_ROUTER.GET_TOKEN_URL,
            response_model=UserVerifyOut,
            responses={
                404: {"model": VerificationTokenNotFoundExceptionOut,
                      "description": "Verification Token Not Found"}
            },
            status_code=status.HTTP_200_OK)
@handle_errors
async def verify_user(token: str):
    """
    Verify user

    ```
    Parameters
    ----------
    token: str
        verification token

    Returns
    -------
    UserVerifyOut
        UserVerifyOut schema

    Raises
    ------
    VerificationTokenNotFoundException
        if verification token not found
    ```
    """
    if UserModel.exist_verification_token(token):

        # update user
        UserModel.verify_user(token)

        session.commit()

        return UserVerifyOut()

    raise VerificationTokenNotFoundException()
