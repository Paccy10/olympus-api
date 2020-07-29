""" Module for testing create user endpoint """

from flask import json

import api.views.user
from api.utils.helpers.messages.success import (PASSWORD_UPDATED_MSG,
                                                PASSWORD_RESET_LINK_SENT_MSG)
from api.utils.helpers.messages.error import (USER_NOT_FOUND,
                                              KEY_REQUIRED_MSG,
                                              INVALID_USER_TOKEN_MSG)
from api.utils.tokens_handler import generate_user_token
from ...mocks.user import (RESET_REQUEST_USER,
                           UNEXISTED_RESET_REQUEST_USER,
                           RESET_PASSWORD_USER)
from ...constants import API_BASE_URL, JSON_CONTENT_TYPE


class TestUserPasswordReset:
    """ Class for testing user password reset resource """

    def test_reset_request_succeeds(self, client, init_db, new_user):
        """ Testing user login """

        new_user.save()
        new_user.update({'is_verified': True})
        request_data = json.dumps(RESET_REQUEST_USER)
        response = client.post(
            f'{API_BASE_URL}/users/reset-password', data=request_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PASSWORD_RESET_LINK_SENT_MSG

    def test_reset_request_with_unexisted_user_fails(self, client, init_db):
        """ Testing reset request with unexisted user """

        request_data = json.dumps(UNEXISTED_RESET_REQUEST_USER)
        response = client.post(
            f'{API_BASE_URL}/users/reset-password', data=request_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == USER_NOT_FOUND

    def test_reset_password_succeeds(self, client, init_db, new_user):
        """ Testing user password reset """

        new_user.save()
        new_user.update({'is_verified': True})
        RESET_PASSWORD_USER['token'] = generate_user_token(new_user.id)
        request_data = json.dumps(RESET_PASSWORD_USER)
        response = client.patch(
            f'{API_BASE_URL}/users/reset-password', data=request_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PASSWORD_UPDATED_MSG

    def test_reset_password_with_invalid_token_fails(self, client, init_db, new_user):
        """ Testing user password reset with invalid token """

        new_user.save()
        new_user.update({'is_verified': True})
        RESET_PASSWORD_USER['token'] = 'token'
        request_data = json.dumps(RESET_PASSWORD_USER)
        response = client.patch(
            f'{API_BASE_URL}/users/reset-password', data=request_data, content_type=JSON_CONTENT_TYPE)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == INVALID_USER_TOKEN_MSG
