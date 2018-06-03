import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = True
	CSRF_Enabled = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'a key'