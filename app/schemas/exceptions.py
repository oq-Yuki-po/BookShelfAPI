from pydantic import BaseModel, ConfigDict, Field

from app.exceptions.message import ExceptionMessage


class DuplicateUserExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.DUPLICATE_USER
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.DUPLICATE_USER
            }
        }
    )


class InvalidUserEmailFormatExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.INVALID_USER_EMAIL_FORMAT
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.INVALID_USER_EMAIL_FORMAT
            }
        }
    )


class UserNotFoundExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.USER_NOT_FOUND
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.USER_NOT_FOUND
            }
        }
    )


class InvalidUserPasswordExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.INVALID_USER_PASSWORD
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.INVALID_USER_PASSWORD
            }
        }
    )


class InvalidCredentialsExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.INVALID_CREDENTIALS
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.INVALID_CREDENTIALS
            }
        }
    )


class NotEnoughPermissionsExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.NOT_ENOUGH_PERMISSIONS
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.NOT_ENOUGH_PERMISSIONS
            }
        }
    )