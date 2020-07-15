from contextlib import ContextDecorator
from datetime import datetime
from typing import Any, List, Optional, Tuple

from sqlalchemy import func, desc, Column, ForeignKey, Integer, String
from sqlalchemy.types import DateTime

from .constants import DOG_ORDER_QUERY_PARAM_MAP
from ..common.db import Session
from ..common.models import Base
from ..users.db import UsersContextManager


class DogDAO(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class DogsContextManager(ContextDecorator):
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

    def get_dogs(
        self,
        name: Optional[str] = None,
        owner_ids: Optional[List[int]] = None,
        sort: Optional[str] = "created_at",
        order: Optional[str] = "desc",
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> Tuple[List[DogDAO], int]:
        """
        Gets Dog objects based on parameters passed in.
        :param name str:                      Name of dog.
        :param owner_ids list(int):           List of owner IDs.
        :param sort str:                      Attribute to sort by.
        :param order str:                     Sort order ('asc' or 'desc').
        :param limit int:                     Limit for results in response.
        :param offset int:                    Offset for results in response.
        :rtype: list(DogDAO), int
        """
        if not (name or owner_ids):
            raise Exception("A parameter must be passed.")

        query = self.session.query(DogDAO)
        if name:
            query = query.filter(DogDAO.name == name)
        if owner_ids:
            query = query.filter(DogDAO.owner_id.in_(owner_ids))

        # count
        count = self._get_count(query)

        # prep query for meta preferences
        sort_order = DOG_ORDER_QUERY_PARAM_MAP[order]
        if sort:
            query = query.order_by(sort_order(getattr(DogDAO, sort)))
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        daos = query.all()
        return daos, count

    def get_dog_by_id(self, dog_id: int) -> Optional[DogDAO]:
        """
        Get dog by ID.

        :param dog_id int: ID of dog.
        :rtype: DogDAO or None
        """
        if not dog_id:
            raise Exception("The 'dog_id' parameter must be passed.")

        dao = self.session.query(DogDAO).filter_by(id=dog_id).one_or_none()
        return dao

    def create_dog(self, name: str, owner_id: int) -> DogDAO:
        """
        Create dog.

        :param name str: Name of dog.
        :param owner_id int: ID of owner.
        :rtype: DogDAO
        """
        now = datetime.utcnow()

        with UsersContextManager() as manager:
            owner = manager.get_user_by_id(user_id=owner_id)
            if not owner:
                raise Exception(f"User with ID {owner_id} does not exist.")

        dao = DogDAO(name=name, owner_id=owner_id, created_at=now, updated_at=now)
        self.session.add(dao)
        self.session.commit()

        return dao

    @staticmethod
    def _get_count(query: Any) -> int:
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        count = query.session.execute(count_q).scalar()
        return count
