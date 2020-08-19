""" Module for type fixtures """

import pytest

from api.models.type import Type


@pytest.fixture(scope='module')
def new_type(init_db):
    """ New type fixture """

    return Type(name='shared room')


@pytest.fixture(scope='module')
def another_type(init_db):
    """ New type fixture """

    return Type(name='test')
