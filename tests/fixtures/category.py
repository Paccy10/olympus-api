""" Module for category fixtures """

import pytest

from api.models.category import Category


@pytest.fixture(scope='module')
def new_category(init_db):
    """ New category fixture """

    return Category(name='apartment')


@pytest.fixture(scope='module')
def another_category(init_db):
    """ New category fixture """

    return Category(name='test')
