import os

from flask import Flask, render_template
from flask_login import login_required, LoginManager

from db import Client
from db.models import User


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_client = Client(app)
login_manager = LoginManager(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', title='Sew Molly | Home')


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True, port=6894)
