""" Module for tests configuration """

import pytest

from config.server import application
from api.models.database import db


pytest_plugins = ['tests.fixtures.user',
                  'tests.fixtures.authorization',
                  'tests.fixtures.category',
                  'tests.fixtures.type',
                  'tests.fixtures.property',
                  'tests.fixtures.booking']


@pytest.fixture(scope='module')
def app():
    """ Setup flask test application """

    return application


@pytest.fixture(scope='module')
def init_db(app):
    """ Initialize the test database """

    db.drop_all()
    db.create_all()
    yield db
    db.session.close()
