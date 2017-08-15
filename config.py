import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    CSRF_ENABLED = True
    THREADED=True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://bocauser:boca@localhost/bocadb'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgresql+psycopg2://bocauser:boca@localhost/bocadb'

class ProductionConfig(Config):
    HOST = '0.0.0.0'
    CSRF_ENABLED = True
    THREADED=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql+psycopg2://bocauser:boca@localhost/bocadb'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
