from dataclasses import dataclass
from datetime import datetime, timedelta

from fastapi import Depends
from jose import JWTError, jwt

from app.exceptions.exceptions import InvalidCredentialsException
from app.routers.setting import oauth2_scheme

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"


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
    def create_access_token(cls, data: dict, expires_delta: timedelta = None) -> str:
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
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_token(cls, token: str = Depends(oauth2_scheme)) -> TokenData:
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
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_name: str = payload.get("sub")
            if user_name is None:
                raise InvalidCredentialsException()
            return TokenData(user_name=user_name, role=payload.get("role"))
        except JWTError as e:
            raise InvalidCredentialsException() from e
