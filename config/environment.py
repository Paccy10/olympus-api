""" Module for the application configurations """

import sys
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """ App base configurations """

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = getenv('MAIL_SERVER')
    MAIL_PORT = getenv('MAIL_PORT')
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = getenv('MAIL_USE_TLS')


class ProductionConfig(Config):
    """ App testing configurations """

    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    """ App Development configurations """

    PORT = 5000
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')


class TestingConfig(Config):
    """ App testing configurations """

    SQLALCHEMY_DATABASE_URI = getenv('TEST_DATABASE_URL')
    FLASK_ENV = 'testing'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

AppConfig = TestingConfig if 'pytest' in sys.modules else config.get(
    getenv('FLASK_ENV'), 'development')
