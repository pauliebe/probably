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
	template='submit.html'
	filename = os.path.join(app.root_path, 'json_files/combined/', '%s.json' %(preposition))
	count = 15
	total = count_total(filename)
	count_list = count_common(preposition, filename, count)
	bigrams_list = count_bigrams(preposition, filename)
	after_query_list = after_query(preposition, filename)
	
	return render_template(template, preposition=preposition, count_list=count_list, count=count, count_total = total)