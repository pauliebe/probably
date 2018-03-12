import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = True
	TESTING = False
	CSRF_Enabled = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'a key'

class ProductionConfig(Config):
	DEBUG = False

class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
	