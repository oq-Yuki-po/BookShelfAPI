from io import BytesIO

import requests
from PIL import Image

from app.exceptions.exceptions import GoogleBooksApiException
from app.exceptions.message import ExceptionMessage
from app.schemas.api import GoogleBookSchema


class GoogleBooksApiService:
    """Service for Google Books API"""

    @classmethod
    def fetch_book_data(cls, isbn: str):
        """Fetches book data from Google Books API

        Parameters
        ----------
        isbn : str
            ISBN of book
        Returns
        -------
        title : str
            Title of book
        authors : list of str
            List of authors of book
        published_at : str
            Date book was published
        cover_url : str
            URL of book cover
        """

        url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise GoogleBooksApiException(message=ExceptionMessage.GOOGLE_BOOKS_API_HTTP_ERROR) from http_err
        except Exception as err:
            print(f'Unexpected error occurred: {err}')
            raise GoogleBooksApiException(message=ExceptionMessage.GOOGLE_BOOKS_API_UNEXPECTED_ERROR) from err
        try:
            data = response.json()['items'][0]['volumeInfo']
            title = data['title']
            authors = data['authors']
            published_at = data['publishedDate']
            cover_url = data.get('imageLinks', {}).get('thumbnail', '')

            google_book_schema = GoogleBookSchema(title=title,
                                                  authors=authors,
                                                  published_at=published_at,
                                                  cover_url=cover_url)
            return google_book_schema
        except (KeyError, TypeError, IndexError) as err:
            print("Invalid response received from the API")
            print("Response:", response.json())
            raise GoogleBooksApiException(message=ExceptionMessage.GOOGLE_BOOKS_API_INVALID_RESPONSE) from err

    @classmethod
    def save_cover_image(cls, google_book_schema: GoogleBookSchema, isbn: str):
        """Get cover image of book from Google Books API

        Parameters
        ----------
        google_book_schema : GoogleBookSchema
            Schema of google book data
        isbn : str
            ISBN of book
        Returns
        -------
        cover_image : PIL.Image
            Cover image of book
        """
        try:
            res = requests.get(google_book_schema.cover_url, timeout=10)
            res.raise_for_status()

            # check if image is valid
            img = Image.open(BytesIO(res.content))

            # save image
            img.save(f"app/static/images/{isbn}.jpg")

            return f"app/static/images/{isbn}.jpg"

        except requests.exceptions.RequestException as e:
            raise GoogleBooksApiException(message=ExceptionMessage.GOOGLE_BOOKS_API_IMAGE_DOWNLOAD_ERROR) from e
        except IOError as e:
            raise GoogleBooksApiException(message=ExceptionMessage.GOOGLE_BOOKS_API_IMAGE_DOWNLOAD_ERROR) from e
        except Exception as e:
            raise GoogleBooksApiException(message=ExceptionMessage.GOOGLE_BOOKS_API_IMAGE_DOWNLOAD_ERROR) from e
