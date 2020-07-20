""" Module for the application configurations """

import sys
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """ App base configurations """

    DEBUG = False


class DevelopmentConfig(Config):
    """ App Development configurations """

    PORT = 5000
    DEBUG = True


class TestingConfig(Config):
    """ App testing configurations """

    PORT = 4000


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}

AppConfig = TestingConfig if 'pytest' in sys.modules else config.get(
    getenv('FLASK_ENV'), 'development')
