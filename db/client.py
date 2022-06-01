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
        db_dialect = os.getenv('DB_DIALECT')
        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASS')
        db_name = os.getenv('DB_NAME')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')

        app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_dialect}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db.init_app(app)
        self.migrate.init_app(app, self.db)

    def commit(self) -> None:
        """A simple wrapper for the `commit` method of the `SQLAlchemy.session` instance."""
        self.db.session.commit()

    def add(self, obj: Any) -> None:
        """A simple wrapper for the `add` method of the `SQLAlchemy.session` instance."""
        self.db.session.add(obj)
