""" Module for authorization fixtures """

import pytest

from api.schemas.user import UserSchema
from api.utils.tokens_handler import generate_auth_token


@pytest.fixture(scope='module')
def user_auth_header(init_db, new_user):
    """ user auth header fixture """

    new_user.save()
    new_user.update({'is_verified': True})
    user_schema = UserSchema()
    token = generate_auth_token(user_schema.dump(new_user)['id'])

    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture(scope='module')
def another_user_auth_header(init_db, another_user):
    """ user auth header fixture """

    another_user.save()
    another_user.update({'is_verified': True})
    user_schema = UserSchema()
    token = generate_auth_token(user_schema.dump(another_user)['id'])

    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture(scope='module')
def admin_auth_header(init_db, admin_user):
    """ admin auth header fixture """

    admin_user.save()
    user_schema = UserSchema()
    token = generate_auth_token(user_schema.dump(admin_user)['id'])

    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
