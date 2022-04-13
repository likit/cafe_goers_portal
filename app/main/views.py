from . import main


@main.get('/')
def index():
    return 'Welcome to Cafe Search Engine'