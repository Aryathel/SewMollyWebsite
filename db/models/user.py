from ..client import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def is_active(self) -> bool:
        return True

    def get_id(self) -> int:
        return self.id

    def is_authenticated(self) -> bool:
        return self.authenticated

    def is_anonymous(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f'<User id={self.id} username="{self.username}">'

    def __str__(self) -> str:
        return self.__repr__()
