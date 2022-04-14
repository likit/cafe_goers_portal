from flask import render_template

from . import main


@main.get('/')
def index():
    return render_template('main/index.html')