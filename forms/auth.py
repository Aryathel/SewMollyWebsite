from typing import Optional

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo, Length

from db.models import User
from .validators import user, user_password


class SignupForm(FlaskForm):
    __user: Optional[User] = None

    signup_username = StringField(
        'Username',
        validators=[
            InputRequired("Please provide a username."),
            Length(min=3, max=32),
            user(exists=False)
        ]
    )
    email = EmailField(
        'Email',
        validators=[
            InputRequired("Please provide an email."),
            Email(),
            Length(min=6, max=48),
            user(exists=False)
        ]
    )
    signup_password = PasswordField(
        'Password',
        validators=[
            InputRequired("Please provide a password."),
            Length(min=4, max=64)
        ]
    )
    confirm = PasswordField(
        'Confirm Password',
        validators=[
            InputRequired("Please confirm your password."),
            EqualTo(
                'signup_password',
                message='Passwords must match.'
            )
        ]
    )
    signup_remember_me = BooleanField('Remember Me')
    signup_submit = SubmitField('Sign Up')

    @property
    def username(self) -> StringField:
        return self.signup_username

    @property
    def password(self) -> PasswordField:
        return self.signup_password

    @property
    def remember_me(self) -> BooleanField:
        return self.signup_remember_me

    @property
    def submit(self) -> SubmitField:
        return self.signup_submit

    @property
    def user(self) -> Optional[User]:
        if not self.__user and self.is_submitted():
            self.__user = User(
                username=self.signup_username.data,
                email=self.email.data,
                password=self.signup_password.data,
                remember_me=self.signup_remember_me.data
            )
        return self.__user


class LoginForm(FlaskForm):
    __user: Optional[User] = None

    login_username = StringField(
        'Username or Email',
        validators=[
            InputRequired("Please provide a username or email."),
            Length(min=3, max=32),
            user()
        ]
    )
    login_password = PasswordField(
        'Password',
        validators=[
            InputRequired("Please provide a password."),
            Length(min=4, max=64),
            user_password
        ]
    )
    login_remember_me = BooleanField('Remember Me')
    login_submit = SubmitField('Log In')

    @property
    def username(self) -> StringField:
        return self.login_username

    @property
    def password(self) -> PasswordField:
        return self.login_password

    @property
    def remember_me(self) -> BooleanField:
        return self.login_remember_me

    @property
    def submit(self) -> SubmitField:
        return self.login_submit

    @property
    def user(self) -> Optional[User]:
        if not self.__user and self.is_submitted():
            self.__user = User.get_by_name_or_email(self.username.data)
        return self.__user
