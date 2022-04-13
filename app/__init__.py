import os

from flask import Flask, redirect, url_for
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.main import main as main_blueprint
app.register_blueprint(main_blueprint)

from app.webadmin import webadmin as webadmin_blueprint
app.register_blueprint(webadmin_blueprint)

from .models import *


@app.get('/')
def main():
    return redirect(url_for('main.index'))
