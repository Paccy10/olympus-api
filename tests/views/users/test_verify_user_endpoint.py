""" Module for testing verify user endpoint """

import time

from api.utils.tokens_handler import generate_user_token
from api.utils.helpers.messages.success import USER_VERIFIED_MSG
from api.utils.helpers.messages.error import (INVALID_USER_TOKEN_MSG,
                                              ALREADY_VERIFIED_MSG)
from ...constants import API_BASE_URL, JSON_CONTENT_TYPE


class TestUserVerify:
    """ Class for testing user verification resource """

    def test_user_verification_succeeds(self, client, new_user):
        """ Testing User verification """

        new_user.save()
        token = generate_user_token(new_user.id)
        response = client.get(f'{API_BASE_URL}/users/{token}/verify')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == USER_VERIFIED_MSG
        assert response.json['data']['user']['is_verified'] is True

    def test_user_verification_with_expired_token_fails(self, client, new_user):
        """ Testing User verification with expired token """

        new_user.save()
        token = generate_user_token(new_user.id, expiration_time=0)
        time.sleep(1)
        response = client.get(f'{API_BASE_URL}/users/{token}/verify')

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == INVALID_USER_TOKEN_MSG

    def test_user_verification_already_verified_fails(self, client, new_user):
        """ Testing User verification already verified """

        new_user.save()
        new_user.update({'is_verified': True})
        token = generate_user_token(new_user.id)
        response = client.get(f'{API_BASE_URL}/users/{token}/verify')

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == ALREADY_VERIFIED_MSG
