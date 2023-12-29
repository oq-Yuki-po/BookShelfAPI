import os
from datetime import datetime
from urllib.parse import quote_plus

from sqlalchemy import Column, DateTime, MetaData, create_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

# Engine
SERVER = os.getenv('POSTGRES_SERVER')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')
PORT = os.getenv('POSTGRES_PORT')

Engine = create_engine(
    "postgresql://{}:{}@{}:{}/{}?client_encoding=utf8".format(USER, quote_plus(PASSWORD), SERVER, PORT, DB),
    echo=False
)

# Session
session = scoped_session(
    sessionmaker(Engine,
                 autoflush=False,
                 autocommit=False)
)


class BaseModel(object):
    """BaseModel

    BaseModel is a base class for all models.
    It provides the following attributes:
        - created_at: A datetime object that represents the date and time
        when the object was created.
        - updated_at: A datetime object that represents the date and time
        when the object was updated.
    """
    __table_args__ = {'schema': os.environ.get('DB_SCHEMA', None)}

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.now, nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=datetime.now, nullable=False)


metadata = MetaData(naming_convention={
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
})

BaseModel = declarative_base(cls=BaseModel, metadata=metadata)
