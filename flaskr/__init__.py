import os

from flask import Flask

def create_app(test_config=None):
	# Create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load test config, if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass


	# A simple page to syat hello
	@app.route('/hello')
	def hello():
		return 'Hello, world!'

	# --------------------------------------------------------------------------------
	# Import and call this function from the factory. 
	# Place the new code at the end of the factory function before returning the app
	# --------------------------------------------------------------------------------
	from . import db
	db.init_app(app)

	# --------------------------------------------------------------------------------
	# Import and register the blueprint from the factory using app.register_blueprint(). 
	# Place the new code at the end of the factory function before returning the app.
	# --------------------------------------------------------------------------------
	from . import auth
	app.register_blueprint(auth.bp)

	from . import blog
	app.register_blueprint(blog.bp)

	app.add_url_rule('/', endpoint='index')

	return app

# ---------------------------------------------------------------
#
#	Notas del tutorial
#	https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
#
# ---------------------------------------------------------------
# create_app is the application factory function. 
# You'll add to it later in the tutorial, but it already does a lot
# 
# app = Flask(__name__, instance_relative_config=True) creates the Flask instance.
# 
# __name__ is the name of the current Python module. 
# The app needs to know where it's located to set up some paths, 
# and __name__ is a convenient way to tell it that.
# 
# instance_relative_config=True tells the app that configuration files are 
# relative to the instance folder. 
# The instance folder is located outside the flaskr package and can hold local 
# data that shouldn't be committed to version control, such as configuration 
# secrets and the database file.
# 
# app.config.from_mapping() sets some default configuration that the app will use:
# 
# SECRET_KEY is used by Flask and extensions to keep data safe. 
# It's set to 'dev' to provide a convenient value during development, 
# but it should be overridden with a random value when deploying.
# 
# DATABASE is the path where the SQLite database file will be saved. 
# It's under app.instance_path, which is the path that Flask has chosen 
# for the instance folder. 
# 
# app.config.from_pyfile() overrides the default configuration with values 
# taken from the config.py file in the instance folder if it exists. 
# For example, when deploying, this can be used to set a real SECRET_KEY.
# 
# test_config can also be passed to the factory, and will be used instead of 
# the instance configuration. 
# This is so the tests you'll write later in the tutorial can be configured 
# independently of any development values you have configured.
# 
# os.makedirs() ensures that app.instance_path exists. 
# Flask doesn't create the instance folder automatically, but it needs to 
# be created because your project will create the SQLite database file there.
# 
# @app.route() creates a simple route so you can see the application 
# working before getting into the rest of the tutorial. 
# It creates a connection between the URL /hello and a function that 
# returns a response, the string 'Hello, World!' in this case.


# ---------------------------------------------------------------------
#	Run the app
# ---------------------------------------------------------------------
# (venv) pi@rpi2:~/dev/flask $ export FLASK_APP=flaskr
# (venv) pi@rpi2:~/dev/flask $ export FLASK_ENV=development
# (venv) pi@rpi2:~/dev/flask $ flask run
 # * Serving Flask app "flaskr" (lazy loading)
 # * Environment: development
 # * Debug mode: on
 # * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 # * Restarting with stat
 # * Debugger is active!
 # * Debugger PIN: 420-823-017

