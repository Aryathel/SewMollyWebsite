import os
from typing import Dict, Any, List

from flask import session, abort, request, url_for
from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests


def _verify_initialization(func):
    def decorator(cls: 'Google', *args, **kwargs):
        if not cls.initialized:
            cls.initialize()

        return func(cls, *args, **kwargs)

    return decorator


class Google:
    flow: Flow
    client_id: str

    _client_secrets_file: str
    _initialized: bool = False
    _scopes: List[str] = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ]

    def __init__(self):
        self._client_secrets_file = os.getenv('GOOGLE_SECRETS_FILE')
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')

    @property
    def initialized(self) -> bool:
        return self._initialized

    def initialize(self):
        self.flow = Flow.from_client_secrets_file(
            client_secrets_file=self._client_secrets_file,
            scopes=self._scopes,
            redirect_uri=url_for('users.callbacks.google_login', _external=True)
        )

    @_verify_initialization
    def get_redirect(self):
        auth_url, state = self.flow.authorization_url()
        session['state'] = state
        session['callback'] = request.url
        return auth_url

    @_verify_initialization
    def get_token(self):
        if not session['state'] == request.args['state']:
            abort(500, "State does not match.")

        self.flow.fetch_token(authorization_response=request.url)

        credentials = self.flow.credentials
        token_req = google.auth.transport.requests.Request()

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_req,
            audience=self.client_id
        )
        return {
            "token": self.credentials_to_token(credentials),
            "verify": id_info
        }

    @staticmethod
    def credentials_to_token(credentials: Credentials) -> Dict[str, Any]:
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
