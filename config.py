import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = True
	CSRF_Enabled = True
	SEND_FILE_MAX_AGE_DEFAULT = 20
	FREEZER_DESTINATION = ('../docs')
