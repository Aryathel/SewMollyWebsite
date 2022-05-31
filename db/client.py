from typing import Any

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


class ClientModel:
    db: SQLAlchemy = db
    migrate: Migrate = migrate
    bcrypt: Bcrypt = bcrypt

    def __init__(self, app: Flask) -> None:
        self.db.init_app(app)
        self.migrate.init_app(app, self.db)

    def commit(self) -> None:
        """A simple wrapper for the `commit` method of the `SQLAlchemy.session` instance."""
        self.db.session.commit()

    def add(self, obj: Any) -> None:
        """A simple wrapper for the `add` method of the `SQLAlchemy.session` instance."""
        self.db.session.add(obj)
