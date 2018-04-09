from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

#class LoginForm(FlaskForm):
	#username = StringField('What\'s your name?', validators=[DataRequired()])
	#user_location = StringField('Where would you like to search?', validators=[DataRequired()])
	#submit = SubmitField('Onward')

class countForm(FlaskForm):
	query = StringField('Probably or maybe?', validators=[DataRequired()])
	submit = SubmitField('submit')
