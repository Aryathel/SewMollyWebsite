from typing import Optional, Any, Dict
import os
from json import dumps

from flask import Flask, url_for
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer

from db import Client
from db.models import User
from utils import Mail, Framework, Google, sort_nested_dict

from .main import Main
from .users import Users
from .callbacks import Callbacks


class App(Flask, Framework):
    """The primary overhead for the entire project structure."""
    db_client: Client
    mail: Mail
    ts: URLSafeTimedSerializer
    login_manager: LoginManager
    google_auth: Google

    main: Main
    users: Users
    callbacks: Callbacks

    def __post_init__(self, *args, **kwargs):
        """Initialize the app and all of its modules.

        This app takes a modular structure with the intention of easily
        making large additions or removals with less hassle.
        """
        # Load secret key from environment.
        self.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

        # Load modules
        self.db_client = Client(self)
        self.mail = Mail(self)
        self.ts = URLSafeTimedSerializer(self.config['SECRET_KEY'])

        self.login_manager = LoginManager(self)
        self.login_manager.login_view = 'main.home'
        self.login_manager.user_loader(self.user_loader)

        self.google_auth = Google()

        # Load blueprints
        self.main = Main(self)
        self.users = Users(self, children=[Callbacks])

        # Register additional handlers
        self.register_error_handler(404, self.error_404)

        self.context_processor(self.inject_google_auth)

    def inject_google_auth(self):
        return dict(
            google_auth=self.google_auth.get_redirect()
        )

    @staticmethod
    def user_loader(user_id: str) -> Optional[User]:
        """The user loader for the `Flask-Login` module."""
        return User.query.get(user_id)

    def error_404(self, e) -> Any:
        return "Could not find that page.<br><br>" + str(e)

    def site_map(self, full: bool = False, raw: bool = False, pretty: bool = False):
        rules = {}
        for rule in self.url_map.iter_rules():
            if (full or (not full and 'GET' in rule.methods)) and self._has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                rules[rule.endpoint] = url

        res = rules
        if not raw:
            res = {}
            for endpoint, url in rules.items():
                paths = endpoint.split('.')
                tmp = res
                for i, path in enumerate(paths):
                    if i >= len(paths)-1:
                        tmp[path] = (endpoint, url)
                    elif path not in tmp:
                        tmp[path] = {}
                    tmp = tmp[path]

        res = sort_nested_dict(res)

        return dumps(res, indent=2) if pretty else res

    @staticmethod
    def _has_no_empty_params(rule) -> bool:
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)
