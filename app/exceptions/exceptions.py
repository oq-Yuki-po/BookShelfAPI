from fastapi import HTTPException, status


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
                 status_code: int = status.HTTP_400_BAD_REQUEST,
                 message: str = "Duplicate User Error"):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code=self.status_code, detail=self.message)


class InvalidUserEmailFormatException(HTTPException):
    """Exception for User Email"""

    def __init__(self,
                 status_code: int = status.HTTP_400_BAD_REQUEST,
                 message: str = "Invalid User Email Format Error"):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code=self.status_code, detail=self.message)
