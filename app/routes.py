from flask import request, make_response, render_template
from app import app
import os
from app.clean import make_dict, load_json
from lesscss import LessCSS

LessCSS(media_dir='static', exclude_dirs=['img', 'src', 'json_files'], based=True, compression='x')
prepositions = ['maybe', 'probably']

@app.route('/', methods=['GET', 'POST'])
def index():
    title = 'test'
    
    return render_template('index.html', title=title, prepositions = prepositions)

@app.route('/<preposition>')
def detail(preposition):
    template='detail.html'
    filename = os.path.join(app.root_path, 'static/json_files/', '%s.json' %(preposition)) 
    data = load_json(filename)
    details=make_dict(data,preposition, app.root_path)
    count = len(details)
    	
    return render_template(template, preposition=preposition, details=details, count=count)