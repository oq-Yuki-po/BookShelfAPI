from fastapi import HTTPException, status


class GoogleBooksApiException(HTTPException):
    """Exception for Google Books API"""

    def __init__(self,
                 status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
                 message: str = "Google Books API Error"):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code=self.status_code, detail=self.message)
