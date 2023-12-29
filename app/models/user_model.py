from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, UniqueConstraint

from app.models.setting import BaseModel, Engine


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
    salt : str
        user salt
    role : str
        user role
    """

    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint('name', 'email', name='uq_users_name_email'), {})
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    email = Column(String(256))
    password = Column(String(256), nullable=False)
    salt = Column(String(256), nullable=False)
    role = Column(String(256), nullable=False)

    def __init__(self,
                 name: str,
                 email: str,
                 password: str,
                 salt: str,
                 role: str,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:

        self.name = name
        self.email = email
        self.password = password
        self.salt = salt
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=Engine)
