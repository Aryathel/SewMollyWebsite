import os

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from db import Client
from db.models import User
from forms import SignupForm, LoginForm


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_client = Client(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'


# ---------- Primary Routes ----------
@app.route('/', methods=['GET', 'POST'])
def home():
    login_form = LoginForm()
    signup_form = SignupForm()

    source = request.args.get('source')

    if source == 'login':
        if login_form.validate_on_submit():
            login(login_form)
            return redirect(url_for('home'))

        return render_template(
            'home.html',
            title='Sew Molly | Home',
            logged_in=False,
            login_form=login_form,
            signup_form=signup_form,
            show_login=True
        )
    elif source == 'signup':
        if signup_form.validate_on_submit():
            signup(signup_form)
            return redirect(url_for('home'))

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


# ---------- Auth ----------
def login(form: LoginForm):
    user = form.user
    user.remember_me = form.remember_me.data
    db_client.commit()

    login_user(user, remember=user.remember_me)


def signup(form: SignupForm):
    user = form.user
    db_client.add(user)
    db_client.commit()

    login_user(user, remember=user.remember_me)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))


# ---------- User Routes ----------
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return 'Profile'


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True, port=6894)
