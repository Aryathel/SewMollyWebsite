from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


class ClientModel:
    db: SQLAlchemy = db
    migrate: Migrate = migrate

    def __init__(self, app: Flask) -> None:
        self.db.init_app(app)
        self.migrate.init_app(app, self.db)
