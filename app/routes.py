from flask import request, make_response, render_template
from app import app
import os
from app.clean import *
#from app.forms import countForm


prepositions = ['maybe', 'probably']

@app.route('/', methods=['GET', 'POST'])
def index():
    title = 'test'
    
    return render_template('index.html', title=title, prepositions = prepositions)

@app.route('/<preposition>')
def detail(preposition):
    query = preposition
    template='detail.html'
    filename = os.path.join(app.root_path, 'json_files/combined/', '%s.json' %(query))
    categories = make_dict(filename, query)
    
    return render_template(template, preposition=preposition, categories= categories)