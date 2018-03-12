from flask import request, make_response, render_template
from app import app
from app.forms import LoginForm

@app.route('/', methods=['GET', 'POST'])

def index():
	title = 'test'
	form = LoginForm()
	if form.validate_on_submit():
		name = form.username.data
		query = form.user_location.data
		#preposition_list = make_preposition_list(query)

		return render_template('submit.html', name=name, query=query)

	# this doesn't work as expected
	#elif (form.validate_on_submit() == False and request.method == ['POST']):
		#error = 'You have to type something!'
		#return render_template('index.html', title=title, form=form, error=error)
	
	else:
		print(request.method)

		return render_template('index.html', title=title, form=form)


# @app.route('/s', methods=['POST'])

# def temp():

# 	return make_response(form.username)

