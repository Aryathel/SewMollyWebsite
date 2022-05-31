from typing import Any, Optional
from enum import Enum

from flask import url_for, render_template, request, redirect
from flask_login import current_user
from pydantic import BaseModel
from flask_pydantic import validate

from db.models import User
from forms import LoginForm, SignupForm

from ._framework import Scheme, Route


# ---------- Validators ----------
class HomeQuery(BaseModel):
    class _SourceOpts(Enum):
        login = "login"
        signup = "signup"

    source: Optional[_SourceOpts]


# ---------- Blueprint ----------
class Main(Scheme, name="main", module=__name__):
    """Standard root-level routes.

    Routes
    ----------
    home - "/"
        The index route, which returns the primary home page of the site.
    """

    class Home(Route, route='/', methods=['GET', 'POST'], endpoint="home"):
        @validate()
        def callback(self, query: HomeQuery) -> Any:
            login_form = LoginForm()
            signup_form = SignupForm()
            print(query.source)
            if query.source == 'login':
                if login_form.validate_on_submit():
                    self.app.users.login(login_form)
                    return redirect(url_for('main.home'))

                return render_template(
                    'home.html',
                    title='Sew Molly | Home',
                    logged_in=False,
                    login_form=login_form,
                    signup_form=signup_form,
                    show_login=True
                )
            elif query.source == 'signup':
                if signup_form.validate_on_submit():
                    self.app.users.signup(signup_form)
                    return redirect(url_for('main.home'))

                return render_template(
                    'home.html',
                    title='Sew Molly | Home',
                    logged_in=False,
                    login_form=login_form,
                    signup_form=signup_form,
                    show_signup=True
                )

            return render_template(
                'home.html',
                title='Sew Molly | Home',
                login_form=login_form,
                signup_form=signup_form,
                logged_in=isinstance(current_user, User),
                show_login=request.args.get('next') is not None
            )

    class SiteMap(Route, route='/sitemap', methods=['GET'], endpoint='sitemap'):
        def callback(self) -> Any:
            sitemap = self.app.site_map(full=True)
            return render_template('sitemap.html', sitemap=sitemap)
