from typing import TypeVar, Optional

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from ..client import db, bcrypt

UserModelType = TypeVar('UserModelType', bound='UserModel')


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    _password = db.Column(db.String(), nullable=False)
    authenticated = db.Column(db.Boolean, default=False, nullable=False)
    remember_me = db.Column(db.Boolean, default=False, nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        if bcrypt.check_password_hash(self._password, password):
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

    @classmethod
    def get_by_name_or_email(cls, val: str) -> Optional[UserModelType]:
        user = cls.query.filter_by(username=val).first()
        if not user:
            user = cls.query.filter_by(email=val).first()
        return user

    def __repr__(self) -> str:
        return f'<User id={self.id} username="{self.username}">'

    def __str__(self) -> str:
        return self.__repr__()
