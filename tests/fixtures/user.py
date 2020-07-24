""" Module for user fixtures """

import pytest
from api.models.user import User
from ..mocks.user import VALID_USER


@pytest.fixture(scope='module')
def new_user(init_db):
    """ New user fixture """

    return User(**VALID_USER)
