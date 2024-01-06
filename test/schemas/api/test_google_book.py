from app.schemas.api.google_book import GoogleBookSchema


class TestGoogleBookSchema():

    def test_cover_url_is_empty(self):
        """If cover_url is empty, replace it with a placeholder image
        """
        # Prepare
        google_book_schema = GoogleBookSchema(
            title='sample',
            authors=['sample'],
            published_at='2022',
            cover_url=''
        )

        # Assert
        assert google_book_schema.cover_url == 'app/static/images/no_image.jpg'

    def test_published_at_is_empty(self):
        """If published_at is empty, replace it with 1970-01-01
        """
        # Prepare
        google_book_schema = GoogleBookSchema(
            title='sample',
            authors=['sample'],
            published_at='',
            cover_url='sample'
        )

        # Assert
        assert google_book_schema.published_at == '1970-01-01'

    def test_published_at_is_year(self):
        """If published_at is year, replace it with year-01-01
        """
        # Prepare
        google_book_schema = GoogleBookSchema(
            title='sample',
            authors=['sample'],
            published_at='2020',
            cover_url='sample'
        )

        # Assert
        assert google_book_schema.published_at == '2020-01-01'

    def test_published_at_is_year_month(self):
        """If published_at is year-month, replace it with year-month-01
        """
        # Prepare
        google_book_schema = GoogleBookSchema(
            title='sample',
            authors=['sample'],
            published_at='2020-01',
            cover_url='sample'
        )

        # Assert
        assert google_book_schema.published_at == '2020-01-01'

    def test_published_at_is_year_month_day(self):
        """If published_at is year-month-day, no change
        """
        # Prepare
        google_book_schema = GoogleBookSchema(
            title='sample',
            authors=['sample'],
            published_at='2020-01-01',
            cover_url='sample'
        )

        # Assert
        assert google_book_schema.published_at == '2020-01-01'

    def test_published_at_is_invalid(self):
        """If published_at is invalid, replace it with 1970-01-01
        """
        # Prepare
        google_book_schema = GoogleBookSchema(
            title='sample',
            authors=['sample'],
            published_at='sample',
            cover_url='sample'
        )

        # Assert
        assert google_book_schema.published_at == '1970-01-01'
