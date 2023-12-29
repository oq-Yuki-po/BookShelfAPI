import requests

from app.exceptions.exceptions import GoogleBooksApiException
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
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise GoogleBooksApiException(message="HTTP error occurred")
        except Exception as err:
            print(f'Unexpected error occurred: {err}')
            raise GoogleBooksApiException(message="Unexpected error occurred")
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
        except (KeyError, TypeError, IndexError):
            print("Invalid response received from the API")
            print("Response:", response.json())
            raise GoogleBooksApiException(message="Invalid response received from the API")
