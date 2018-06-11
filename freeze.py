from flask_frozen import Freezer
from app import app
from app.routes import load_json
import os

freezer = Freezer(app)
prepositions = ['probably', 'maybe', 'perhaps']

@freezer.register_generator
def detail():
    for preposition in prepositions:
        yield {'preposition' : preposition}

if __name__ == '__main__':
    freezer.freeze()