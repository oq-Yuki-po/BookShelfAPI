import re
import secrets
from datetime import datetime
from typing import Optional

import bcrypt
from sqlalchemy import Boolean, Column, Integer, String, select

from app.exceptions.exceptions import DuplicateUserException, InvalidUserEmailFormatException, UserNotFoundException
from app.models.setting import BaseModel, Engine, session


class UserModel(BaseModel):
    """
    UserModel

    Attributes
    ----------
    id : int
        user id
    name : str
        user name
    email : str
        user email
    password : str
        user password
    role : str
        user role
        role is one of "user", "admin"
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    role = Column(String(256), nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_token = Column(String(256), nullable=True)

    def __init__(self,
                 name: str,
                 email: str,
                 password: str,
                 role: str = "user",
                 is_verified: bool = False,
                 verification_token: str = secrets.token_urlsafe(16),
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:

        self.salt = bcrypt.gensalt().decode()
        self.password = self._hash_password(password, self.salt)
        self.name = name
        self.email = self._validate_email(email)
        self.role = role
        self.is_verified = is_verified
        self.verification_token = verification_token
        self.created_at = created_at
        self.updated_at = updated_at

    def _validate_email(self, email: str) -> str:

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if re.match(pattern, email):
            return email
        else:
            raise InvalidUserEmailFormatException()

    def _hash_password(self, password: str, salt: str) -> str:
        """Hash password

        Parameters
        ----------
        password : str
            password
        salt : str
            salt

        Returns
        -------
        str
            hashed password
        """
        return bcrypt.hashpw(password.encode(), salt.encode()).decode()

    def _is_duplicate(self, email: str) -> bool:
        """Check if user is duplicate

        Parameters
        ----------
        email : str
            user email

        Returns
        -------
        bool
            True if user is duplicate
        """
        stmt = select(UserModel).where(UserModel.email == email)
        result = session.execute(stmt).one_or_none()
        if result is None:
            return False
        return True

    def save(self) -> None:
        """Save user model

        Parameters
        ----------
        name : str
            user name
        email : str
            user email
        password : str
            user password
        role : str (optional) (default="user")
            user role

        Raises
        ------
        DuplicateUserException
            if user name and email is duplicate
        """
        if self._is_duplicate(self.email):
            raise DuplicateUserException()
        session.add(self)
        session.flush()

    @classmethod
    def authenticate(cls, password: str, email: str) -> bool:
        """Authenticate user

        Parameters
        ----------
        name : str
            user name
        password : str
            user password
        email : str
            user email

        Returns
        -------
        bool
            True if authentication is successful, False otherwise
        """
        stmt = select(UserModel).where(UserModel.email == email)
        user = session.execute(stmt).scalars().one_or_none()
        if user is None:
            raise UserNotFoundException()
        hashed_password = user.password
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            return True
        return False

    @classmethod
    def fetch_user_by_email(cls, email: str) -> tuple:
        """Fetch user by email

        Parameters
        ----------
        name : str
            user name
        email : str
            user email

        Returns
        -------
        tuple
            user tuple
            (id, name, email, role)
        """
        stmt = select(UserModel.id,
                      UserModel.name,
                      UserModel.email,
                      UserModel.role,
                      UserModel.is_verified,
                      ).where(UserModel.email == email)
        user = session.execute(stmt).one_or_none()
        if user is None:
            raise UserNotFoundException()
        return user

    @classmethod
    def exist_verification_token(cls, token) -> bool:
        stmt = select(UserModel).where(UserModel.verification_token == token)
        user = session.execute(stmt).scalars().one_or_none()
        if user is None:
            return False
        return True

    @classmethod
    def verify_user(cls, token) -> None:
        stmt = select(UserModel).where(UserModel.verification_token == token)
        user = session.execute(stmt).scalars().one_or_none()
        if user is None:
            raise UserNotFoundException()
        user.is_verified = True
        user.verification_token = None


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=Engine)
