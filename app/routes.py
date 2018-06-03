from flask import request, make_response, render_template
from app import app
import os
import json
from lesscss import LessCSS

LessCSS(media_dir='static', exclude_dirs=['img', 'src', 'json_files'], based=True, compression='x')
prepositions = ['maybe', 'probably']

def load_json(filename):
    with open(filename) as json_data:
        #load json file
        parsed_json = json.load(json_data)

        return parsed_json

@app.route('/', methods=['GET', 'POST'])
def index():
    title = 'test'
    
    return render_template('index.html', title=title, prepositions = prepositions)

@app.route('/<preposition>')
def detail(preposition):
    template='detail.html'
    filename = os.path.join(app.root_path, 'static/json_files/', '%s-details.json' %(preposition)) 
    details = load_json(filename)
    count = len(details)
    	
    return render_template(template, preposition=preposition, details=details, count=count)