import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.exceptions.exceptions import InvalidCredentialsException, NotEnoughPermissionsException

SECRET_KEY = os.environ.get("TOKEN_SECRET")
ALGORITHM = os.environ.get("TOKEN_ALGORITHM")

http_bearer = HTTPBearer()


@dataclass
class TokenData:
    """Token data

    Attributes
    ----------
    user_name : str
        user name
    role : str
        user role
        admin or user
    """
    user_name: str = None
    role: str = None


class LoginService:

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        """Create access token

        Parameters
        ----------
        data : dict
            data to encode
        expires_delta : timedelta
            expiration time

        Returns
        -------
        str
            access token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=int(os.environ.get("TOKEN_EXPIRE_MINUTES")))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_token(cls,
                     token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> TokenData:
        """Verify token

        Parameters
        ----------
        token : str
            access token

        Returns
        -------
        TokenData
            token data

        Raises
        ------
        InvalidCredentialsException
            if token is invalid
        """
        try:
            payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            user_name: str = payload.get("sub")
            if user_name is None:
                raise InvalidCredentialsException()
            return TokenData(user_name=user_name, role=payload.get("role"))
        except JWTError as e:
            raise InvalidCredentialsException() from e
