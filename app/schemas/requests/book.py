from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.exceptions.exceptions import BookIsbnInvalidFormatException
from app.exceptions.message import ExceptionMessage


def isbn10_to_isbn13(isbn10: str) -> str:
    """isbn10_to_isbn13 is a function that converts ISBN-10 to ISBN-13

    Parameters
    ----------
    isbn10 : str
        ISBN-10

    Returns
    -------
    str
        ISBN-13
    """

    # add prefix
    isbn13 = "978" + isbn10[:-1]

    # calculate checksum
    checksum = 0
    for i, digit in enumerate(isbn13):
        if i % 2 == 0:
            checksum += int(digit)
        else:
            checksum += 3 * int(digit)

    # add checksum
    isbn13 += str((10 - (checksum % 10)) % 10)

    return isbn13


class BooksGoogleBooksApiSaveIn(BaseModel):
    """
    BooksGoogleBooksApiSaveIn is a class that defines the schema for book registration

    Attributes
    ----------
    isbn : str
        isbn number of book which is 10 or 13 digits
    """

    isbn: str = Field(title='isbn', min_length=1, max_length=20)

    @field_validator('isbn')
    def isbn_validator(cls, v):
        v = v.replace('-', '')
        if not v.isdigit():
            raise BookIsbnInvalidFormatException(message=ExceptionMessage.BOOK_ISBN_FORMAT)
        if len(v) not in [10, 13]:
            raise BookIsbnInvalidFormatException(message=ExceptionMessage.BOOK_ISBN_DIGITS)
        if len(v) == 10:
            v = isbn10_to_isbn13(v)
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "isbn": "9788576082675"
            }
        }
    )
