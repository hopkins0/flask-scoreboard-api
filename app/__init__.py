from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_




bootstrap = Bootstrap()
moment = Moment()



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('postgresql+psycopg2://bocauser:boca@localhost/bocadb', echo=True)
engine = None
Base = None
session = None




def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	bootstrap.init_app(app)
	app.config['BOOTSTRAP_SERVE_LOCAL'] = True


	global engine
	global Base
	engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
	# engine = create_engine('postgresql+psycopg2://bocauser:boca@localhost/bocadb', echo=True)
	Base = declarative_base(engine)

	global session
	import main.contest
	session = main.contest.loadSession()

	# app.register_module(index, url_prefix='/main/views')
	from main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	
	return app
