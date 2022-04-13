from flask import Flask, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

from app.main import main as main_blueprint

app.register_blueprint(main_blueprint)


@app.get('/')
def main():
    return redirect(url_for('main.index'))
