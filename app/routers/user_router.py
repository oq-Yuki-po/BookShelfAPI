from fastapi import APIRouter, Depends, status

from app import handle_errors
from app.exceptions.exceptions import NotEnoughPermissionsException
from app.models import UserModel, session
from app.routers.setting import AppRoutes
from app.schemas.requests import UserSaveIn
from app.schemas.responses import UserSaveOut
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


@router.get(AppRoutes.Users.GET_ME_URL)
async def get_current_user(current_user: str = Depends(LoginService.verify_token)):
    if "admin" not in current_user.role:
        raise NotEnoughPermissionsException()
    return current_user
