""" Module for testing create user endpoint """

from flask import json

import api.views.user
from api.utils.helpers.messages.success import USER_LOGGED_IN_MSG
from api.utils.helpers.messages.error import (USER_NOT_FOUND,
                                              INVALID_CREDENTIALS,
                                              KEY_REQUIRED_MSG)
from ...mocks.user import (USER_WITH_CORRECT_CREDENTIALS,
                           USER_WITH_INCORRECT_USERNAME,
                           USER_WITH_INCORRECT_PASSWORD)
from ...constants import API_BASE_URL, JSON_CONTENT_TYPE


class TestUserLogin:
    """ Class for testing user login resource """

    def test_user_login_succeeds(self, client, init_db, new_user):
        """ Testing user login """

        new_user.save()
        new_user.update({'is_verified': True})
        user_data = json.dumps(USER_WITH_CORRECT_CREDENTIALS)
        response = client.post(
            f'{API_BASE_URL}/users/login', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == USER_LOGGED_IN_MSG
        assert 'token' in response.json['data']
        assert 'user' in response.json['data']

    def test_user_login_without_credentials_fails(self, client):
        """ Testing user login without credentials """

        user_data = json.dumps({})
        response = client.post(
            f'{API_BASE_URL}/users/login', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == KEY_REQUIRED_MSG.format(
            'username')
        assert response.json['errors'][1]['message'] == KEY_REQUIRED_MSG.format(
            'password')

    def test_user_login_with_incorrect_username_fails(self, client):
        """ Testing user login with incorrect username """

        user_data = json.dumps(USER_WITH_INCORRECT_USERNAME)
        response = client.post(
            f'{API_BASE_URL}/users/login', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == USER_NOT_FOUND

    def test_user_login_with_incorrect_password_fails(self, client):
        """ Testing user login with incorrect password """

        user_data = json.dumps(USER_WITH_INCORRECT_PASSWORD)
        response = client.post(
            f'{API_BASE_URL}/users/login', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == INVALID_CREDENTIALS
