from sqlalchemy import select

from app.models import AuthorModel
from app.models.factories import AuthorModelFactory


class TestAuthorModel:

    def test__is_duplicated_is_true(self, db_session):
        """Test for _is_duplicated method of AuthorModel
        with duplicated name
        """
        # Prepare
        test_name = 'test_name'
        AuthorModelFactory(name=test_name)
        db_session.commit()

        # Execute
        author = AuthorModel(name=test_name)

        # Assert
        assert author._is_duplicated() is True

    def test__is_duplicated_is_false(self):
        """Test for _is_duplicated method of AuthorModel
        with non-duplicated name
        """
        # Prepare
        test_name = 'test_name'

        # Execute
        author = AuthorModel(name=test_name)

        # Assert
        assert author._is_duplicated() is False

    def test_save_successfully(self, db_session):
        """Test for save method of AuthorModel
        with successful case
        """
        # Prepare
        test_name = 'test_name'

        # Execute
        saved = AuthorModel.save(name=test_name)

        # Assert
        assert saved is True
        stmt = select(AuthorModel).where(AuthorModel.name == test_name)
        result = db_session.execute(stmt).scalars().first()
        assert result is not None
        assert result.name == test_name

    def test_save_with_duplicated_name(self, db_session):
        """Test for save method of AuthorModel
        with duplicated name
        """
        # Prepare
        test_name = 'test_name'
        AuthorModelFactory(name=test_name)
        db_session.commit()

        # Execute
        saved = AuthorModel.save(name=test_name)

        # Assert
        assert saved is False
        stmt = select(AuthorModel).where(AuthorModel.name == test_name)
        result = db_session.execute(stmt).scalars().first()
        assert result is not None
        assert result.name == test_name
