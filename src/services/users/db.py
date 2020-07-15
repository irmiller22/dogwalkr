from contextlib import ContextDecorator
from datetime import datetime
from typing import Any, List, Optional, Tuple

from sqlalchemy import func, Column, Integer, String
from sqlalchemy.types import DateTime

from ..common.db import Session
from ..common.models import Base


class UserDAO(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class UsersContextManager(ContextDecorator):
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        try:
            if exc_type:
                self.session.rollback()
                return False
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_users(
        self, user_id: Optional[int] = None, name: Optional[str] = None,
    ) -> Tuple[List[UserDAO], int]:
        """
        Gets Userg objects based on parameters passed in.
        :param name str:        Name of user.
        :param user_id int:     ID of user.
        :rtype: list(UserDAO), int
        """
        if not (name or user_id):
            raise Exception("A parameter must be passed.")
        if name and user_id:
            raise Exception("Only one parameter maybe passed.")

        query = self.session.query(UserDAO)
        if name:
            query = query.filter(UserDAO.name == name)
        if user_id:
            query = query.filter(UserDAO.id == user_id)

        # count
        count = self._get_count(query)

        daos = query.all()
        return daos, count

    def get_user_by_id(self, user_id: int) -> Optional[UserDAO]:
        """
        Get user by ID.

        :param user_id int: ID of user.
        :rtype: UserDAO or None
        """
        if not user_id:
            raise Exception("The 'user_id' parameter must be passed.")

        dao = self.session.query(UserDAO).filter_by(id=user_id).one_or_none()
        return dao

    def create_user(self, name: str) -> UserDAO:
        """
        Create user.

        :param user_id int: ID of user.
        :rtype: UserDAO
        """
        now = datetime.utcnow()
        dao = UserDAO(name=name, created_at=now, updated_at=now)
        self.session.add(dao)
        self.session.commit()

        return dao

    @staticmethod
    def _get_count(query: Any) -> int:
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        count = query.session.execute(count_q).scalar()
        return count
