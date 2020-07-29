""" Module for testing create user endpoint """

from flask import json

import api.views.user
from api.utils.helpers.messages.success import USER_CREATED_MSG
from api.utils.helpers.messages.error import (KEY_REQUIRED_MSG,
                                              KEY_NOT_ALLOWED_MSG,
                                              INVALID_EMAIL_MSG,
                                              TAKEN_EMAIL_MSG,
                                              TAKEN_USERNAME_MSG,
                                              WEAK_PASSWORD_MSG)
from ...mocks.user import (VALID_USER,
                           INVALID_USER_WITHOUT_FIRSTNAME,
                           INVALID_USER_WITH__NOT_ALLOWED_PARAM,
                           INVALID_USER_WITH_INVALID_EMAIL,
                           INVALID_USER_WITH_WEAK_PASSWORD,
                           INVALID_USER_WITH_EXISTED_USERNAME)
from ...constants import API_BASE_URL, JSON_CONTENT_TYPE


class TestUserSignup:
    """ Class for testing user signup resource """

    def test_user_signup_succeeds(self, client, init_db):
        """ Testing user signup """

        user_data = json.dumps(VALID_USER)
        response = client.post(
            f'{API_BASE_URL}/users/signup', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 201
        assert response.json['status'] == 'success'
        assert response.json['message'] == USER_CREATED_MSG
        assert response.json['data']['user']['email'] == VALID_USER['email']
        assert response.json['data']['user']['username'] == VALID_USER['username']

    def test_user_signup_with_missing_param_fails(self, client, init_db):
        """ Testing without the firstname """

        user_data = json.dumps(INVALID_USER_WITHOUT_FIRSTNAME)
        response = client.post(
            f'{API_BASE_URL}/users/signup', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['value'] == ''
        assert response.json['errors'][0]['message'] == KEY_REQUIRED_MSG.format(
            'firstname')

    def test_user_signup_with_not_allowed_param_fails(self, client, init_db):
        """ Testing with a not allowed param """

        user_data = json.dumps(INVALID_USER_WITH__NOT_ALLOWED_PARAM)
        response = client.post(
            f'{API_BASE_URL}/users/signup', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['param'] == 'is_admin'
        assert response.json['errors'][0]['message'] == KEY_NOT_ALLOWED_MSG.format(
            'is_admin')

    def test_user_signup_with_invalid_email_fails(self, client, init_db):
        """ Testing user signup with invalid email """

        user_data = json.dumps(INVALID_USER_WITH_INVALID_EMAIL)
        response = client.post(
            f'{API_BASE_URL}/users/signup', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == INVALID_EMAIL_MSG

    def test_user_signup_with_existed_email_fails(self, client, init_db):
        """ Testing user signup with existed email """

        user_data = json.dumps(VALID_USER)
        response = client.post(
            f'{API_BASE_URL}/users/signup', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 409
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == TAKEN_EMAIL_MSG

    def test_user_signup_with_weak_password_fails(self, client, init_db):
        """ Testing user signup with weak password """

        user_data = json.dumps(INVALID_USER_WITH_WEAK_PASSWORD)
        response = client.post(
            f'{API_BASE_URL}/users/signup', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == WEAK_PASSWORD_MSG

    def test_user_signup_with_existed_username_fails(self, client, init_db):
        """ Testing user signup with existing email """

        user_data = json.dumps(INVALID_USER_WITH_EXISTED_USERNAME)
        response = client.post(
            f'{API_BASE_URL}/users/signup', data=user_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 409
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == TAKEN_USERNAME_MSG
