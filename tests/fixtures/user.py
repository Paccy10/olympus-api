""" Module for user fixtures """

import pytest
from api.models.user import User
from api.utils.helpers.passwords_handler import hash_password


@pytest.fixture(scope='module')
def new_user(init_db):
    """ New user fixture """

    return User(firstname='John',
                lastname='Doe',
                email='john.doe@app.com',
                username='John',
                password=hash_password('Password1234'))


@pytest.fixture(scope='module')
def another_user(init_db):
    """ New user fixture """

    return User(firstname='Kelly',
                lastname='Doe',
                email='kelly.doe@app.com',
                username='Kelly',
                password=hash_password('Password1234'))
