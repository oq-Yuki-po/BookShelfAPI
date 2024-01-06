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

    def test_fetch_by_names(self, db_session):
        """Test for fetch_by_names method of AuthorModel"""
        # Prepare
        test_names = ['test_name1', 'test_name2']
        for name in test_names:
            AuthorModelFactory(name=name)
        db_session.commit()

        # Execute
        authors = AuthorModel.fetch_by_names(names=test_names)

        # Assert
        assert authors is not None
        assert len(authors) == len(test_names)
        for author in authors:
            assert author.name in test_names

    def test_fetch_by_names_with_non_exist_name(self, db_session):
        """Test for fetch_by_names method of AuthorModel
        with non-exist name
        """
        # Prepare

        # Execute
        authors = AuthorModel.fetch_by_names(names=['test_name3'])

        # Assert
        assert authors is not None
        assert not len(authors)
