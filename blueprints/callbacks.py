from typing import Any

from flask import redirect, url_for, session, abort
from flask_login import login_user
from flask_pydantic import validate
from pydantic import BaseModel

from db.models import User

from ._framework import Scheme, Route


class EmailQuery(BaseModel):
    token: str


class Callbacks(Scheme, name="callbacks", module=__name__, url_prefix="/callback"):
    class EmailCallback(
        Route,
        route='/activate_email',
        endpoint='email_confirmation',
        methods=['GET']
    ):
        @validate()
        def callback(self, query: EmailQuery) -> Any:
            """The confirmation callback route to authenticate a user's email.

            Parameters
            ----------
            token - `str`
                The serialized token containing the email of the user
                to authorize.

            Returns
            ----------
            main.home - "/"
                A redirect to the home page after a successful confirmation.

            Raises
            ----------
            404
                Decrypting the email token ran into an error,
                likely to to an expired token.
            """
            try:
                email = self.app.ts.loads(query.token, salt='email-confirm-key', max_age=86400)
            except Exception as e:
                return abort(404, e)

            user = User.query.filter_by(email=email).first_or_404()
            user.authenticated = True
            self.app.db_client.commit()

            return redirect(url_for('main.home'))

    class GoogleAuth(Route, route='/login/google', endpoint="google_login", methods=['GET']):
        def callback(self) -> Any:
            data = self.app.google_auth.get_token()

            user = User(
                username=data['verify']['name'],
                email=data['verify']['email'],
                icon=data['verify']['picture'],
                google_token=data['token']['token'],
                authenticated=True,
                remember_me=True,
                default_name=True
            )

            if not user.already_exists:
                self.app.db_client.add(user)
            else:
                user: User = User.get_by_email(data['verify']['email'])
                user.google_token = data['token']['token']
                user.authenticated = True
                user.remember_me = True
                if not user.icon:
                    user.icon = data['verify']['picture']
                if user.default_name:
                    user.username = data['verify']['name']
            self.app.db_client.commit()

            login_user(user, remember=user.remember_me)

            res = redirect(session.get('callback', redirect(url_for('main.home'))))
            del session['callback']
            return res

