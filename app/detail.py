from app.clean import *

class Preposition:
    def __init__(self, data, query):
        self.data = data
        self.query = query
        self.categories = make_dict(data, query)
        print(categories)