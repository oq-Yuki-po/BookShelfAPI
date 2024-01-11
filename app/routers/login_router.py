from fastapi import APIRouter, status

from app import handle_errors
from app.exceptions.exceptions import InvalidUserPasswordException
from app.models import UserModel
from app.routers.setting import AppRoutes
from app.schemas.exceptions import InvalidUserPasswordExceptionOut, UserNotFoundExceptionOut
from app.schemas.requests import UserLoginIn
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
    access_token = LoginService.create_access_token(data={"sub": user.name, "role": user.role})
    return UserLoginOut(access_token=access_token, type="bearer", role=user.role)
