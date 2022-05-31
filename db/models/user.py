from typing import TypeVar, Optional, Type

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func

from ..client import db, bcrypt

UserModelType = TypeVar('UserModelType', bound='UserModel')


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    _password = db.Column(db.String())
    authenticated = db.Column(db.Boolean, default=False, nullable=False)
    remember_me = db.Column(db.Boolean, default=False, nullable=False)
    google_token = db.Column(db.String())
    icon = db.Column(db.String())
    default_name = db.Column(db.Boolean)

    def __init__(
            self,
            username: str,
            email: str,
            password: str = None,
            authenticated: bool = False,
            remember_me: bool = False,
            google_token: str = None,
            icon: str = None,
            default_name: bool = False
    ) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.authenticated = authenticated
        self.remember_me = remember_me
        self.google_token = google_token
        self.icon = icon
        self.default_name = default_name

    @hybrid_property
    def password(self) -> db.Column:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        if password:
            self._password = bcrypt.generate_password_hash(password).decode('utf-8')
        else:
            self._password = password

    def check_password(self, password: str) -> bool:
        if self._password and bcrypt.check_password_hash(self._password, password):
            return True
        return False

    def is_active(self) -> bool:
        return True

    def get_id(self) -> str:
        return str(self.id)

    def is_authenticated(self) -> bool:
        return self.authenticated

    def is_anonymous(self) -> bool:
        return False

    @property
    def already_exists(self) -> bool:
        cls: Type[UserModelType] = self.__class__
        return cls.get_by_email(self.email) is not None

    @classmethod
    def get_by_name_or_email(cls, val: str) -> Optional[UserModelType]:
        user = cls.get_by_name(val)
        if not user:
            user = cls.get_by_email(val)
        return user

    @classmethod
    def get_by_name(cls, username: str) -> Optional[UserModelType]:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email: str) -> Optional[UserModelType]:
        return cls.query.filter(func.lower(cls.email) == func.lower(email)).first()

    def __repr__(self) -> str:
        return f'<User id={self.id} username="{self.username}">'

    def __str__(self) -> str:
        return self.__repr__()
