import base64
import os
from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from sqlalchemy.sql.ddl import CreateSchema, DropSchema
from sqlalchemy_utils import database_exists
from sqlalchemy_utils.functions.database import create_database

from app.main import app
from app.models import BaseModel, Engine, session
from app.services.login_service import LoginService, TokenData


def remove_session() -> None:

    session.close()


@pytest.fixture(scope='session', autouse=True)
def setup_test_env(request):

    if not database_exists(Engine.url):
        create_database(Engine.url)

    schema_name: str = os.environ.get('DB_SCHEMA', 'test')

    stmt = CreateSchema(schema_name, if_not_exists=True)
    with Engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

    def drop_schema():
        stmt = DropSchema(schema_name)
        with Engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

    request.addfinalizer(drop_schema)

    return setup_test_env


def drop_all_tables():
    remove_session()
    BaseModel.metadata.drop_all(Engine)


@pytest.fixture(scope='function', autouse=True)
def setup_tables_at_function(request):

    BaseModel.metadata.drop_all(Engine)
    BaseModel.metadata.create_all(Engine)

    request.addfinalizer(drop_all_tables)

    return setup_tables_at_function


@pytest.fixture(scope='class', autouse=True)
def setup_tables_at_class(request):

    BaseModel.metadata.drop_all(Engine)
    BaseModel.metadata.create_all(Engine)

    request.addfinalizer(drop_all_tables)

    return setup_tables_at_class


@pytest.fixture()
def app_client():
    return TestClient(app)


@pytest.fixture()
def db_session(request):

    request.addfinalizer(remove_session)
    return session


@pytest.fixture()
def make_image(tmpdir):
    """make image and save to temp dir and return image path
    """
    def _make_image(image_name: str):
        """_make_image_

        Parameters
        ----------
        image_name : str
            save image name
        Returns
        -------
        str
            image path
        """
        image_path = str(tmpdir.join(image_name))
        image = Image.new('RGB', (100, 100))
        image.save(image_path)
        return image_path
    return _make_image


@pytest.fixture()
def change_dir():
    """change directory to app root
    """
    cwd = os.getcwd()
    os.chdir(os.path.join(cwd, 'app'))
    yield
    os.chdir(cwd)


@contextmanager
def create_user_mock(role: str):
    """create_user_mock
    """
    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[LoginService.verify_token] = lambda: TokenData(user_name="test_user", role=role)
    try:
        yield
    finally:
        app.dependency_overrides = original_overrides


@pytest.fixture()
def override_verify_token_dependency():
    """override_verify_token_dependency
    """
    def _override(role: str):
        return create_user_mock(role)

    return _override


@pytest.fixture()
def encode_image_base64():
    """encode_image_base64
    image_path -> base64 encoded image
    """
    def _encode(image_path: str):
        with open(image_path, 'rb') as f:
            img = f.read()
        return base64.b64encode(img)

    return _encode
