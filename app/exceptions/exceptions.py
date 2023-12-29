from fastapi import HTTPException, status

from app.exceptions.message import ExceptionMessage


class GoogleBooksApiException(HTTPException):
    """Exception for Google Books API"""

    def __init__(self,
                 status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
                 message: str = "Google Books API Error"):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code=self.status_code, detail=self.message)


class DuplicateUserException(HTTPException):
    """Exception for User Duplicate"""

    def __init__(self,
                 status_code: int = status.HTTP_409_CONFLICT,
                 message: str = ExceptionMessage.DUPLICATE_USER):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code=self.status_code, detail=self.message)


class InvalidUserEmailFormatException(HTTPException):
    """Exception for User Email"""

    def __init__(self,
                 status_code: int = status.HTTP_400_BAD_REQUEST,
                 message: str = ExceptionMessage.INVALID_USER_EMAIL_FORMAT):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code=self.status_code, detail=self.message)


class UserNotFoundException(HTTPException):
    """Exception for User Not Found"""

    def __init__(self,
                 status_code: int = status.HTTP_404_NOT_FOUND,
                 message: str = ExceptionMessage.USER_NOT_FOUND):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code=self.status_code, detail=self.message)
