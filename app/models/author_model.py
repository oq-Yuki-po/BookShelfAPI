from sqlalchemy import Column, Integer, String

from app.models.setting import BaseModel, Engine


class AuthorModel(BaseModel):
    """
    AuthorModel
    """
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))

    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=Engine)
