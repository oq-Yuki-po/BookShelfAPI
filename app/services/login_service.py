from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"


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
