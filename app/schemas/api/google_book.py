import datetime
from typing import List

from pydantic import BaseModel, field_validator


class GoogleBookSchema(BaseModel):
    """Schema for Google Books API

    Attributes
    ----------
    title : str
        Title of book
    authors : list of str
        List of authors of book
    published_at : str
        Date book was published
        if date is unknown, set to 1970-01-01
        if month is unknown, set to 01
        if day is unknown, set to 01
        if invalid date format, set to 1970-01-01
    cover_url : str
        URL of book cover
        if cover_url is empty, replace it with a placeholder image
    """
    title: str
    authors: List[str]
    published_at: str
    cover_url: str

    @field_validator('cover_url')
    def cover_url_is_empty(cls, v):
        """If cover_url is empty, replace it with a placeholder image"""
        if not v:
            return 'app/static/images/no_image.jpg'
        return v

    @field_validator('published_at')
    def check_published_at(cls, v):
        """
        check published_at is valid date format
        if date is unknown, set to 1970-01-01
        if month is unknown, set to 01
        if day is unknown, set to 01
        if invalid date format, set to 1970-01-01
        """

        formats = ['%Y-%m-%d', '%Y-%m', '%Y']
        formatted_v = ""
        for format in formats:
            try:
                formatted_v = datetime.datetime.strptime(v, format)
            except ValueError:
                pass
        if not formatted_v:
            return '1970-01-01'
        return formatted_v.strftime('%Y-%m-%d')
