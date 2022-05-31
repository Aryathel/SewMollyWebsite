from typing import Any, Optional

from flask import abort, redirect, url_for, render_template
from flask_login import logout_user, login_user, login_required

from db.models import User
from forms import LoginForm, SignupForm

from ._framework import Scheme, Route


class Users(Scheme, name="users", module=__name__):
    """Routes relating to users.

    Attributes
    ----------
    app - `.main.App`
        The active App object which is the parent of the blueprint.
    blueprint - `flask.Blueprint`
        The blueprint structure that is being created.

    Methods
    ----------
    auth.confirm_email - "/confirm/<token>"
        The confirmation callback url to authenticate a user's email.

    auth.logout - "/logout"
        Logs out the user who is sending the request, then redirects home.
    """
    class Logout(Route, route='/logout', endpoint='logout', methods=['GET']):
        def callback(self) -> Any:
            """Logs out the user who sent the request.

            Returns
            ---------
            main.home - "/"
                Redirects back to the home page after the user is logged out.
            """
            logout_user()
            return redirect(url_for('main.home'))

    class Profile(Route, route='/profile', endpoint='profile', methods=['GET']):
        @login_required
        def callback(self) -> Any:
            """Gets the user's profile."""
            return 'Profile'

    def login(self, form: LoginForm) -> None:
        """Logs a user in.

        Parameters
        ----------
        form - `forms.LoginForm`
            The form from which to pull the data about which user to log in.
        """
        # Get the user from the form and update it according to the "remember me" field.
        user = form.user
        user.remember_me = form.remember_me.data
        self.app.db_client.commit()

        # Log the user in.
        login_user(user, remember=user.remember_me)

    def signup(self, form: SignupForm) -> Optional[User]:
        """Registers a new user.

        Adds the user to the database, and sends a verification email to their
        registered email address.

        Parameters
        ----------
        form - `forms.SignupForm`
            The form from which to construct the new `db.models.User`.

        Returns
        ---------
        Optional[db.models.User]
            The new user entry which has been created.
        """
        # Add user to database.
        user = form.user
        self.app.db_client.add(user)
        self.app.db_client.commit()

        # Log the user in.
        login_user(user, remember=user.remember_me)

        # Send an email to the user.
        subject = "Sew Molly Email Confirmation"

        token = self.app.ts.dumps(user.email, salt='email-confirm-key')
        confirm_url = url_for(
            'callbacks.email_confirmation',
            _external=True
        ) + f'?token={token}'

        html = render_template(
            'email/confirmation.html',
            confirmation_url=confirm_url
        )

        self.app.mail.send_message_async(
            subject=subject,
            sender="houghtonawe@gmail.com",
            recipients=[user.email],
            html=html
        )

        return user
