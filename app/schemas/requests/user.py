import datetime
from typing import List

from pydantic import BaseModel, Field


class UserSaveIn(BaseModel):
    """
    UserSaveIn is a class that defines the schema for user registration

    Attributes
    ----------
    name : str
        user name
    email : str
        user email
    password : str
        user password
    """
    name: str = Field(title='user name', min_length=1, max_length=255)
    email: str = Field(title='user email', min_length=1, max_length=255)
    password: str = Field(title='user password', min_length=8, max_length=255)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "sample user",
                "email": "sample@sample.com",
                "password": "password"
            }
        }
