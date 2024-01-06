from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, select

from app.models.setting import BaseModel, Engine, session


class AuthorModel(BaseModel):
    """
    AuthorModel

    Attributes
    ----------
    id : int
        author id
    name : str
        author name
    """
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True)

    def __init__(self,
                 name: str,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:

        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def save(cls, name: str) -> bool:
        """
        Save author

        Parameters
        ----------
        name : str
            author name

        Returns
        -------
        bool
            True if saved successfully
        """
        author = cls(name=name)

        if author._is_duplicated():
            return False
        else:
            session.add(author)
            session.flush()
            return True

    def _is_duplicated(self) -> bool:
        """
        Check if author is duplicated

        Returns
        -------
        bool
            True if author is duplicated
        """
        stmt = select(AuthorModel).where(AuthorModel.name == self.name)
        result = session.execute(stmt).scalars().one_or_none()
        if result is None:
            return False
        else:
            return True

    @classmethod
    def fetch_by_names(cls, names: List[str]) -> AuthorModel:
        """
        Fetch author by name

        Parameters
        ----------
        name : str
            author name

        Returns
        -------
        AuthorModel
            AuthorModel object
        """
        stmt = select(AuthorModel).where(AuthorModel.name.in_(names))
        result = session.execute(stmt).scalars().all()
        return result


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=Engine)
