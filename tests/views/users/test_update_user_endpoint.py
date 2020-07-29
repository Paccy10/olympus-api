""" Module for testing update user profile endpoint """

import os
import time
from io import BytesIO
from flask import json

import api.views.user
from api.utils.tokens_handler import generate_auth_token
from api.utils.helpers.messages.success import (PROFILE_UPDATED_MSG)
from api.utils.helpers.messages.error import (INVALID_PHONE_MSG,
                                              TAKEN_PHONE_MSG,
                                              NO_AUTH_TOKEN_MSG,
                                              NO_BEARER_IN_TOKEN_MSG,
                                              INVALID_AUTH_TOKEN_MSG,
                                              EXPIRED_AUTH_TOKEN_MSG)
from ...mocks.user import (PROFILE_USER,
                           PROFILE_USER_WITH_INVALID_PHONE,
                           PROFILE_USER_WITH_TAKEN_PHONE)
from ...constants import API_BASE_URL, FORM_CONTENT_TYPE


class TestUserProfileUpdate:
    """ Class for testing user profile update resource """

    file_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(file_dir, 'tests/mocks/images/pytest.png')

    def test_user_profile_update_succeeds(self, client, init_db, user_auth_header):
        """ Testing User profile update """

        image = open(self.filename, 'rb')
        img_string_io = BytesIO(image.read())

        PROFILE_USER['avatar'] = (img_string_io, 'image.png')
        response = client.put(f'{API_BASE_URL}/users/profile',
                              content_type=FORM_CONTENT_TYPE,
                              data=PROFILE_USER,
                              headers=user_auth_header)
        image.close()
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == PROFILE_UPDATED_MSG
        assert response.json['data']['user']['phone_number'] == PROFILE_USER['phone_number']

    def test_user_profile_update_with_invalid_phone_fails(self, client, init_db, user_auth_header):
        """ Testing User profile update with invalid phone number """

        response = client.put(f'{API_BASE_URL}/users/profile',
                              content_type=FORM_CONTENT_TYPE,
                              data=PROFILE_USER_WITH_INVALID_PHONE,
                              headers=user_auth_header)

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == INVALID_PHONE_MSG

    def test_user_profile_update_with_taken_phone_fails(self,
                                                        client,
                                                        init_db,
                                                        another_user_auth_header):
        """ Testing User profile update with taken phone number """

        response = client.put(f'{API_BASE_URL}/users/profile',
                              content_type=FORM_CONTENT_TYPE,
                              data=PROFILE_USER_WITH_TAKEN_PHONE,
                              headers=another_user_auth_header)

        assert response.status_code == 409
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == TAKEN_PHONE_MSG

    def test_user_profile_update_without_auth_token_fails(self, client):
        """ Testing User profile update without auth token """

        response = client.put(f'{API_BASE_URL}/users/profile',
                              data={},
                              content_type=FORM_CONTENT_TYPE)

        assert response.status_code == 401
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == NO_AUTH_TOKEN_MSG

    def test_user_profile_update_without_bearer_token_fails(self, client):
        """ Testing User profile update without Bearer token  """

        response = client.put(f'{API_BASE_URL}/users/profile',
                              data={},
                              content_type=FORM_CONTENT_TYPE,
                              headers={'Authorization': 'token'})

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == NO_BEARER_IN_TOKEN_MSG

    def test_user_profile_update_without_jwt_part_fails(self, client):
        """ Testing User profile update without jwt part  """

        response = client.put(f'{API_BASE_URL}/users/profile',
                              data={},
                              content_type=FORM_CONTENT_TYPE,
                              headers={'Authorization': 'Bearer'})

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == INVALID_AUTH_TOKEN_MSG

    def test_user_profile_update_with_invalid_jwt_part_fails(self, client):
        """ Testing User profile update with invalid jwt part  """

        response = client.put(f'{API_BASE_URL}/users/profile',
                              data={},
                              content_type=FORM_CONTENT_TYPE,
                              headers={'Authorization': 'Bearer token'})

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == INVALID_AUTH_TOKEN_MSG

    def test_user_profile_update_with_expired_token_fails(self, client):
        """ Testing User profile update with expired token  """

        token = generate_auth_token(1, 0)
        time.sleep(1)
        response = client.put(f'{API_BASE_URL}/users/profile',
                              data={},
                              content_type=FORM_CONTENT_TYPE,
                              headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 401
        assert response.json['status'] == 'error'
        assert response.json['errors'][0]['message'] == EXPIRED_AUTH_TOKEN_MSG
