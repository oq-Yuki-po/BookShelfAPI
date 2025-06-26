from typing import List

from fastapi import Depends

from app.exceptions.exceptions import NotEnoughPermissionsException
from app.services.login_service import LoginService, TokenData


def has_permission(required_roles: List[str]):
    def _has_permission(current_user: TokenData = Depends(LoginService.verify_token)) -> TokenData:
        if current_user.role not in required_roles:
            raise NotEnoughPermissionsException()
        return current_user
    return _has_permission
