#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
            """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        Saves new user to database
        '''
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''
        Finds user based on arbitrary args
        '''
        allowed = {attr for attr in dir(User) if not attr.startswith("_")}
        fields = set(kwargs.keys())
        if not fields.issubset(allowed):
            raise InvalidRequestError
        match = self._session.query(User).all()
        for row in match:
            is_match = [getattr(row, key) == kwargs[key] for key in kwargs]
            if all(is_match):
                return row
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        '''
        use find_user_by to locate the user to update
        '''
        allowed = {attr for attr in dir(User) if not attr.startswith("_")}
        fields = set(kwargs.keys())
        if not fields.issubset(allowed):
            raise ValueError
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        self._session.commit()
