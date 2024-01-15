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


class DuplicateBookISBNExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.DUPLICATE_BOOK_ISBN
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.DUPLICATE_BOOK_ISBN
            }
        }
    )


class BookIsbnInvalidFormatExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.BOOK_ISBN_FORMAT
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.BOOK_ISBN_FORMAT
            }
        }
    )


class GoogleBooksApiExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.GOOGLE_BOOKS_API_HTTP_ERROR
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.GOOGLE_BOOKS_API_HTTP_ERROR
            }
        }
    )


class UserIsNotVerifiedExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.USER_IS_NOT_VERIFIED
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.USER_IS_NOT_VERIFIED
            }
        }
    )


class VerificationTokenNotFoundExceptionOut(BaseModel):

    detail: str = Field(
        description='The detail of the exception',
        default=ExceptionMessage.VERIFICATION_TOKEN_NOT_FOUND
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'detail': ExceptionMessage.VERIFICATION_TOKEN_NOT_FOUND
            }
        }
    )
