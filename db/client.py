from typing import Any
import os

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
        DB_USER = os.getenv('DB_USER')
        DB_PASS = os.getenv('DB_PASS')
        DB_NAME = os.getenv('DB_NAME')
        DB_HOST = os.getenv('DB_HOST')
        DB_PORT = os.getenv('DB_PORT')

        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db.init_app(app)
        self.migrate.init_app(app, self.db)

    def commit(self) -> None:
        """A simple wrapper for the `commit` method of the `SQLAlchemy.session` instance."""
        self.db.session.commit()

    def add(self, obj: Any) -> None:
        """A simple wrapper for the `add` method of the `SQLAlchemy.session` instance."""
        self.db.session.add(obj)
